# invitations/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Invitation
from .serializers import InvitationSerializer
from django.core.mail import send_mail
from django.conf import settings

# 🔹 Permission untuk Admin/Manager
class InvitationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Superadmin, Admin, Manager bisa membuat dan kelola invitation
        return request.user.is_authenticated and request.user.role in ["superadmin", "admin", "manager"]

# 🔹 ViewSet utama untuk CRUD invitation
class InvitationViewSet(viewsets.ModelViewSet):
    queryset = Invitation.objects.all().order_by("-created_at")
    serializer_class = InvitationSerializer
    permission_classes = [InvitationPermission]

    # 🔹 Create invitation
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invitation = serializer.save(invited_by=request.user)

        invite_url = f"http://localhost:3000/register?token={invitation.token}"
        send_mail(
            subject="Undangan Bergabung ke Portal",
            message=f"Anda diundang untuk bergabung ke Portal. Klik link ini: {invite_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[invitation.email],
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # 🔹 Resend email tanpa mengubah token atau used
    @action(detail=True, methods=["POST"])
    def resend(self, request, pk=None):
        invitation = self.get_object()
        if invitation.used:
            return Response({"detail": "Token sudah digunakan, tidak bisa di-resend"}, status=status.HTTP_400_BAD_REQUEST)
        if invitation.is_expired():
            return Response({"detail": "Token sudah kadaluarsa, buat undangan baru"}, status=status.HTTP_400_BAD_REQUEST)

        invite_url = f"http://localhost:3000/register?token={invitation.token}"
        send_mail(
            subject="Undangan Bergabung ke Portal (Resend)",
            message=f"Anda diundang untuk bergabung ke Portal. Klik link ini: {invite_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[invitation.email],
        )
        return Response({"detail": "Email undangan berhasil dikirim ulang"}, status=status.HTTP_200_OK)

    # 🔹 Revoke invitation
    @action(detail=True, methods=["POST"])
    def revoke(self, request, pk=None):
        invitation = self.get_object()

        # Hanya superadmin bisa hapus apapun
        if request.user.role == "superadmin":
            invitation.delete()
            return Response({"detail": "Undangan berhasil dicabut."}, status=status.HTTP_200_OK)
        
        # Admin/Manager tidak bisa hapus jika sudah digunakan
        if invitation.used:
            return Response(
                {"detail": "Token sudah digunakan, tidak bisa dicabut oleh Anda"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        invitation.delete()
        return Response({"detail": "Undangan berhasil dicabut."}, status=status.HTTP_200_OK)


# 🔹 Endpoint public untuk cek token invitation tanpa login
class InvitationDetailPublicView(APIView):
    permission_classes = []  # bebas tanpa authentication

    def get(self, request, token):
        try:
            invite = Invitation.objects.get(token=token)
            if invite.is_expired():
                return Response({"detail": "Undangan telah kadaluarsa."}, status=status.HTTP_400_BAD_REQUEST)
            if invite.used:
                return Response({"detail": "Undangan sudah digunakan."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = InvitationSerializer(invite)
            return Response(serializer.data)
        except Invitation.DoesNotExist:
            return Response({"detail": "Undangan tidak ditemukan."}, status=status.HTTP_404_NOT_FOUND)
