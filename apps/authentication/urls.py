from rest_framework import routers

from apps.authentication.views.auth import AuthViewSet

router = routers.DefaultRouter()
router.register(r"user", AuthViewSet, basename="user")
# router.register(r'user', UserViewSet, basename='user')

router.urlpatterns = router.urls
