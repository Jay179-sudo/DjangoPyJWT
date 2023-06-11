from django.urls import path, include
from .views import (
    SuperAdminRegister,
    HostelRegister,
    HostelAdminRegister,
    MessManagerRegister,
    StudentRegister,
    SuperAdminLoginView,
    HostelAdminLogin,
    StudentLogin,
    MessManagerLogin,
    UserProfileView,
    UserChangePasswordView,
    SendPasswordResetEmail,
    UserPasswordResetView,
)

urlpatterns = [
    path("register/", SuperAdminRegister.as_view(), name="super_admin_register"),
    path("hostelregister/", HostelRegister.as_view(), name="hostel_register"),
    path(
        "hosteladminregister/",
        HostelAdminRegister.as_view(),
        name="hostel_admin_register",
    ),
    path(
        "messmanagerregister/",
        MessManagerRegister.as_view(),
        name="mess_manager_register",
    ),
    path(
        "studentregister/",
        StudentRegister.as_view(),
        name="student_register",
    ),
    path("superadminlogin/", SuperAdminLoginView.as_view(), name="super_admin_login"),
    path("hosteladminlogin/", HostelAdminLogin.as_view(), name="hostel_admin_login"),
    path("studentlogin/", StudentLogin.as_view(), name="student_login"),
    path("messmanagerlogin/", MessManagerLogin.as_view(), name="mess_login"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("changepassword/", UserChangePasswordView.as_view(), name="change_password"),
    path(
        "send-rest-password-email/",
        SendPasswordResetEmail.as_view(),
        name="reset_email",
    ),
    path(
        "reset-password/<uid>/<token>/",
        UserPasswordResetView.as_view(),
        name="change_password",
    ),
]
