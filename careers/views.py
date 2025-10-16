from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters import rest_framework as filters
from .models import Career, Comment
from .serializers import CareerSerializer, CareerUpdateSerializer, CommentSerializer


class CareerFilter(filters.FilterSet):
    """
    FilterSet for filtering posts.
    """
    username = filters.CharFilter(lookup_expr='icontains')
    title = filters.CharFilter(lookup_expr='icontains')
    created_after = filters.DateTimeFilter(field_name='created_datetime', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_datetime', lookup_expr='lte')
    
    class Meta:
        model = Career
        fields = ['username', 'title']

class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing comments on posts.
    Authorization: Only the author (username) can update or delete their comments.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def update(self, request, *args, **kwargs):
        """Only the comment author can update their comment."""
        instance = self.get_object()
        username = request.data.get('username')
        
        if not username:
            return Response(
                {"detail": "Username is required to update a comment"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if instance.username != username:
            return Response(
                {"detail": "You can only edit your own comments"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """Only the comment author can partially update their comment."""
        return self.update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Only the comment author can delete their comment."""
        instance = self.get_object()
        username = request.query_params.get('username')
        
        if not username:
            return Response(
                {"detail": "Username is required to delete a comment"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if instance.username != username:
            return Response(
                {"detail": "You can only delete your own comments"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().destroy(request, *args, **kwargs)

class CareerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing posts.
    Authorization: Only the author (username) can update or delete their posts
    """
    queryset = Career.objects.all()
    filterset_class = CareerFilter
    ordering_fields = ['created_datetime', 'title', 'username']
    ordering = ['-created_datetime']
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return CareerUpdateSerializer
        return CareerSerializer
    
    def list(self, request, *args, **kwargs):
        """
        GET /careers/
        Returns list of all posts
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """
        POST /careers/
        Create a new post with username, title, and content
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def retrieve(self, request, *args, **kwargs):
        """
        GET /careers/{id}/
        Get a specific post by ID
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        """
        PATCH /careers/{id}/
        Update title and/or content of a post
        Cannot update id, username, or created_datetime
        Only the author (username) can update their post
        """
        instance = self.get_object()
        
        # Validate that the user is the author
        username = request.data.get('username')
        if not username:
            return Response(
                {"detail": "Username is required to update a post"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if instance.username != username:
            return Response(
                {"detail": "You can only edit your own posts"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Return full object after update
        full_serializer = CareerSerializer(instance)
        return Response(full_serializer.data)
    
    def update(self, request, *args, **kwargs):
        """
        PUT /careers/{id}/
        Full update (calls partial_update since we only allow title/content updates)
        """
        return self.partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """
        DELETE /careers/{id}/
        Delete a post - returns empty response
        Only the author (username) can delete their post
        """
        instance = self.get_object()
        
        # Validate that the user is the author
        username = request.query_params.get('username')
        if not username:
            return Response(
                {"detail": "Username is required to delete a post"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if instance.username != username:
            return Response(
                {"detail": "You can only delete your own posts"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)