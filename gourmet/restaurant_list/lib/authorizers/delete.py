class Delete_Authorizer(object):
    """
    Determines whether given user is authorized to delete content
    """

    def is_authorized(self, user_performing_action, owner):
        return user_performing_action == owner
