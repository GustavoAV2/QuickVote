from rest_framework import routers
from api.viewset import ApiViewSet

route = routers.DefaultRouter()
route.register(r'', ApiViewSet, basename="Api")
