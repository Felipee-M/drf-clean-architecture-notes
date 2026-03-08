from rest_framework import serializers
from ..models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "note",
            "text",
            "deleted",
            "created_at",
            "updated_at",
        ]

        read_only_fields = ["id", "note", "created_at", "updated_at"]