from restaurant_list.lib.authorizers import delete, edit, view

DELETE_ACTION = 'delete'
EDIT_ACTION = 'edit'
VIEW_ACTION = 'view'

class Authorization_Check(object):
    """
    Responsible for determining whether a given user has authorization
    to perform a given action
    """

    def __init__(self, action):
        self.authorizer = self.get_authorizer_for_action(action)

    def get_authorizer_for_action(self, action):
        if action not in [DELETE_ACTION, EDIT_ACTION, VIEW_ACTION]:
            raise 'Unknown actions'

        authorizer = None
        if action == DELETE_ACTION:
            authorizer = delete.Delete_Authorizer()
        elif action == VIEW_ACTION:
            authorizer = view.View_Authorizer()
        elif action == EDIT_ACTION:
            authorizer = edit.Edit_Authorizer()

        return authorizer


    def is_authorized(self, user_performing_action, owner):
        return self.authorizer.is_authorized(user_performing_action, owner)
