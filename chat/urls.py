# chat/urls.py
from django.urls import path
from chat.views import ChatView

urlpatterns = [
    path('<str:room_name>/<str:username>/', ChatView.as_view(), name='room'),
]
