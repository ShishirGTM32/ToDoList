from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, PasswordResetDoneView

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='LogIn'),
    path('logout/', LogoutView.as_view(next_page='LogIn'), name='LogOut'),
    path('register/', views.RegisterPage.as_view(), name='Register'),
    path('', views.TaskList.as_view(), name="TaskList"),
    path('task-create', views.TaskCreate.as_view(), name="CreateTask"),
    path('task/<int:pk>', views.TaskDetail.as_view(), name="TaskDetail"),
    path('task-update/<int:pk>', views.TaskUpdate.as_view(), name="TaskUpdate"),
    path('task-delete/<int:pk>', views.TaskDelete.as_view(), name="TaskDelete"),
    path('task-toggle-complete/<int:pk>/', views.ToggleCompleteView.as_view(), name='ToggleComplete'),
    path('password_reset/', views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('password_reset_done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]