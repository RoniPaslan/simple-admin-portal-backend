from rest_framework import viewsets, permissions
from .models import Order
from .serializers import OrderSerializer

class OrderPermission(permissions.BasePermission):
    """
    Admin & SuperAdmin -> full CRUD
    Manager -> read-only
    Staff -> read-only (hanya order miliknya)
    """

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if user.role in ["superadmin", "admin"]:
            return True
        if user.role == "manager" and view.action in ["list", "retrieve"]:
            return True
        if user.role == "staff" and view.action in ["list", "retrieve"]:
            return True
        return False

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("-id")
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, OrderPermission]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.role == "staff":
            return qs.filter(ordered_by=user)
        return qs
