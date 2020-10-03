from django.db import models
from enum import Enum
# Create your models here.

class DummyModel(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    @classmethod
    def create(cls,text=None):
        obj = cls(question_text = text)
        return obj

# Model for user settings

def getAgeModel():
    c_0 = "0"
    c_1 = "1"
    c_2 = "2"
    c_3 = "3"
    c_4 = "4"
    c_5 = "5"
    c_6 = "6"
    c_7 = "7"
    c_8 = "7"
    c_9 = "9"
    c_10 = "10"

    choices = [
        (c_0, '5'),
        (c_1, '8'),
        (c_2, '12'),
        (c_3, '18'),
        (c_4, '21'),
        (c_5, '23'),
        (c_6, '27'),
        (c_7, '32'),
        (c_8, '52'),
        (c_9, '61'),
        (c_10, '72'),
    ]
    choices = [(i, int(j)) for i, j in choices]
    
    age = models.IntegerField(
        max_length=2,
        choices=choices,
    )

    return age

def getHealthModel():
    c_0 = "0"
    c_1 = "1"
    c_2 = "2"
    c_3 = "3"

    choices = [
        (c_0, 'in great health'),
        (c_1, 'small health problems'),
        (c_2, 'moderate health problems'),
        (c_3, 'terminally ill(less than 3 years left)'),
    ]

    health = models.CharField(
        max_length=1,
        choices=choices
    )
    return health

def getGenderModel():
    c_0 = "0"
    c_1 = "1"
    choices = [
        (c_0, 'male'),
        (c_1, 'female'),
    ]

    gender = models.CharField(
        max_length=1,
        choices=choices
    )
    return gender

def getIncomeLevelModel():
    c_0 = "0"
    c_1 = "1"
    c_2 = "2"
    
    choices = [
        (c_0, 'low'),
        (c_1, 'mid'),
        (c_2, 'high'),
    ]

    incomeLevel = models.CharField(
        max_length=1,
        choices=choices
    )
    return incomeLevel

def getNumberOfDependentsModel():
    c_0 = "0"
    c_1 = "1"
    c_2 = "2"
    c_3 = "3"
    c_4 = "4"
    c_5 = "5"

    choices = [
        (c_0, '0'),
        (c_1, '1'),
        (c_2, '2'),
        (c_3, '3'),
        (c_4, '4'),
        (c_5, '5'),
    ]

    choices = [(i, int(j)) for i, j in choices]

    numberOfDependents = models.IntegerField(
        max_length=1,
        choices=choices
    )
    return numberOfDependents
    


class UserSettingsModel(models.Model):
    userID = models.CharField(max_length=100, primary_key=True)
    age = getAgeModel()
    health = getHealthModel()
    gender = getGenderModel()
    incomeLevel = getIncomeLevelModel()
    numberOfDependents = getNumberOfDependentsModel()

    
# generator for a set of scenarios (likned to the user settings)

# model for storing user input scores.
