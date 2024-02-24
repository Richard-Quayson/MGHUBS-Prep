from django.urls import path
from .views import (
    AddToDoView, ToDoListView, RetrieveToDoView, 
    MarkToDoAsCompletedView, UpdateToDoView, DeleteToDoView
)

urlpatterns = [
    path("add/", AddToDoView.as_view(), name="add"),
    path("get/", ToDoListView.as_view(), name="list"),
    path("get/<int:todo_id>/", RetrieveToDoView.as_view(), name="retrieve"),
    path("update/<int:todo_id>/", UpdateToDoView.as_view(), name="update"),
    path("complete/<int:todo_id>/", MarkToDoAsCompletedView.as_view(), name="complete"),
    path("delete/<int:todo_id>/", DeleteToDoView.as_view(), name="delete"),
]