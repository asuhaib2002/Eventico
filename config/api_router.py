from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from eventico.users.api.views import UserSignupView, UserViewSet, UserLoginView, UserLogoutView
from eventico.event_manager.api.views import EventViewSet

router = DefaultRouter()

router.register("users", UserViewSet)
router.register(r'events', EventViewSet,basename = 'event')


app_name = "api"
#creating my own paths
urlpatterns = router.urls + [
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('signin/', UserLoginView.as_view(), name='user-signin'),
    path('signout/', UserLogoutView.as_view(), name='user-signout'),

]
