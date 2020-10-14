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



# Model for a Scenario (e.g. Choose an individual to give a life jacket to.)
class Scenario(models.Model):
	# textfield for scenario details
	prompt = models.CharField(max_length=300)

	# auto-filled date to differentiate same scenario w/ diff choices
	date = models.DateTimeField(default=datetime.date.today)

	def __str__(self):
		return self.prompt

# Model for a generic attribute for some choice (e.g. age or health)
class Attribute(models.Model):
	# attribute name (e.g. age/health)
	name = models.CharField(max_length=30)

	# field value
	value = models.CharField(max_length=30)

	# consider having a set of allowed values?
	# allowed = models.??
	# or specifying the type of value? (int, bool, etc)
	# type = models.??

# Model for a generic choice in a Scenario (e.g. Person)
class Choice(models.Model):
	# name of the current choice (e.g. Person)
	name = models.CharField(max_length=30)
	
	# link to given scenario
	scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)

	# many-to-many relation to given attributes (e.h. Person <-> age, health, occupation)
	attributes = models.ManyToManyField(Attribute, related_name='choice_attributes')

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
class Response(models.Model):
	# choice that is being scored
	choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

	# score for the given choice
	score = models.IntegerField()