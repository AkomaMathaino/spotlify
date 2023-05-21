from django.shortcuts import render
from .models import Album
from artists.models import Artist
from rest_framework import status
from rest_framework.parsers import JSONParser
from .serializers import AlbumSerializer
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
User = get_user_model()


class index(APIView):
    def get(self, request):
        queryset = Album.objects.all()
        return Response({"album": queryset})


@login_required
def album_list(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user != request.user:
        return JsonResponse({"error": "Unauthorized"}, status=401)
    artist = get_object_or_404(Artist, user=user.id)

    if request.method == "POST":
        album_data = JSONParser().parse(request)
        album_data["primary_artist"] = artist.id

        collaborator_names = album_data.pop("collaborators", [])
        collaborators = Artist.objects.filter(name__in=collaborator_names)

        if len(collaborators) != len(collaborator_names):
            return JsonResponse(
                {"error": "Invalid collaborators"}, status=status.HTTP_400_BAD_REQUEST
            )

        album_serializer = AlbumSerializer(data=album_data)
        if album_serializer.is_valid():
            album = album_serializer.save(primary_artist=artist)
            album.collaborators.set(collaborators)
            return JsonResponse(album_serializer.data)
        return JsonResponse(album_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        albums = Album.objects.filter(primary_artist=artist)
        serializer = AlbumSerializer(albums, many=True)
        return JsonResponse(serializer.data, safe=False)
