# chat/urls.py
from django.urls import path
from chat.views import ChatView

urlpatterns = [
    path('<str:room_name>/', ChatView.as_view(), name='room'),
]
