from django.db import models

# Create your models here.

class DummyModel(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    @classmethod
    def create(cls,text=None):
        obj = cls(question_text = text)
        return obj

# Model for user settings


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

# model for storing user input scores.
