from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import NoteViewSet, CommentViewSet  

router = DefaultRouter()
router.register(r"notess", NoteViewSet, basename="note")
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = router.urls + [
    path(
        "notess/<int:note_id>/comments/",
        CommentViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
        name="note-comments",
    ),
]