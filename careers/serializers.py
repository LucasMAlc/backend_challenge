from rest_framework import serializers
from .models import Career, Comment

class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = ['id', 'username', 'created_datetime', 'title', 'content']
        read_only_fields = ['id', 'created_datetime']

class CareerUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = Career
        fields = ['title', 'content', 'username']
        extra_kwargs = {
            'username': {'write_only': True}
        }
    
    def update(self, instance, validated_data):
        # Remove username from validated_data as it's only for validation
        validated_data.pop('username', None)
        return super().update(instance, validated_data)
    
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'