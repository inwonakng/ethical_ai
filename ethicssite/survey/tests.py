from django.test import TestCase
import json
import os
from survey.models import SettingCollection, Setting,\
    SettingOption, createNewSettingsCollection

script_dir = os.path.dirname(__file__)




class UserSettingTestCase(TestCase):

    def test_to_string(self):
        with open(os.path.join(script_dir, 'rule_test.json')) as f:
            data = json.load(f)

        orig_json_string = json.dumps(data)
        newSettingCollection = createNewSettingsCollection(orig_json_string)
        self.assertEqual(newSettingCollection.toJson(), orig_json_string)

# Create your tests here.

