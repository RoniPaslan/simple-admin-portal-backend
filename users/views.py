from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer, RegisterSerializer

class RolePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        # Semua bisa akses 'me'
        if view.action == "me":
            return True

        # Superadmin bisa semua
        if user.role == "superadmin":
            return True

        # Admin bisa list, retrieve, destroy
        if user.role == "admin":
            if view.action in ["list", "retrieve", "destroy"]:
                return True

        # Manager hanya bisa lihat list/retrieve
        if user.role == "manager" and view.action in ["list", "retrieve"]:
            return True

        # Staff hanya bisa lihat dirinya sendiri
        if user.role == "staff" and view.action == "me":
            return True

        return False


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, RolePermission]

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            self.perform_destroy(user)
            return Response(
                {"detail": f"User {user.username} berhasil dihapus."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"detail": str(e) or "Gagal menghapus user."},
                status=status.HTTP_400_BAD_REQUEST
            )


class RegisterView(APIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]  # Bisa diakses tanpa login

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Registrasi berhasil!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
