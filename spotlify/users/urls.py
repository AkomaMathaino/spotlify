from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("api/register/", user_views.register, name="register"),
    path("api/login/", user_views.login_user, name="login"),
    path("api/logout/", user_views.logout_user, name="logout"),
    path("api/user/<int:pk>/", user_views.get_user_info, name="user_info"),
    path("api/user/<int:pk>/update", user_views.update_user_info, name="update_info"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
