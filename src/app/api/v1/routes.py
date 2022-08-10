from app.api.v1.auth import (SignupView, LoginView, RefreshView, LogoutView,
                             AuthorizeSocialView, LoginSocialView)
from app.api.v1.permissions import PermissionViewSet, PermissionsListViewSet
from app.api.v1.profiles import (ProfileRoleView, ProfileUserView,
                                 ProfileAccessView, ProfileView,
                                 ProfileLoginHistoryView,
                                 ProfileSocialAuthView,
                                 ProfileSocialDeleteView)
from app.api.v1.roles import RoleViewSet, RolesListViewSet, RolePermissionView


# не нашла как blueprint поможет не хранить роуты полотном,
# если используется flask_restful
def initialize_routes(api):
    api.add_resource(SignupView, '/register')
    api.add_resource(LoginSocialView, '/login/<social_name>')
    api.add_resource(AuthorizeSocialView, '/authorize/<social_name>',
                     endpoint="authorize")
    api.add_resource(LoginView, '/login')
    api.add_resource(LogoutView, '/logout')
    api.add_resource(RefreshView, '/refresh')
    api.add_resource(RolesListViewSet, '/role')
    api.add_resource(RoleViewSet, '/role/<uuid:id>')
    api.add_resource(RolePermissionView, '/role/<uuid:id>/permission')
    api.add_resource(PermissionsListViewSet, '/permission')
    api.add_resource(PermissionViewSet, '/permission/<uuid:id>')
    api.add_resource(ProfileRoleView, '/profile/<uuid:id>/role')
    api.add_resource(ProfileAccessView, '/profile/access')
    api.add_resource(ProfileView, '/profile')
    api.add_resource(ProfileUserView, '/profile/user')
    api.add_resource(ProfileLoginHistoryView, '/profile/history')
    api.add_resource(ProfileSocialAuthView, '/profile/social')
    api.add_resource(ProfileSocialDeleteView, '/profile/social/<uuid:id>')
