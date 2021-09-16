# /urls.py
from django.urls import path
from quickvote.views import RoomView, IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('<str:room_name>/<str:username>/', RoomView.as_view(), name='room'),
]
