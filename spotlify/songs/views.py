from django.shortcuts import render
from albums.models import Album
from .models import Song
from artists.models import Artist
from rest_framework import status
from rest_framework.parsers import JSONParser
from .serializers import SongSerializer
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
User = get_user_model()


@login_required
def song_list(request, pk, album_pk):
    user = get_object_or_404(User, pk=pk)
    if user != request.user:
        return JsonResponse({"error": "Unauthorized"}, status=401)
    album = get_object_or_404(Album, pk=album_pk)

    if request.method == "POST":
        song_data = JSONParser().parse(request)
        song_data["album"] = album.id

        song_serializer = SongSerializer(data=song_data)
        if song_serializer.is_valid():
            song_serializer.save()
            return JsonResponse(song_serializer.data)
        return JsonResponse(song_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        songs = Song.objects.filter(album=album)
        serializer = SongSerializer(songs, many=True)
        return JsonResponse(serializer.data, safe=False)


@login_required
def song_delete(request, pk, album_pk, song_pk):
    user = get_object_or_404(User, pk=pk)
    if user != request.user:
        return JsonResponse({"error": "Unauthorized"}, status=401)
    album = get_object_or_404(Album, pk=album_pk)
    song = get_object_or_404(Song, id=song_pk)

    if request.method == "DELETE":
        if song.album != album:
            return JsonResponse(
                {"error": "Song does not belong to specified album."}, status=404
            )

        song.delete()
        return JsonResponse({"message": "Song deleted successfully"})
