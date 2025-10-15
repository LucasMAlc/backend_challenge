from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_datetime')
    serializer_class = PostSerializer


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        username = request.query_params.get('username')
        if instance.username != username:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)

