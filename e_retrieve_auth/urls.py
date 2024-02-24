from e_retrieve_auth.views import *
from django.urls import path

app_name = "auth"

urlpatterns = [
    path('', HomePage.as_view(), name="home"),

    # Auth
    path('login/', LoginPageView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),

    # Dashboard
    path('dashboard/', DashBoard.as_view(), name="dashboard"),

    # Student
    path('manage_student/', ManageStudentView.as_view(), name="manage_student"),
    path('update_student/<str:pk>',
         UpdateStudentView.as_view(), name="update_student"),
    path('delete_student/<str:pk>',
         DeleteStudentView.as_view(), name="delete_student"),

    # Admin
    path('manage_admin/', ManageAdminView.as_view(), name="manage_admin"),
    path('update_admin/<str:pk>',
         UpdateAdminView.as_view(), name="update_admin"),
    path('delete_admin/<str:pk>',
         DeleteAdminView.as_view(), name="delete_admin"),

    # profile
    path('update_profile/<str:pk>',
         UpdateProfileView.as_view(), name="update_profile"),
    path('change_password/<str:pk>',
         ChangePassword.as_view(), name="change_password"),

    # past question
    path('manage_past_question/', ManagePastQuestionView.as_view(), name="manage_past_question"),
    path('update_past_question/<str:pk>',
         UpdatePastQuestionView.as_view(), name="update_past_question"),
    path('delete_past_question/<str:pk>',
         DeletePastQuestionView.as_view(), name="delete_past_question"),

    # retrieve past question
    path('retrieve_past_question/', RetrievePastQuestionView.as_view(), name="retrieve_past_question"),
]
