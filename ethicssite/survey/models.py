import datetime
from django.db import models

# Question model


class questionModel(models.Model):
	# Question field (text field shown to user)
	question_txt: models.CharField(max_length=200, null=False)

	# Question description (text field shown to user)
	question_desc: models.TextField(null=False, blank=False)

	# Not including images (like OPRA) because what happens if the image is
	# inappropriate (since we're having literally anyone have access to creating)?

	# minimum of 2 options that must be entered which can dynamically grow
	# options = models.Array || WHAT DATABASE??

	# Date when question was submitted (auto done in backend)
	date = models.DateField(("Date"), default=datetime.date.today)

	# Implement options when the options object is created above ^^
    # @classmethod
    # def create(cls, questionTXT, questionDESC, optionsTXT):
    # 	# I don't think I need to pass in a parameter for the date
    #     questionObject = cls(question_txt = questionTXT, question_desc = questionDESC, options = optionsTXT, date = datetime.date.today)
    #     return(questionObject)

	# Print the question if invoked
	def __str__(self):
		return self.question_txt

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

# Model for storing user input scores
