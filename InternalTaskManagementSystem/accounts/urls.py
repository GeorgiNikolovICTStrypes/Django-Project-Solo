from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name = 'register'),
    path('log_in/', views.CustomLoginView.as_view(), name = 'loginuser'),
    path('log_out/', LogoutView.as_view(next_page = 'loginuser'), name = 'logout'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name = 'password_reset'),
    path('password_reset_done/', views.CustomPasswordResetDoneView.as_view(), name = 'password_reset_done'),
    path('password_reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name = 'password_reset_confirm'),
    path('password_reset_complete/', views.CustomPasswordResetCompleteView.as_view(), name = 'password_reset_complete'),
    path('view_profile/<int:pk>/', views.ViewProfileView.as_view(), name = 'view_profile'),
    path('edit_profile/<int:pk>/', views.EditProfileView.as_view(), name = 'edit_profile'),
    path('password_change/', views.ChangePasswordView.as_view(), name = 'password_change'),
    path('password_change_done/', views.ChangePasswordDoneView.as_view(), name = 'password_change_done'),
    path('delete_profile/<int:pk>/', views.DeleteProfileView.as_view(), name = 'delete_profile')
]