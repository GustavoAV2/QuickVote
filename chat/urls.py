from django.urls import path
from views import IndexView, RoomView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('chat/<str:number>/', RoomView.as_view(), name='room')
]

