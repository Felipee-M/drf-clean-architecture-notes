from ..domain.results import NoteAndCommentsResult
from ..repositories.comment_repository import CommentRepository

class CommentRestoreCommand:
    def __init__(self, repo: CommentRepository):
        self.repo = repo

    def execute(self, *, comment_id: int):
        item = self.repo.get_by_id(comment_id)

        if item is None:
            return None, NoteAndCommentsResult.NOT_FOUND
        
        if not item.deleted:
            return item, NoteAndCommentsResult.ALREADY_ACTIVE
        
        out = self.repo.restore(item)
        return out, NoteAndCommentsResult.RESTORED