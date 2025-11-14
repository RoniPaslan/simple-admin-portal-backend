# invitations/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvitationViewSet, InvitationDetailPublicView

# 🔹 Router untuk CRUD + action (resend/revoke)
router = DefaultRouter()
router.register("invitations", InvitationViewSet, basename="invitation")

urlpatterns = [
    # 🔹 Semua endpoint CRUD + action
    path("", include(router.urls)),

    # 🔹 Endpoint public untuk cek token invitation tanpa login
    path("invitations/public/<uuid:token>/", InvitationDetailPublicView.as_view(), name="invitation-public"),
]
