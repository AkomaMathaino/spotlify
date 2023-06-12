from django.urls import path
from songs import views as song_views
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path(
        "api/songs/<int:pk>/<int:album_pk>/",
        csrf_exempt(song_views.song_list),
        name="song_list",
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
