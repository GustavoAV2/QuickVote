from django.views.generic import TemplateView
from django.utils.safestring import mark_safe


class IndexView(TemplateView):
    template_name = 'index.html'


class RoomView(TemplateView):
    template_name = 'chat.html'

    def get_context_data(self, **kwargs):
        context = super(RoomView, self).get_context_data(**kwargs)

        # Removendo inseguranças do JSON
        context['room_name'] = mark_safe(
            self.kwargs.get('room_name')
        )
        return context
