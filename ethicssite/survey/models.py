from django.db import models

# Create your models here.

class DummyModel(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    @classmethod
    def create(cls,text=None):
        obj = cls(question_text = text)
        return obj