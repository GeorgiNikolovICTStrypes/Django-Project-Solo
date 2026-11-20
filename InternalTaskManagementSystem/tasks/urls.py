from django.urls import path
from . import views
urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name = 'dashboard'),
    path('create_task/', views.CreateTaskView.as_view(), name= 'create_a_task'),
    path('view_task/<int:pk>/', views.DetailTaskView.as_view(), name = 'view_task'),
    path('edit_task/<int:pk>/', views.UpdateTaskView.as_view(), name = 'edit_task'),
    path('created_by_me/', views.CreatedByMeView.as_view(), name = 'created_by_me'),
    path('delete_task/<int:pk>/', views.DeleteTaskView.as_view(), name = 'delete_task'),
    path('all_tasks/', views.AllTasksView.as_view(), name = 'all_tasks')
]