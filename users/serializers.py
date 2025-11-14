from rest_framework import serializers
from .models import User
from invitations.models import Invitation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "is_active"]
        read_only_fields = ["id", "is_active"]

class RegisterSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=6)


    def validate_token(self, value):
        try:
            invitation = Invitation.objects.get(token=value)
        except Invitation.DoesNotExist:
            raise serializers.ValidationError("Token undangan tidak valid.")
        
        if invitation.used:
            raise serializers.ValidationError("Token undangan sudah digunakan.")
        if invitation.is_expired():
            raise serializers.ValidationError("Token undangan sudah kadaluarsa.")
        
        self.invitation = invitation
        return value

    def create(self, validated_data):
        invitation = self.invitation
        user = User.objects.create_user(
            username=validated_data["username"],  # ambil dari input user
            email=invitation.email,
            password=validated_data["password"],
            role=invitation.role,
        )
        invitation.used = True
        invitation.save()
        return user
