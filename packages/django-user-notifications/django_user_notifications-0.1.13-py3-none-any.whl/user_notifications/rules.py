from django.utils import timezone
from django.db.models import Q
from user_messages import api as user_messages
from user_notifications.models import Notification


class RuleBase:
    RULE_NAME = None
    notification = None
    user = None
    apply_rule = False

    def __init__(self, notification, user):
        if not self.RULE_NAME:
            raise NotImplementedError
        if not type(notification) == Notification:
            raise TypeError("passed notification variable is not a Notification type")
        if not user:
            raise TypeError("user cannot be None type")

        self.notification = notification
        self.user = user
    
    def __str__(self):
        return self.RULE_NAME

    def does_rule_apply(self):
        raise NotImplementedError()

    def gt(self, value):
        raise NotImplementedError()

    def gte(self, value):
        raise NotImplementedError()

    def lt(self, value):
        raise NotImplementedError()

    def lte(self, value):
        raise NotImplementedError()



class RuleConstructorBase:
    """
    You can create you own rule contructor or implement another
    design to implement and process rules. This is just an example"""

    def create_rule(notification, rule_name, user):
        raise NotImplementedError()



    
