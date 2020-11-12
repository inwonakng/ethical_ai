import json
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

'''Survey models sections start here'''

class Survey(models.Model):
    prompt = models.CharField(max_length=200, null=False, default='')
    desc = models.TextField(null=False, blank=False, default='')
    date = models.DateTimeField(default=timezone.now)
    scenarios = models.ManyToManyField('Scenario')
    attributes = models.ManyToManyField('Attribute')
    ruleset_id = models.IntegerField(null=False, default=2)


class Scenario(models.Model):
    options = models.ManyToManyField('Option')


class Option(models.Model):
    name = models.CharField(max_length=50, null=False, default='')
    attributes = models.ManyToManyField('Attribute', related_name='combo_attributes')
    text = models.CharField(max_length=50, null=False, default='')


class SingleResponse(models.Model):
    value = models.CharField(max_length=50, null=False, default='')
    option = models.OneToOneField(Option, on_delete=models.CASCADE, default=1)


class Attribute(models.Model):
    name = models.CharField(max_length=50, null=False, default='')
    value = models.CharField(max_length=50, null=False, default='')


'''Survey models sections end here'''

# Rule model


class RuleSet(models.Model):
    choice_categs = models.ManyToManyField('ListCateg')
    range_categs = models.ManyToManyField('RangeCateg')
    badcombos = models.ManyToManyField('BadCombo')
    generative_survey = models.ManyToManyField('Survey')

    same_categories = models.IntegerField(null=False, default=2)
    scenario_size = models.IntegerField(null=False, default=2)
    generative = models.BooleanField(null=False, blank=False, default=False)
    '''These accessor functions are for the generator to use'''

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
        return {bc.object_form()[0]: bc.object_form()[1]
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

    def __str__(self):
        return json.dumps(self.object_form())

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
]
'''
# This function will recieve a list of json scenarios and
# load them into Django models.


def json_to_survey(survey_data, prompt='empty', desc='empty'):

    curr_survey = Survey(prompt=prompt, desc=desc)
    curr_survey.save()

    for scenario in survey_data:

        curr_scenario = Scenario()
        curr_scenario.save()

        person_count = 1

        for option in scenario:

            curr_option = Option(name="Person " + str(person_count))
            curr_option.save()

            person_count += 1

            for attribute in option:
                value = option[attribute]

                curr_attribute = Attribute(name=attribute, value=value)
                curr_attribute.save()

                curr_option.attributes.add(curr_attribute)
                curr_option.save()

                curr_survey.attributes.add(curr_attribute)
                curr_survey.save()

            curr_scenario.options.add(curr_option)
            curr_scenario.save()

        curr_survey.scenarios.add(curr_scenario)
        curr_survey.save()

    return curr_survey


# type(d) must be dict()
def json_to_ruleset(d):
    inp = {'same_categories': d['config']['same_categories'],
           'scenario_size': d['config']['scenario_size']}
    rule_set = RuleSet(**inp)
    rule_set.save()
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
    rule_set.save()
    print(rule_set.id)
    return rule_set
