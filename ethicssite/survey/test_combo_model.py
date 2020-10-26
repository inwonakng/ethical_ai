from django.test import TestCase
from django.conf import settings
import json
from .generation.Generator import Generator
from survey.models import Scenario, Attribute, Combo, \
    create_scenario

class ScenarioTestCase(TestCase):
    def test_creation(self):
        # create a sample scenario from the generator
        rule = json.load(open(os.path.join(settings.BASE_DIR, 'survey/generation/rule/rule.json'),'r'))
        story_gen = Generator(rule=rule)
        ss = story_gen.get_scenario()
        scenario_json = json.dumps(ss)

        # test creation of the model
        scenario = create_scenario(scenario_json)

        # check that the retrieved model matches the original scenario
        self.assertEqual(json.dumps(scenario.object_form()), scenario_json)

        # test retrieving the model from the database
        retrieved_scenario = Scenario.objects.get()
        self.assertEqual(json.dumps(retrieved_scenario.object_form()), scenario_json)