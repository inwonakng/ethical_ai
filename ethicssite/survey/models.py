import datetime
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


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
class DummyModel(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')

	@classmethod
	def create(cls,text=None):
		obj = cls(question_text = text)
		return obj
"""

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

class GenericRules(models.Model):
    title = models.CharField(max_length=100)



class OptionSetting(models.Model):
    optionSettingText = models.CharField(max_length=300)
    isRadio = models.BooleanField(default=False)
    genericRules = models.ForeignKey(GenericRules, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.optionSettingText


class Option(models.Model):
    optionText = models.CharField(max_length=200)
    optionSetting = models.ForeignKey(OptionSetting, on_delete=models.CASCADE)

    def __str__(self):
        return self.optionText
    

# class GenericResponse(models.Model):
#     ruleSet = models.ForeignKey(GenericRules, on_delete=models.CASCADE)


# generator for a set of scenarios (likned to the user settings)

# Model for storing user input scores
