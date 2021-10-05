from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from core.settings import API_URL, CHAT_SOCKET_URL, ROOM_SOCKET_URL


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['api_url'] = API_URL
        return context


class RoomView(TemplateView):
    template_name = 'room.html'

    def get_context_data(self, **kwargs):
        context = super(RoomView, self).get_context_data(**kwargs)
        context['room_name'] = mark_safe(self.kwargs.get('room_name'))
        context['username'] = mark_safe(self.kwargs.get('username'))
        context['url_socket_room'] = ROOM_SOCKET_URL
        context['url_socket_chat'] = CHAT_SOCKET_URL
        return context
