from django.test import TestCase
import json
import os
from survey.models import RuleSet, ChoiceCategory, RuleSetChoice, RangeCategory,\
    parse_json

# from survey.models import SettingCollection, Setting,\
#     SettingOption, createNewSettingsCollection

script_dir = os.path.dirname(__file__)


class UserSettingTestCase(TestCase):

    def test_to_string(self):
        with open(os.path.join(script_dir, 'rule_test.json')) as f:
            data = json.load(f)

        orig_json_string = json.dumps(data, indent=4)
        new_rule_set = create_rule_set_from_json_string(orig_json_string)

        self.assertEqual(json.dumps(
            new_rule_set.object_form(), indent=4), orig_json_string)

        loaded_rule_set = RuleSet.objects.get(pk=new_rule_set.id)

        self.assertEqual(json.dumps(
            loaded_rule_set.object_form(), indent=4), orig_json_string)
        self.assertEqual(json.dumps(loaded_rule_set.object_form(
        ), indent=4), json.dumps(new_rule_set.object_form(), indent=4))

    def test_object_form(self):

        rule_set = RuleSet()
        rule_set.save()

        choice_age = ChoiceCategory(name="age")
        rule_set.choicecategory_set.add(choice_age, bulk=False)

        choice_age.rulesetchoice_set.create(index=0, description="5")
        choice_age.rulesetchoice_set.create(index=1, description="8")
        choice_age.rulesetchoice_set.create(index=2, description="12")
        choice_age.rulesetchoice_set.create(index=3, description="18")

        choice_gender = ChoiceCategory(name="gender")
        rule_set.choicecategory_set.add(choice_gender, bulk=False)
        choice_gender.rulesetchoice_set.create(
            index=0, description="in great health")
        choice_gender.rulesetchoice_set.create(
            index=1, description="small health problems")
        choice_gender.rulesetchoice_set.create(
            index=2, description="moderate health problems")
        choice_gender.rulesetchoice_set.create(
            index=3, description="terminally ill(less than 3 years left)")

        range_survival_without = RangeCategory(
            name="survival without",
            minVal=20,
            maxVal=50,
            unit="%")
        rule_set.rangecategory_set.add(range_survival_without, bulk=False)

        # print(json.dumps(rule_set.object_form(), indent=4))


# Create your tests here.
