from django.test import TestCase
from django.contrib.auth import get_user_model
from user_notifications.models import Notification
from user_notifications.tests.example_rules import DoesNotApplyRuleExample, NoRuleNameExample


User = get_user_model()
    

class RuleBaseTests(TestCase):

    fixtures = ['user', 'unit_test']

    def test_rule_name_not_implemented_error(self):
        with self.assertRaises(NotImplementedError) as error:
            invalid_rule = NoRuleNameExample(None, None)

    def test_rule_notification_incorrect_type_implemented_error(self):
        with self.assertRaises(TypeError) as error:
            invalid_rule = DoesNotApplyRuleExample("str instead of notification", User.objects.get(pk=1))

    def test_does_rule_apply_not_implemented_error(self):
        with self.assertRaises(NotImplementedError):
            invalid_rule = DoesNotApplyRuleExample(Notification.objects.all().first(), User.objects.get(pk=1))
            invalid_rule.does_rule_apply()
        
