import datetime
from django.db import models

# Question model
class questionModel(models.Model):
	# Question field (text field shown to user)
	question_txt: models.CharField(max_length=200, null=False)

	# Question description (text field shown to user)
	question_desc: models.TextField(null=False, blank=False)

	# Date when question was submitted (auto done in backend)
	date = models.DateField(("Date"), default=datetime.date.today)

	# minimum of 2 options that must be entered which can dynamically grow

	# every option has an **optional**..  option description (not required)

	# Print the question if invoked
	def __str__(self):
		return self.question_text

	# fix this
    @classmethod
    def create(cls,text=None):
        obj = cls(question_text = text)
        return obj

# Model for user settings
class userSettings(models.Model):
	# generator for a set of scenarios (likned to the user settings)
	return(None)


# model for storing user input scores.
class inputScores(models.Model):
	return(None)
