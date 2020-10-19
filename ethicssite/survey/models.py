import datetime
import json
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

"""
class DummyModel(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    @classmethod
    def create(cls,text=None):
        obj = cls(question_text = text)
        return obj
"""


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


# Model for user settings {


def create_rule_set_from_json_string(rule_set_json_string):
    rule_set = RuleSet()
    rule_set.save()
    d = json.loads(rule_set_json_string)
    for category in d['categories'].keys():
        obj = d['categories'][category]
        if 'range' in obj.keys():

            new_range_category = RangeCategory(
                name=category,
                minVal=float(obj['range'][0]),
                maxVal=float(obj['range'][1]),
                unit=obj['unit'])

            rule_set.rangecategory_set.add(new_range_category, bulk=False)
        else:
            new_choice_category = ChoiceCategory(name=category)
            rule_set.choicecategory_set.add(new_choice_category, bulk=False)

            for index in range(len(obj.keys())):
                new_choice_category.choice_set.create(
                    index=index, description=obj[str(index)])

    for category_name in d['bad combo'].keys():
        obj = d['bad combo'][category_name]
        new_bad_combination = BadCombination(category_name=category_name)
        rule_set.badcombination_set.add(new_bad_combination, bulk=False)
        for category_value in obj.keys():
            sub_obj = obj[category_value]
            new_bad_sub_combination = BadSubCombination(category_value=category_value)
            new_bad_combination.badsubcombination_set.add(
                new_bad_sub_combination, bulk=False)

            for category_name_in in sub_obj.keys():
                new_bad_sub_combination_element = BadSubCombinationElement(category_name=category_name_in)
                new_bad_sub_combination.badsubcombinationelement_set.add(new_bad_sub_combination_element, bulk=False)

                for category_index in sub_obj[category_name_in]:
                    new_bad_sub_combination_element.elementchoice_set.create(
                        category_index=category_index)

    return rule_set


class RuleSet(models.Model):

    def object_form(self):
        return_dict = {}
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


class BadCombination(models.Model):
    category_name = models.CharField(max_length=100)
    ruleSet = models.ForeignKey(RuleSet, on_delete=models.CASCADE, default=1)

    def object_form(self):
        return (self.category_name, {key: value for (key, value) in [obj.object_form() for obj in self.badsubcombination_set.all()]})

    def __str__(self):
        return self.category_name


class BadSubCombination(models.Model):
    category_value = models.CharField(max_length=500)
    badCombination = models.ForeignKey(
        BadCombination, on_delete=models.CASCADE, default=1)

    def object_form(self):
        return (self.category_value, {key: value for (key, value) in [obj.object_form() for obj in self.badsubcombinationelement_set.all()]})
        


    def __str__(self):
        return self.category_value


class BadSubCombinationElement(models.Model):
    category_name = models.CharField(max_length=100)
    badSubCombination = models.ForeignKey(
        BadSubCombination, on_delete=models.CASCADE, default=1)

    def object_form(self):
        return (self.category_name, [str(elem_choice) for elem_choice in self.elementchoice_set.all()])

    def __str__(self):
        return self.category_name

class ElementChoice(models.Model):
    category_index = models.IntegerField()
    badSubCombinationElement = models.ForeignKey(
        BadSubCombinationElement, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.category_index)



class ChoiceCategory(models.Model):
    name = models.CharField(max_length=100)
    ruleSet = models.ForeignKey(RuleSet, on_delete=models.CASCADE, default=1)

    def object_form(self):
        r = {}
        for choice in self.choice_set.all():
            r[choice.object_form()[0]] = choice.object_form()[1]

        return (self.name, r)

    def __str__(self):
        return self.name


class Choice(models.Model):
    index = models.IntegerField()
    description = models.CharField(max_length=500)
    choiceCategory = models.ForeignKey(
        ChoiceCategory, on_delete=models.CASCADE, default=1)

    def object_form(self):
        return (str(self.index), self.description)

    def __str__(self):
        return json.dumps({str(self.index): self.description})


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

# } End Model for user setting




# Model for scenario
class Scenario(models.Model):

    prompt = models.CharField(max_length=300, default="---")

    def __str__(self):
        return self.prompt

# Model for a generic attribute for some combination (e.g. age or health)
class Attribute(models.Model):
    # attribute name (e.g. age or health)
    name = models.CharField(max_length=50, null=False, default='')

    # value for the attribute
    value = models.CharField(max_length=50, null=False, default='')

    def __str__(self):
        return '{:} {:}'.format(self.name, self.value)

# Model for a set of attributes under some scenario (e.g. Person)
class Combo(models.Model):
    # name of current Combo (e.g. Person A)
    name = models.CharField(max_length=50, null=False, default='')

    # link to given scenario
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, default=1)

    # attributes under the current Combo
    attributes = models.ManyToManyField(Attribute, related_name='combo_attributes')

    def __str__(self):
        return self.name


# Model for person
# dependency of scenario
class Person(models.Model):

    # links back to scenario
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)

    age = models.IntegerField(
        validators=[
            MaxValueValidator(120),
            MinValueValidator(0)
        ]
    )
    # spectrum?
    health = models.CharField(max_length=50)
    # true = make
    # false = female
    gender = models.BooleanField()
    # 0 = low
    # 1 = mid
    # 2 = high
    income = models.IntegerField(
        validators=[
            MaxValueValidator(2),
            MinValueValidator(0)
        ]
    )
    number_of_dependants = models.IntegerField(
        validators=[
            MaxValueValidator(20),
            MinValueValidator(0)
        ]
    )
    survival_with_jacket = models.IntegerField(
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ]
    )
    survival_without_jacket = models.IntegerField(
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ]
    )

    def __str__(self):
        return "Person"


# generator for a set of scenarios (likned to the user settings)

# Model for storing user input scores
