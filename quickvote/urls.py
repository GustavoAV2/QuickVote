# /urls.py
from django.urls import path
from quickvote.views import RoomView, IndexView, FastLogin, RoomPlanningView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('fast-login/<str:room_name>/<str:password>', FastLogin.as_view(), name='fast-login'),
    path('<str:room_name>/<str:username>/<str:password>', RoomView.as_view(), name='room'),
    path('planning/<str:room_name>/<str:username>/<str:password>', RoomPlanningView.as_view(), name='room-planning'),
]
