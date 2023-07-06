from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from contacts.views import ContactView
from authn.views import (
    LogoutView,
    LoginAPI,
    RegisterAPI,
    EmailLoginAPI,
)
from tasks.views import TaskView, UserViewSet


router = routers.DefaultRouter()
router.register(r"tasks", TaskView, basename="task")
router.register(r"contacts", ContactView, basename="contact")
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("register/", RegisterAPI.as_view(), name="register"),
    path("login/", EmailLoginAPI.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('reset-password/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
