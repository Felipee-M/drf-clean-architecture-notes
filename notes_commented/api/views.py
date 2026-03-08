from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from ..repositories.comment_repository import CommentRepository
from ..repositories.note_repository import NoteRepository
from ..domain.results import NoteAndCommentsResult
from ..commands.note_delete import NoteSoftDeleteCommand
from ..commands.note_restore import NoteRestoreCommand
from ..commands.comment_delete import CommentSoftDeleteCommand
from ..commands.comment_restore import CommentRestoreCommand
from .note_serializer import NoteSerializer
from .comment_serializer import CommentSerializer

class NoteViewSet(viewsets.ViewSet):
    note_repo = NoteRepository()
    comment_repo = CommentRepository()

    def list(self, request):
        include_deleted = request.query_params.get("include_deleted", "").lower() in(
            "yes",
            "y",
            "true",
            "t",
            "1",
        )
        all_items = self.note_repo.get_all(include_deleted=include_deleted)
        serializer = NoteSerializer(all_items, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        include_deleted = request.query_params.get("include_deleted", "").lower() in(
            "yes",
            "y",
            "true",
            "t",
            "1",
        )
        item = self.note_repo.get_by_id(int(pk))

        if item is None:
            raise NotFound()
        if item.deleted and not include_deleted:
            raise NotFound()

        out = NoteSerializer(item)
        return Response(out.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = NoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_item = self.note_repo.create(**serializer.validated_data)
        out = NoteSerializer(new_item)
        return Response(out.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        item = self.note_repo.get_by_id(int(pk))
        
        if item is None:
            raise NotFound()
        if item.deleted:
            raise NotFound()

        validating_item = NoteSerializer(item, data=request.data)
        validating_item.is_valid(raise_exception=True)
        item_to_update = self.note_repo.update(item, **validating_item.validated_data)
        out = NoteSerializer(item_to_update)
        return Response(out.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk=None):
        soft_delete_cmd = NoteSoftDeleteCommand(self.note_repo, self.comment_repo)
        obj,result = soft_delete_cmd.execute(note_id=int(pk))

        if result == NoteAndCommentsResult.NOT_FOUND:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if result == NoteAndCommentsResult.ALREADY_DELETED:
            return Response({"detail": "Already deleted."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=["post"])
    def restore(self, request, pk=None):
        restore_cmd = NoteRestoreCommand(self.note_repo, self.comment_repo)
        obj,result = restore_cmd.execute(note_id=int(pk))

        if result == NoteAndCommentsResult.NOT_FOUND:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if result == NoteAndCommentsResult.ALREADY_ACTIVE:
            return Response({"detail": "Already active."}, status=status.HTTP_400_BAD_REQUEST)
        
        out = NoteSerializer(obj)
        return Response(out.data, status=status.HTTP_200_OK)
    
class CommentViewSet(viewsets.ViewSet):
    note_repo = NoteRepository()
    comment_repo = CommentRepository()

    def list(self, request, note_id=None):
        validating_note = self.note_repo.get_by_id(int(note_id))

        if validating_note is None:
            raise NotFound()
        if validating_note.deleted:
            raise NotFound()
        
        include_deleted = request.query_params.get("include_deleted", "").lower() in(
            "yes",
            "y",
            "true",
            "t",
            "1",
        )
        all_comments = self.comment_repo.get_by_note(note_id, include_deleted=include_deleted)
        serializer = CommentSerializer(all_comments, many=True)
        return Response(serializer.data)
    
    def create(self, request, note_id=None):
        validating_note = self.note_repo.get_by_id(int(note_id))

        if validating_note is None:
            raise NotFound()
        if validating_note.deleted:
            return Response({"detail": "Note is deleted, need restore first."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_item = self.comment_repo.create(note=validating_note,**serializer.validated_data)
        out = CommentSerializer(new_item)
        return Response(out.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        item = self.comment_repo.get_by_id(int(pk))

        if item is None:
            raise NotFound()      
        if item.note.deleted:
            return Response({"detail": "Note is deleted, need restore first."}, status=status.HTTP_400_BAD_REQUEST)
        if item.deleted:
            raise NotFound()

        validating_item = CommentSerializer(item, data=request.data)
        validating_item.is_valid(raise_exception=True)
        item_to_update = self.comment_repo.update(item, **validating_item.validated_data)
        out = CommentSerializer(item_to_update)
        return Response(out.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk=None):
        item = self.comment_repo.get_by_id(int(pk))

        if item is None:
            raise NotFound() 
        if item.note.deleted:
            return Response({"detail": "Note is deleted, need restore first."}, status=status.HTTP_400_BAD_REQUEST)
        
        soft_delete_cmd = CommentSoftDeleteCommand(self.comment_repo)
        obj,result = soft_delete_cmd.execute(comment_id=int(pk))

        if result == NoteAndCommentsResult.NOT_FOUND:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if result == NoteAndCommentsResult.ALREADY_DELETED:
            return Response({"detail": "Already deleted."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=["post"])
    def restore(self, request, pk=None):
        item = self.comment_repo.get_by_id(int(pk))

        if item is None:
            raise NotFound()
        if item.note.deleted:
            return Response({"detail": "Note is deleted, need restore first."}, status=status.HTTP_400_BAD_REQUEST)
        
        restore_cmd = CommentRestoreCommand(self.comment_repo)
        obj,result = restore_cmd.execute(comment_id=int(pk))

        if result == NoteAndCommentsResult.NOT_FOUND:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if result == NoteAndCommentsResult.ALREADY_ACTIVE:
            return Response({"detail": "Already active."}, status=status.HTTP_400_BAD_REQUEST)
        
        out = CommentSerializer(obj)
        return Response(out.data, status=status.HTTP_200_OK)