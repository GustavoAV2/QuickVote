import json as js
from ratelimit import limits
from quickvote import actions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from quickvote.models.room import Room, RoomObjects, RoomPlanning


class ApiViewSet(ModelViewSet):

    def update(self, request, *args, **kwargs):
        ...

    @limits(calls=30, period=60)
    def list(self, request, *args, **kwargs):
        json = request.GET

        if json.get('room'):
            room = actions.scenery.get_room_by_room_name(json.get('room', ''))
            if room:
                if actions.login(room.room_name, json.get('password', '')):
                    return Response(room.advanced_serialize(),
                                    headers={'Access-Control-Allow-Origin': '*'})
                return Response(room.serialize_protected(), headers={'Access-Control-Allow-Origin': '*'})
            return Response(headers={'Access-Control-Allow-Origin': '*'})

        return Response(actions.scenery.serialize(), headers={'Access-Control-Allow-Origin': '*'})

    @limits(calls=30, period=60)
    def create(self, request, *args, **kwargs):
        json = request.data.dict()
        j = str(json)
        j = j.replace("': ''}", "").replace("{'", "")
        json = js.loads(j)

        if not actions.scenery.if_room_exists(json.get('room')):
            if json.get('type') == 'planning':
                room = actions.create_room_for_objects(json.get('room'), json.get('theme'),
                                                       password=json.get('password'), objects=json.get('objects'),
                                                       room_obj=RoomPlanning)
            elif json.get('type') == 'objects':
                room = actions.create_room_for_objects(json.get('room'), json.get('theme'),
                                                       password=json.get('password'), objects=json.get('objects'),
                                                       room_obj=RoomObjects)
            else:
                room = actions.create_room_for_users(json.get('room'), json.get('theme'), password=json.get('password'))
            return Response(room.advanced_serialize(), status=200,
                            headers={'Access-Control-Allow-Origin': '*'})

        return Response(status=404, headers={'Access-Control-Allow-Origin': '*'})
