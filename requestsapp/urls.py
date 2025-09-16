from django.urls import path
from . import views

app_name = "requestsapp"

urlpatterns = [
    path("", views.requests_page, name="requests_page"),
    path("delete/<int:request_id>/", views.delete_request, name="delete_request"),
]