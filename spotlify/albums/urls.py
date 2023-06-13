from django.urls import path
from albums import views as album_views
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path("", album_views.index.as_view()),
    path(
        "api/albums/<int:pk>/", csrf_exempt(album_views.album_list), name="album_list"
    ),
    path(
        "api/albums/<int:pk>/<int:album_pk>/",
        csrf_exempt(album_views.album_delete),
        name="album_delete",
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
