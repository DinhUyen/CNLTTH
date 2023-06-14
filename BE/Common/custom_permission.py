from rest_framework import permissions
from Common import generics_cursor
from Common.generics import NO_ROLE,GUARDSMAN_ROLE
class CustomPermissions(permissions.BasePermission):
    def __init__(self):
        super().__init__()

    # def get_allowed_methods(self, username):
    #     ## query in database here
    #     username = username
    #     return ['GET','POST','PUT','DELETE']

    def get_allowed_methods(self, CODE_VIEW):
        if int(CODE_VIEW) == GUARDSMAN_ROLE : # role admin
            return ['GET']
        elif int(CODE_VIEW) > NO_ROLE:
            return ['GET','POST','PUT','DELETE']
        else:
            return []
    
    def has_permission(self, request, view):
        ## check if token is valid
        if not (request.user and request.user.is_authenticated):
            return False
        ## get username
        username = request.user
        try:       
            ## get allowed methods by username [query to database]
            allowed_methods = self.get_allowed_methods(request.user.roleID)
            # allowed_methods = self.search_allowed_methods
            ## check if request method in allowed methods
            if request.method in allowed_methods :
                return True
            return False
        except:
            return False