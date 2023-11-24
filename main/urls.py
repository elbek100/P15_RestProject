from django.urls import path

from main.views import TodoApiView, TodoUpdateAPIView, CreateTodoAPIView, TodoSlugAPIView, SearchAPIView, \
    TodoFilterAPIView

urlpatterns = [
    path('todo', TodoApiView.as_view(), name='todo'),
    path('todo/<str:slug>', TodoSlugAPIView.as_view(), name='todo-slug'),
    path('create-todo', CreateTodoAPIView.as_view(), name='create-todo'),
    path('todo-update/<int:pk>', TodoUpdateAPIView.as_view(), name='todo-update'),
    path('category-list', SearchAPIView.as_view(), name='categories'),
    path('filter', TodoFilterAPIView.as_view(), name='filter')
]