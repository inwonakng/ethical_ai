# commands to run in the shell to populate the database:
from survey.models import *
import yaml
from django.conf import settings

# placeholder user

user = User.objects.all()[0]
# user.user_id = 'ddkadfjviasdl'
# user.save()
rule = yaml.safe_load(
        open(settings.BASE_DIR+'/survey/generation/rule/rule.yaml', 'r'))

json_to_ruleset(rule,user)