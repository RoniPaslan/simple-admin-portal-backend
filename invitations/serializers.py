# invitations/serializers.py
from rest_framework import serializers
from .models import Invitation

class InvitationSerializer(serializers.ModelSerializer):
    expired = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Invitation
        fields = [
            "id",
            "email",
            "role",
            "token",
            "created_at",
            "used",
            "expired_at",
            "expired",
            "invited_by",
        ]
        read_only_fields = ["id", "token", "created_at", "used", "expired", "invited_by"]

    def get_expired(self, obj):
        return obj.is_expired()
