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
	question_txt = models.CharField(max_length=200, null=False)

	# Question description (text field shown to user)
	question_desc = models.TextField(null=False, blank=False)

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
"""
    Structure: 

        SettingsCollection 1 : <title>
            - Setting 1: Closest Age
                - SettingOption 1: 10
                - SettingOption 2: 15
                - SettingOption 3: 20
                - SettingOption 4: 25
            - Setting 2: Gender
                - SettingOption 1: Male
                - SettingOption 2: Female

        ...

    Usage:

        # Creating a Settings Collection
        sc = SettingCollection(title="This is a title")
        sc_primaryKey = sc.save()

        # Create a new setting
        newSetting = Setting(settingText="Age")

		newSetting.save()

        # Add options to the setting
        newSetting.settingoption_set.create(optionText="20")
        newSetting.settingoption_set.create(optionText="25")

        # Add the setting to the original settings collection
        sc.setting_set.add(newSetting)
        
"""


"""
	{
		'title': 'example title',
		'settings': [
			{
				'setingText': 'example setting text 1',
				'settingsOptions': [
					'this is option 1',
					'this is option 2',
					...
				]
			},
			{
				'setingText': 'example setting text 2',
				'settingsOptions': [
					'this is option 1',
					'this is option 2',
					'this is option 3',
					...
				]
			}
		]
	}
"""


# def addOptionsToSetting(settingObject, optionTextsList):
# 	# settingsObject is assumed to be already saved with a primary key (i.e. added to a SettingsCollection)
# 	# optionsList is a list of strings

# 	# create an option for every string in optionTextsList
# 	for option in optionTextsList:
# 		settingObject.settingoption_set.create(optionText=option)


# def createNewSettingsCollection(input_json_string):
# 	# creates and saves a new SettingsCollection object
# 	# parsed from a json string
# 	# see format in 'rule_test.json'

# 	# parse string into python dictionaries
# 	input_dict = json.loads(input_json_string)

# 	# create a new sc object and save it
# 	sc = SettingCollection(title=input_dict['title'])
# 	sc.save()

# 	# Add new setting objects into newly saved collection
# 	for settingJson in input_dict['settings']:
# 		newSetting = Setting(settingText=settingJson['settingText'])
# 		sc.setting_set.add(newSetting, bulk=False)

# 		addOptionsToSetting(newSetting, settingJson['settingOptions'])
	
# 	# primary key can be accessed through this
# 	return sc


# class SettingCollection(models.Model):

#     # title of the collection
# 	title = models.CharField(max_length=100)

# 	def __str__(self):
# 		return self.title

# 	# Converts a setting collection to Json string and returns it
# 	def toJson(self):
# 		r = {}
# 		r['title'] = self.title

# 		def helper(settingObj):
# 			return {
# 				'settingText': str(settingObj),
# 				'settingOptions': [str(option) for option in settingObj.settingoption_set.all()]
# 			}

# 		r['settings'] = [helper(setting) for setting in self.setting_set.all()]

# 		return json.dumps(r)


# # Generic model for a setting that the user could add to a settings collection
# class Setting(models.Model):

#     # Text describing the setting
#     settingText = models.CharField(max_length=300, default="---")

#     # The generic rule set that this setting is a part of
#     genericRules = models.ForeignKey(
#     	SettingCollection, on_delete=models.CASCADE, default=1)

#     def __str__(self):
#         return self.settingText

# # Option that belongs to a particular Setting


# class SettingOption(models.Model):

#     # Text defining choosing the option
#     optionText = models.CharField(max_length=200, default="---")

#     # The Setting that this option is a part of
#     optionSetting = models.ForeignKey(Setting, on_delete=models.CASCADE, default=1)

#     def __str__(self):
#         return self.optionText

class RuleSet(models.Model):
    title = models.CharField(max_length=100)

    def object_form(self):
        r = {}

        r['categories'] = {}
        for choice_category in self.choicecategory_set.all():
            obj = choice_category.object_form()
            r['categories'][obj[0]] = obj[1]

        for range_category in self.rangecategory_set.all():
            obj = range_category.object_form()
            r['categories'][obj[0]] = obj[1]

        return r
        

    def __str__(self):
        return self.title


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
# contains 'person_set'
class Scenario(models.Model):

	prompt = models.CharField(max_length=300, default="---")

	def __str__(self):
		return self.prompt

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
