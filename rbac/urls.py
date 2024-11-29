from django.urls import path
from .views import (
    RegisterUserView, 
    RegisterAdminView, 
    AssignRoleView,
    LogoutView,
    ManageResources,
    MyResources,
    EditResources,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register-user"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path('token/refresh/', TokenRefreshView.as_view(), name="refresh-token"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path("register_admin/", RegisterAdminView.as_view(), name="register-admin"),
    path("assign_role/<int:user_id>", AssignRoleView.as_view(), name="assign_role"),
    path('manage_resources/', ManageResources.as_view() , name="manage-resources"),
    path('my_resources/', MyResources.as_view(), name="my-resources"),
    path('edit_resources/', EditResources.as_view(), name="edit_resources")
]