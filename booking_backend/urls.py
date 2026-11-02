from django.urls import path
from . import views

urlpatterns = [
    path("rooms", views.rooms),
    path("rooms/<int:room_id>", views.roomDetail),
    path("rooms/<int:room_id>/slots", views.roomSlots),
]