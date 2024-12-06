from user_notifications.rules import RuleBase


class NoRuleNameExample(RuleBase):

    def __init__(self, notification, user):
        super().__init__(notification, user)

class DoesNotApplyRuleExample(RuleBase):
    RULE_NAME = "DoesNotApplyRuleExample"