from ..domain.results import NoteAndCommentsResult
from ..repositories.note_repository import NoteRepository
from ..repositories.comment_repository import CommentRepository

class NoteRestoreCommand:
    def __init__(self, note_repo: NoteRepository, comment_repo: CommentRepository):
        self.note_repo = note_repo
        self.comment_repo = comment_repo

    def execute(self, *, note_id: int):
        item = self.note_repo.get_by_id(note_id)

        if item is None:
            return None, NoteAndCommentsResult.NOT_FOUND
        
        if not item.deleted:
            return item, NoteAndCommentsResult.ALREADY_ACTIVE
        
        out = self.comment_repo.restore(item)
        relateds = self.comment_repo.get_by_note(note_id, include_deleted=True)

        for comment in relateds:
            if comment.deleted:
                self.comment_repo.restore(comment)

        return out, NoteAndCommentsResult.RESTORED