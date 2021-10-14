from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from quickvote import actions


class ApiViewSet(ModelViewSet):

    def update(self, request, *args, **kwargs):
        ...

    def list(self, request, *args, **kwargs):
        json = request.GET

        if json.get('room'):
            room = actions.scenery.get_room_by_room_name(json.get('room', ''))
            if room:
                if actions.login(room.room, json.get('password', '')):
                    return Response(room.advanced_serialize())
                return Response(room.serialize_protected())
            return Response()

        return Response(actions.scenery.serialize())

    def create(self, request, *args, **kwargs):
        json = request.data

        if not actions.scenery.if_room_exists(json.get('room')):
            if json.get('type') == 'objects':
                room = actions.create_room_for_objects(json.get('room'), json.get('theme'),
                                                       password=json.get('password'), objects=json.get('objects'))
            else:
                room = actions.create_room_for_users(json.get('room'), json.get('theme'), password=json.get('password'))
            return Response(room.advanced_serialize(), status=200)

        return Response(status=404)
