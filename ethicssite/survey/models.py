import datetime
from django.utils.encoding import python_2_unicode_compatible
from django.db import models


# Question model
@python_2_unicode_compatible
class Question(models.Model):
	# Question field (text field shown to user)
	question_txt: models.CharField(max_length=200, null=False)

	# Question description (text field shown to user)
	question_desc: models.TextField(null=False, blank=False)

	# Not including images (like OPRA) because what happens if the image is
	# inappropriate (since we're having anyone have access to creating)?

	# Can always add more fields to the db if needed

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

# Option/choice model (from OPRA)
@python_2_unicode_compatible
class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_txt = models.CharField(max_length=200)
    timestamp = models.DateTimeField('item timestamp')

	# Return option text
    def __str__(self):
        return self.option_txt

	# ordering
    class Meta:
        ordering = ['timestamp']

"""
class DummyModel(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')

	@classmethod
	def create(cls,text=None):
		obj = cls(question_text = text)
		return obj
"""


# Model for user settings
# generator for a set of scenarios (linked to the user settings)


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
