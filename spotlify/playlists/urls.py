from django.urls import path
from playlists import views as playlist_views
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path(
        "api/playlists/<int:pk>/",
        csrf_exempt(playlist_views.playlist_list),
        name="playlist_list",
    ),
    path(
        "api/playlists/<int:pk>/<int:playlist_pk>/",
        csrf_exempt(playlist_views.playlist_specific),
        name="playlist_specific",
    ),
    path(
        "api/playlists/<int:pk>/<int:playlist_pk>/songs/<int:song_pk>/",
        csrf_exempt(playlist_views.playlist_song_delete),
        name="playlist_song_delete",
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
