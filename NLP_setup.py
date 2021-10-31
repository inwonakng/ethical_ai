# DO NOT RUN THIS FILE IF YOU DON'T KNOW WHAT IT DOES

from survey.models import *
import json
from django.conf import settings
import requests

# this is how many datasets we have
for i in tqdm(range(219)):
    try:
        file = requests.get(
            'https://inwonakng.github.io/survey-scripts/comments/{}_comments.json'.format(i)).content
    except:
        pass
    coms = json.loads(file)
    num = len(coms['comments'])
    for j in range(num):
        oc = OneComment(dataset_index = i,comment_index = j)
        oc.save()