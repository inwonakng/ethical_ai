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

# Model for storing user input scores
