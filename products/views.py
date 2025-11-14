from rest_framework import viewsets, permissions
from .models import Product
from .serializers import ProductSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class ProductPermission(permissions.BasePermission):
    """
    Admin & SuperAdmin -> CRUD
    Manager -> read + update
    Staff -> read-only
    """

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if user.role in ["superadmin", "admin"]:
            return True
        if user.role == "manager" and view.action in ["list", "retrieve", "update", "partial_update"]:
            return True
        if user.role == "staff" and view.action in ["list", "retrieve"]:
            return True
        return False

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("-id")
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, ProductPermission]
    parser_classes = [MultiPartParser, FormParser]  # 🔹 handle upload file

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save()  # tetap simpan tanpa mengubah created_by
