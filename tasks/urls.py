from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task-list'),
    path('task/new/', views.TaskCreateView.as_view(), name='task-create'),
    path('task/<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
    path('task/<int:pk>/complete/', views.complete_task, name='task-complete'),
    path('task/<int:pk>/reopen/', views.reopen_task, name='task-reopen'),
]