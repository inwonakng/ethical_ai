import json
from django import forms
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext, ugettext_lazy as _
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, validate_email
from django.contrib.auth.models import User
from django_mysql.models import JSONField
from random import sample
from random import randint as rint
from itertools import combinations as comb
from survey.generation import Generator as gen

'''User Profile models'''
class UserProfile(models.Model):
    # links the UserProfile to a User model
    # User model is Django's authentication model: contains username, password, etc.
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    creation_time = models.DateTimeField()

    # TODO: fill other useful fields here as needed
    # current_survey = models.OneToOneField('Survey', default=1)

class UserForm(forms.ModelForm):
    """UserForm is the form for user registration
    """
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput())
    password2 = forms.CharField(label=_("Confirm Password"), widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email',)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # will raise a ValidationError if email is invalid
        validate_email(email)
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two passwords do not match", 'password_mismatch')
        return password2

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class Dict(models.Model):
    json = JSONField()

class SurveyGenerator(models.Model):
    rule_id = models.ForeignKey('RuleSet',on_delete=models.CASCADE,null=True)
    combos = models.ManyToManyField('Dict',related_name='combo_dict')
    config = models.OneToOneField('Dict',related_name='config_dict',on_delete=models.CASCADE)
    list_categs = models.ManyToManyField('ListCateg')
    range_categs = models.ManyToManyField('RangeCateg')

    def check_duplicates(self, scenario):
        # get all possible pairs to compare duplicates
        tocheck = list(comb(scenario, 2))
        found = {}
        for c1, c2 in tocheck:
            dups = [(k,v) for k,v in c1.items() if c2[k] == v]
            for d in dups:
                if not d in found:
                    found[d] = 0
                else:
                    found[d] += 1
        numfound = list(found.values())
        numlen = len(numfound)
        return numlen == 0 or (max(numfound) < self.config.json['same_categories'] + 1 and numfound.count(self.config.json['same_categories']) < len(scenario) - 1)

    def get_scenario(self):
        '''
            random pick
            @TODO we need to record what we have already
            @TODO maybe take too long
        '''
        selected = []
        while True:
            s = sample(list(range(len(self.combos.all()))), self.config.json['scenario_size'])
            outputs = []
            for i in s:
                ss = self.combos.all()[i].json.copy()
                for r in self.range_categs.all(): ss[r.name] = r.get_range()
                outputs.append(ss)
            if self.check_duplicates(outputs):
                selected = outputs
                break
        for c in self.list_categs.all():
            selected = [c.translate(ss) for ss in selected]
        
        return selected
    
def build_generator(rule):
    sg = SurveyGenerator()
    sg.rule_id = rule

    gg = gen.Generator(rule)
    dd = Dict(json = gg.config)
    dd.save()

    sg.config = dd
    sg.save()

    for c in gg.combos:
        dd = Dict(json = c.getCombo())
        dd.save() 
        sg.combos.add(dd)
    sg.save()

    for rcateg in rule.range_categs.all():
        sg.range_categs.add(rcateg)
    for lcateg in rule.choice_categs.all():
        sg.list_categs.add(lcateg)
    sg.save()
    return sg

# Question model
@python_2_unicode_compatible
# Model for a generic attribute for some combination (e.g. age or health)
class Attribute(models.Model):
    # attribute name (e.g. age or health)
    name = models.CharField(max_length=50, null=False, default='')
    # value for the attribute
    value = models.CharField(max_length=50, null=False, default='')

class Survey(models.Model):
    prompt = models.CharField(max_length=200, null=False, default='')
    desc = models.TextField(null=False, blank=False, default='')
    date = models.DateTimeField(default=timezone.now)
    scenarios = models.ManyToManyField('Scenario')
    ruleset_id = models.IntegerField(null=False, default=2)
    feature_scores = models.ManyToManyField('FeatureScore')
    # user taking this survey
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class FeatureScore(models.Model):
    name = models.TextField(null=False,default='default_namee')
    score = models.OneToOneField('SingleResponse',on_delete=models.CASCADE)

class Scenario(models.Model):
    options = models.ManyToManyField('Option')

class Option(models.Model):
    name = models.CharField(max_length=50, null=False, default='')
    attributes = models.ManyToManyField('Attribute' , related_name='combo_attributes')
    text = models.CharField(max_length=50, null=False, default='')
    score = models.OneToOneField("SingleResponse", on_delete=models.CASCADE,null=True)

class SingleResponse(models.Model):
    value = models.CharField(max_length=50, null=False, default='')

# Holds ruleset ID and scenario model
class TempScenarios(models.Model):
    user_id = models.IntegerField(null=False, blank=False)
    session_id = models.IntegerField(null=False, blank=False)
    ruleset_id = models.IntegerField(null=False, blank=False)
    scenario = models.ManyToManyField('Scenario')


'''Survey models sections end here'''

# Rule model
class RuleSet(models.Model):
    choice_categs = models.ManyToManyField('ListCateg')
    range_categs = models.ManyToManyField('RangeCateg')
    badcombos = models.ManyToManyField('BadCombo')
    # generative_survey = models.OneToManyField('Survey') # ISSUE OneToMany (get this working) or ManyToMany
    # # https://stackoverflow.com/questions/6928692/how-to-express-a-one-to-many-relationship-in-django

    same_categories = models.IntegerField(null=True, default=2)
    scenario_size = models.IntegerField(null=True, default=2)

    # ruleset creator
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    generative = models.BooleanField(null=False, blank=False, default=False)
    rule_title = models.TextField(null=False,default='Default description')
    prompt = models.TextField(null=False,default='Default prompt!')
    # this field is only populated if not generative

    scenarios = models.ManyToManyField("Scenario")    

    '''These accessor functions are for the generator to use'''

    def get_sample(self):
        ss = self.scenarios.all()[0]
        return [o.text for o in ss.options.all()]

    def get_choicecategs(self):
        # for cc in self.choice_categs
        categ = {}
        for cc in self.choice_categs.all():
            c = cc.object_form()
            categ[c[0]] = c[1]
        return categ

    def object_form(self):
        # for cc in choice_categs.all():
        cho = self.get_choicecategs()
        ran = self.get_rangecategs()
        cho.update(ran)
        return {
            'config': self.get_configs(),
            'categories': cho,
            'bad_combos': self.get_badcombos()
        }

    def get_rangecategs(self):
        bb = {}
        for cc in self.range_categs.all():
            bb.update(cc.object_form())
        return bb

    def get_badcombos(self):
        return {bc.object_form()[0]:bc.object_form()[1]
        for bc in self.badcombos.all()}

    def get_configs(self):
        return {
            'same_categories': self.same_categories,
            'scenario_size': self.scenario_size
        }

# Bad combination model
class BadCombo(models.Model):
    category_name = models.CharField(max_length=100)
    subcombos = models.ManyToManyField('BadSubCombo')

    def object_form(self):
        return (self.category_name, {key: value for (key, value) in [obj.object_form() for obj in self.subcombos.all()]})

    def __str__(self):
        return self.category_name

# This level contains the bad combos for specified category
class BadSubCombo(models.Model):
    categ = models.CharField(max_length=500)
    badcombo_elems = models.ManyToManyField('BadSubComboElement')

    def object_form(self):
        return (self.categ,
                {key: value
                for (key, value) in
                    [obj.object_form() for obj in self.badcombo_elems.all()]})

    def __str__(self):
        return self.categ

# Bad sub?? combination element model
class BadSubComboElement(models.Model):
    categ = models.CharField(max_length=100)
    elems = models.ManyToManyField('ElementChoice')

    def object_form(self):
        return (self.categ, [str(elem_choice) for elem_choice in self.elems.all()])

    def __str__(self):
        return self.categ

# Element choice model
class ElementChoice(models.Model):
    category_index = models.IntegerField()

    def __str__(self):
        return str(self.category_index)

# Choice category model - choosing froma list of values
class ListCateg(models.Model):
    name = models.CharField(max_length=100)
    choices = models.ManyToManyField('RuleSetChoice')

    def object_form(self):
        r = {c.object_form()[0]: c.object_form()[1]
             for c in self.choices.all()}
        return [self.name, r]

    def object_form_choices(self):
        l = [];
        for c in self.choices.all():
            l.append([c.object_form()[0],c.object_form()[1]])
        return l

    def __str__(self):
        return json.dumps(self.object_form())

    def translate(self,vals):
        idx = vals[self.name]
        vals[self.name] = self.choices.get(index=idx).value
        return vals

    def get_id(self):
        return self.id

# Rule set choice model
class RuleSetChoice(models.Model):
    index = models.IntegerField()
    value = models.CharField(max_length=500)

    def object_form(self):
        return (str(self.index), self.value)

    def __str__(self):
        return json.dumps({str(self.index): self.value})

# Range category model
class RangeCateg(models.Model):
    name = models.CharField(max_length=100)
    minVal = models.FloatField()
    maxVal = models.FloatField()
    unit = models.CharField(max_length=50)

    def get_range(self):
        return str(rint(self.minVal,self.maxVal)) + self.unit

    def object_form(self):
        return {self.name: {
                "range": [self.minVal, self.maxVal],
                "unit": self.unit}
                }

    def __str__(self):
        return json.dumps(self.object_form())


'''
Currently this function receives the survey data as in a format of [Scenario1,scenario2,...].
Then it creates the all the submodels accordingly and links the foreign keys
Before this function is called, the Survey model should be instantiated and saved beforehand

ex)
ss = Survey(prompt='test',desc='hi')
ss.save()
ss.create_survey([[{'alt1':2,'alt2':3}]])
After this, ss will be the complete survey object
(does not carry user scores yet)

Test scenario example:
[
    [
        [
            {
            "age": "61",
            "health": "terminally ill(less than 3 years left)",
            "gender": "male",
            "income level": "low",
            "number of dependents": "2",
            "survival without": "42%",
            "survival difference": "79%",
            },
            {
            "age": "12",
            "health": "small health problems",
            "gender": "female",
            "income level": "low",
            "number of dependents": "0",
            "survival without": "23%",
            "survival difference": "66%",
            },
        ],
        [
            {
            "age": "5",
            "health": "small health problems",
            "gender": "female",
            "income level": "low",
            "number of dependents": "3",
            "survival without": "31%",
            "survival difference": "59%",
            },
            {
            "age": "23",
            "health": "moderate health problems",
            "gender": "male",
            "income level": "high",
            "number of dependents": "0",
            "survival without": "30%",
            "survival difference": "58%",
            },
            {
            "age": "23",
            "health": "moderate health problems",
            "gender": "male",
            "income level": "high",
            "number of dependents": "0",
            "survival without": "30%",
            "survival difference": "58%",
            },
        ],
        [
            {
            "age": "5",
            "health": "small health problems",
            "gender": "female",
            "income level": "low",
            "number of dependents": "3",
            "survival without": "31%",
            "survival difference": "59%",
            },
            {
            "age": "23",
            "health": "moderate health problems",
            "gender": "male",
            "income level": "high",
            "number of dependents": "0",
            "survival without": "30%",
            "survival difference": "58%",
            },
        ],
    ],
    [
        ["0", "1"],
        ["2", "3", "5"],
        ["4", "5"],
    ],
    [
        { "key": "age", "value": "0"},
        { "key": "gender", "value": "5"},
        { "key": "health", "value": "3"},
        { "key": "income level", "value": "6"},
        { "key": "number of dependents", "value": "8"},
        { "key": "survival without", "value": "2"},
        { "key": "survival difference", "value": "9"},
    ],
]
'''
# This function will recieve a list of json scenarios and
# load them into Django models.

# FUTURE: Should be modified to store the survey's title, description, and prompt
def json_to_survey(survey_data, user, prompt='empty', desc='empty'):

    # First, we need to translate the data from byte to the data structure above
    survey_data = survey_data.decode('utf-8')
    survey_data = json.loads(survey_data)

    curr_survey = Survey(prompt=prompt, desc=desc, user=user)
    curr_survey.save()
    scenarios = 0
    for scenario in survey_data[0]:
        
        curr_scenario = Scenario()
        curr_scenario.save()

        
        person_count = 1
        scenarios += 1

        for option in scenario:
            
            curr_option = Option(name="Person " + str(person_count))

            # Saves option scores
            curr_score = SingleResponse(value=survey_data[1][(int(person_count/2))][int((person_count-1)%len(scenario))])
            curr_score.save()

            curr_option.score = curr_score
            curr_option.save()

            person_count += 1

            # Will trigger this if the options aren't strings.
            # For now, the entire string is marked as an option.
            # In the future, should there be a way to parse the string
            # to form attributes?
            if(isinstance(option,str) != True):

                for attribute in option:
                    value = option[attribute]

                    curr_attribute = Attribute(name=attribute, value=value)
                    curr_attribute.save()

                    curr_option.attributes.add(curr_attribute)
                    curr_option.save()

            curr_scenario.options.add(curr_option)
            curr_scenario.save()

        curr_survey.scenarios.add(curr_scenario)
        curr_survey.save()

    # loads feature scores into survey
    for feature in survey_data[2]:
        
        curr_score = SingleResponse(value=feature["value"])
        curr_score.save()

        curr_feature = FeatureScore(name=feature["key"], score=curr_score)
        curr_feature.save()

        curr_survey.feature_scores.add(curr_feature)
        curr_survey.save()
    
    curr_survey.save()
    print(curr_survey)
    return curr_survey

'''
type(d) must be dict()
some hardcoding stuff:
If the user is passing in a 'custom' ruleset, then the dictionary must take this form:
{1:['text1','text2'],2:['text1','text2'],...}

'''
def json_to_ruleset(d,user,title,prompt):
    # true if 'config' values exist in d
    generative = 'config' in d
    if generative:
        inp = {'same_categories': d['config']['same_categories'],
            'scenario_size': d['config']['scenario_size']}
        rule_set = RuleSet(**inp)
    else: rule_set = RuleSet()
    rule_set.rule_title = title
    # This should be converted to actually grab the user. Placeholder for now so stuff don't break
    rule_set.user = user
    rule_set.generative = generative
    rule_set.prompt = prompt
    rule_set.save()
    if generative:
        for categ, obj in d['categories'].items():
            if 'range' in obj:
                range_category = RangeCateg(
                    name=categ,
                    minVal=float(obj['range'][0]),
                    maxVal=float(obj['range'][1]),
                    unit=obj['unit'])
                range_category.save()
                rule_set.range_categs.add(range_category)
            else:
                list_categ = ListCateg(name=categ)
                list_categ.save()
                for k, v in obj.items():
                    list_categ.choices.create(
                        index=k, value=v)
                rule_set.choice_categs.add(list_categ)

        for categ_name, obj in d['bad_combos'].items():
            bad_combo = BadCombo(category_name=categ_name)
            bad_combo.save()
            for cval, sub_obj in obj.items():
                subcombo = BadSubCombo(
                    categ=cval)
                subcombo.save()

                for category_name_in in sub_obj.keys():
                    bsubcom_elem = BadSubComboElement(
                        categ=category_name_in)
                    bsubcom_elem.save()
                    for category_index in sub_obj[category_name_in]:
                        bsubcom_elem.elems.create(
                            category_index=category_index)

                    subcombo.badcombo_elems.add(
                        bsubcom_elem)

                bad_combo.subcombos.add(
                    subcombo)
            rule_set.badcombos.add(bad_combo)
    else:
        for v in d:
            scen = Scenario()
            scen.save()
            for i,s in enumerate(v):
                op = Option()
                op.name = 'Option '+ str(i)
                op.text = s
                op.save()
                scen.options.add(op)
            scen.save()
            rule_set.scenarios.add(scen)
    rule_set.save()
    return rule_set

