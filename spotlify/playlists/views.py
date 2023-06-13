from django.shortcuts import render
from .models import Playlist
from artists.models import Artist
from rest_framework import status
from rest_framework.parsers import JSONParser
from .serializers import PlaylistSerializer
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
def playlist_list(request, pk):
    user = get_object_or_404(User, pk=pk)

    if user != request.user:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    if request.method == "POST":
        playlist_data = JSONParser().parse(request)

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
        return JsonResponse(serializer.data, safe=True)


@login_required
def playlist_specific(request, pk, playlist_pk):
    user = get_object_or_404(User, pk=pk)

    if user != request.user:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    playlist = get_object_or_404(Playlist, playlist_pk)

    if request.method == "GET":
        serializer = PlaylistSerializer(playlist)
        return JsonResponse(serializer.data, safe=True)

    if request.method == "DELETE":
        playlist.delete()
        return JsonResponse({"message": "Playlist deleted successfully"})
