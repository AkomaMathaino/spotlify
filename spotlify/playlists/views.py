from django.shortcuts import render
from .models import Playlist
from songs.models import Song
from rest_framework import status
from rest_framework.parsers import JSONParser
from .serializers import PlaylistSerializer
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


# Create your views here.
User = get_user_model()


@login_required
def playlist_list(request, pk):
    user = get_object_or_404(User, pk=pk)

    if user != request.user:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    if request.method == "POST":
        playlist_data = JSONParser().parse(request)
        playlist_data["user"] = user.id

        playlist_serializer = PlaylistSerializer(data=playlist_data)
        if playlist_serializer.is_valid():
            playlist_serializer.save(user=user)
            return JsonResponse(playlist_serializer.data)
        return JsonResponse(
            playlist_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    if request.method == "GET":
        playlists = Playlist.objects.filter(user=user)
        serializer = PlaylistSerializer(playlists, many=True)
        return JsonResponse(serializer.data, safe=False)


@login_required
def playlist_specific(request, pk, playlist_pk):
    user = get_object_or_404(User, pk=pk)

    if user != request.user:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    playlist = get_object_or_404(Playlist, pk=playlist_pk)

    if request.method == "GET":
        serializer = PlaylistSerializer(playlist)
        return JsonResponse(serializer.data, safe=True)

    if request.method == "DELETE":
        playlist.delete()
        return JsonResponse({"message": "Playlist deleted successfully"})

    if request.method == "PATCH":
        song_ids = JSONParser().parse(request)

        if song_ids["songs"] is not None:
            for song_id in song_ids["songs"]:
                song = get_object_or_404(Song, pk=song_id)
                playlist.songs.add(song.pk)

        playlist_dict = {
            "id": playlist.id,
            "title": playlist.title,
            "user": playlist.user.id,
            "songs": [song.id for song in playlist.songs.all()],
        }
        playlist_serializer = PlaylistSerializer(data=playlist_dict)

        if playlist_serializer.is_valid():
            playlist_serializer.save()
            return JsonResponse(playlist_serializer.data, safe=True)
        return JsonResponse(
            playlist_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


@login_required
def playlist_song_delete(request, pk, playlist_pk, song_pk):
    user = get_object_or_404(User, pk=pk)
    if user != request.user:
        return JsonResponse({"error": "Unauthorized"}, status=401)
    playlist = get_object_or_404(Playlist, pk=playlist_pk)
    song = get_object_or_404(Song, pk=song_pk)

    if request.method == "PATCH":
        playlist.songs.remove(song.pk)
        playlist.save()

        return JsonResponse({"message": "Song deleted from playlist"})
