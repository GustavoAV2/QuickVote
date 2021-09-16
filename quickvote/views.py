from django.views.generic import TemplateView
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


class RoomView(TemplateView):
    template_name = 'room.html'

    def get_context_data(self, **kwargs):
        context = super(RoomView, self).get_context_data(**kwargs)

        # Removendo inseguranças do JSON
        context['room_name'] = mark_safe(self.kwargs.get('room_name'))
        context['username'] = mark_safe(self.kwargs.get('username'))

        return context
