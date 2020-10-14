import datetime
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
class Survey(models.Model):
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
        sc = SettingsCollection(title="This is a title")
        sc.save()

        # Create a new setting
        newSetting = Setting(settingText="Age")

        # Add options to the setting
        newSetting.settingoption_set.create(optionText="20")
        newSetting.settingoption_set.create(optionText="25")

        # Add the setting to the original settings collection
        sc.setting_set.add(newSetting)
        
"""
class SettingsCollection(models.Model):

    # title of the collection
    title = models.CharField(max_length=100)

# Generic model for a setting that the user could add to a settings collection
class Setting(models.Model):

    # Text describing the setting
    settingText = models.CharField(max_length=300)

    # The generic rule set that this setting is a part of
    genericRules = models.ForeignKey(SettingsCollection, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.settingText

# Option that belongs to a particular Setting
class SettingOption(models.Model):

    # Text defining choosing the option
    optionText = models.CharField(max_length=200)

    # The Setting that this option is a part of
    optionSetting = models.ForeignKey(Setting, on_delete=models.CASCADE)

    def __str__(self):
        return self.optionText




# Model for user settings

# Model for scenario
# contains 'person_set'
class Scenario(models.Model):

	prompt = models.CharField(max_length=300)

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

# class GenericRules(models.Model):
#     title = models.CharField(max_length=100)



# class OptionSetting(models.Model):
#     optionSettingText = models.CharField(max_length=300)
#     isRadio = models.BooleanField(default=False)
#     genericRules = models.ForeignKey(GenericRules, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return self.optionSettingText


# class Option(models.Model):
#     optionText = models.CharField(max_length=200)
#     optionSetting = models.ForeignKey(OptionSetting, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.optionText
    

# class GenericResponse(models.Model):
#     ruleSet = models.ForeignKey(GenericRules, on_delete=models.CASCADE)


# generator for a set of scenarios (likned to the user settings)

# Model for storing user input scores
