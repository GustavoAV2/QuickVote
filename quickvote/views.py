from ratelimit import limits
from quickvote import actions
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from core.settings import API_URL, CHAT_SOCKET_URL, ROOM_SOCKET_URL


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['api_url'] = API_URL
        return context

    @limits(calls=15, period=60)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class FastLogin(TemplateView):
    template_name = 'fast_login.html'

    def get_context_data(self, **kwargs):
        context = super(FastLogin, self).get_context_data(**kwargs)
        context['api_url'] = API_URL
        return context

    @limits(calls=15, period=60)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class RoomView(TemplateView):
    template_name = 'room.html'

    def get_context_data(self, **kwargs):
        context = super(RoomView, self).get_context_data(**kwargs)
        context['room_name'] = mark_safe(self.kwargs.get('room_name'))
        context['username'] = mark_safe(self.kwargs.get('username'))
        context['url_socket_room'] = ROOM_SOCKET_URL
        context['url_socket_chat'] = CHAT_SOCKET_URL
        context['tutorial'] = """
        \tSeja bem vindo!\n
        \t* Quando estiver preparado para a votação clique no botão 'Pronto'!\n
        \t* Após a votação começar, clique em qualquer item a direita para votar nele.
        """
        return context

    @limits(calls=6, period=60)
    def get(self, request, *args, **kwargs):
        room_name = mark_safe(self.kwargs.get('room_name'))
        username = mark_safe(self.kwargs.get('username'))
        password = mark_safe(self.kwargs.get('password'))

        if room_name and username:
            room = actions.scenery.get_room_by_room_name(room_name)
            if room:
                if actions.login(room_name, password):
                    if not room.get_user_by_name(username):
                        context = self.get_context_data(**kwargs)
                        return self.render_to_response(context)
                    else:
                        return redirect('fast-login', room_name=room_name, password=password)
                return redirect('home')
        return redirect('home')
