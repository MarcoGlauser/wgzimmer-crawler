from rest_framework import routers

from room.views import RoomViewSet

router = routers.SimpleRouter()
router.register(r'rooms', RoomViewSet)
urlpatterns = router.urls
