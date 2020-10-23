import datetime
import json
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Question model
@python_2_unicode_compatible
class Question(models.Model):
    # Question field (text field shown to user)
    question_txt = models.CharField(max_length=200, null=False,default='')

    # Question description (text field shown to user)
    question_desc = models.TextField(null=False, blank=False,default='')

    # Can always add more fields for the question object if needed

    # Date when question was submitted (auto done in backend)
    date = models.DateTimeField(default=datetime.date.today)

    # Return question text
    def __str__(self):
        return self.question_txt

    # Alternative to overriding __init__ (initial)
    @classmethod
    def create(cls, questionTXT, questionDESC):
        questionObject = cls(question_txt=questionTXT, question_desc=questionDESC)
        return(questionObject)

# Rule model
class RuleSet(models.Model):

    def object_form(self):
        return_dict = {}

        return_dict['config'] = {}
        return_dict['config']['same_categories'] = 3
        return_dict['config']['scenario_size'] = 2

        return_dict['categories'] = {}
        for choice_category in self.choicecategory_set.all():
            obj = choice_category.object_form()
            return_dict['categories'][obj[0]] = obj[1]

        for range_category in self.rangecategory_set.all():
            obj = range_category.object_form()
            return_dict['categories'][obj[0]] = obj[1]


        return_dict['bad combo'] = {key: value for (key, value) in [obj.object_form() for obj in self.badcombination_set.all()]}


        return return_dict

    def __str__(self):
        return self.id

# Bad combination model
class BadCombination(models.Model):
    category_name = models.CharField(max_length=100)
    ruleSet = models.ForeignKey(RuleSet, on_delete=models.CASCADE, default=1)

    def object_form(self):
        return (self.category_name, {key: value for (key, value) in [obj.object_form() for obj in self.badsubcombination_set.all()]})

    def __str__(self):
        return self.category_name

# Bad sub?? combination model
class BadSubCombination(models.Model):
    category_value = models.CharField(max_length=500)
    badCombination = models.ForeignKey(
        BadCombination, on_delete=models.CASCADE, default=1)

    def object_form(self):
        return (self.category_value, {key: value for (key, value) in [obj.object_form() for obj in self.badsubcombinationelement_set.all()]})
        
    def __str__(self):
        return self.category_value

# Bad sub?? combination element model
class BadSubCombinationElement(models.Model):
    category_name = models.CharField(max_length=100)
    badSubCombination = models.ForeignKey(
        BadSubCombination, on_delete=models.CASCADE, default=1)

    def object_form(self):
        return (self.category_name, [str(elem_choice) for elem_choice in self.elementchoice_set.all()])

    def __str__(self):
        return self.category_name

# Element choice model
class ElementChoice(models.Model):
    category_index = models.IntegerField()
    badSubCombinationElement = models.ForeignKey(
        BadSubCombinationElement, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.category_index)

# Choice category model
class ChoiceCategory(models.Model):
    name = models.CharField(max_length=100)
    ruleSet = models.ForeignKey(RuleSet, on_delete=models.CASCADE, default=1)

    def object_form(self):
        r = {}
        for choice in self.rulesetchoice_set.all():
            r[choice.object_form()[0]] = choice.object_form()[1]

        return (self.name, r)

    def __str__(self):
        return self.name

# Rule set choice model
class RuleSetChoice(models.Model):
    index = models.IntegerField()
    description = models.CharField(max_length=500)
    choiceCategory = models.ForeignKey(
        ChoiceCategory, on_delete=models.CASCADE, default=1)

    def object_form(self):
        return (str(self.index), self.description)

    def __str__(self):
        return json.dumps({str(self.index): self.description})

# Range category model
class RangeCategory(models.Model):
    name = models.CharField(max_length=100)
    minVal = models.FloatField()
    maxVal = models.FloatField()
    unit = models.CharField(max_length=50)

    ruleSet = models.ForeignKey(
        RuleSet, on_delete=models.CASCADE, default=1)

    def object_form(self):

        return (self.name, {
            "range": [self.minVal, self.maxVal],
            "unit": self.unit
        })

    def __str__(self):

        return json.dumps({self.name: {
            "range": [self.minVal, self.maxVal],
            "unit": self.unit
        }})

# Model for scenario
class Scenario(models.Model):

    prompt = models.CharField(max_length=300, default="---")

    def object_form(self):
        # returns a list of combos that makes up the scenario e.g. [{}, {}, {}]
        # todo: object_form currently doesn't include prompt, consider this
        res = []
        for combo in self.combo_set.all():
            res.append(combo.object_form())
        
        return res

    def __str__(self):
        return str(self.prompt)

# Model for a generic attribute for some combination (e.g. age or health)
class Attribute(models.Model):
    # attribute name (e.g. age or health)
    name = models.CharField(max_length=50, null=False, default='')

    # value for the attribute
    value = models.CharField(max_length=50, null=False, default='')

    def object_form(self):
        # return a tuple with a (name, value)
        return (self.name, self.value)

    def __str__(self):
        return json.dumps(self.object_form())

# Model for a set of attributes under some scenario (e.g. Person)
class Combo(models.Model):
    # name of current Combo (e.g. Person A)
    name = models.CharField(max_length=50, null=False, default='')

    # link to given scenario
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, default=1)

    # attributes under the current Combo
    attributes = models.ManyToManyField(Attribute, related_name='combo_attributes')

    def object_form(self):
        # return a dict of all attribute and values e.g. {'age': '52'}
        res = {}
        for attr in self.attributes.all():
            key, val = attr.object_form()
            res[key] = val
        
        return res

    def __str__(self):
        return json.dumps(self.object_form())

# Model for storing user input scores
class Response(models.Model):
    # consider including some fields for identifying the user?
    # userid = ?

    # which combo the current score is for
    combo = models.ForeignKey(Combo, on_delete=models.CASCADE, default=1)

    # user input score
    # todo: consider changing this to be IntegerChoices / Range?
    score = models.IntegerField()

def parse_json(rule_set_json_string):
    rule_set = RuleSet()
    rule_set.save()
    d = json.loads(rule_set_json_string)
    for category in d['categories'].keys():
        obj = d['categories'][category]
        if 'range' in obj.keys():

            range_category = RangeCategory(
                name=category,
                minVal=float(obj['range'][0]),
                maxVal=float(obj['range'][1]),
                unit=obj['unit'])

            rule_set.rangecategory_set.add(range_category, bulk=False)
        else:
            choice_category = ChoiceCategory(name=category)
            rule_set.choicecategory_set.add(choice_category, bulk=False)

            for index in range(len(obj.keys())):
                choice_category.rulesetchoice_set.create(
                    index=index, description=obj[str(index)])

    for category_name in d['bad combo'].keys():
        obj = d['bad combo'][category_name]
        bad_combination = BadCombination(category_name=category_name)
        rule_set.badcombination_set.add(bad_combination, bulk=False)
        for category_value in obj.keys():
            sub_obj = obj[category_value]
            bad_sub_combination = BadSubCombination(
                category_value=category_value)
            bad_combination.badsubcombination_set.add(
                bad_sub_combination, bulk=False)

            for category_name_in in sub_obj.keys():
                bad_sub_combination_element = BadSubCombinationElement(
                    category_name=category_name_in)
                bad_sub_combination.badsubcombinationelement_set.add(
                    bad_sub_combination_element, bulk=False)

                for category_index in sub_obj[category_name_in]:
                    bad_sub_combination_element.elementchoice_set.create(
                        category_index=category_index)

    return rule_set

def create_scenario(json_string):
    # currently json as scenario is list of combos e.g. '[{}, {}, {}]'
    # todo: scenario should have some prompt, should this be included in json?
    scenario = Scenario()
    scenario.save()

    data = json.loads(json_string)
    for json_combo in data:
        combo = Combo(scenario=scenario)
        combo.save()
        for json_attr in json_combo.keys():
            attribute = Attribute(name=json_attr, value=json_combo[json_attr])
            attribute.save()
            combo.attributes.add(attribute)

    return scenario
