class Edit_Authorizer(object):
    """
    Determines whether a user has permission to edit content
    """

    def is_authorized(self, user_performing_action, owner):
        return user_performing_action == owner

