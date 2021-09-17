# /urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from quickvote.views import RoomView, IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('<str:room_name>/<str:username>/', RoomView.as_view(), name='room'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
