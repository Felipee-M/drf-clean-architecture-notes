from ..models import Comment

class CommentRepository:
    
    def get_by_id(self, id):
        try:
            return Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            return None
        
    def get_by_note(self, note_id, include_deleted: bool=False):
        qs = Comment.objects.filter(note_id=note_id)
        return qs if include_deleted else qs.filter(deleted=False)
            
    def create(self, **data):
        return Comment.objects.create(**data)
    
    def update(self, comment: Comment, **data):
        for key,value in data.items():
            setattr(comment, key, value)
        comment.save()
        return comment
    
    def soft_delete(self, comment:Comment):
        comment.deleted = True
        comment.save(update_fields=["deleted"])
        return comment
    
    def restore(self, comment:Comment):
        comment.deleted = False
        comment.save(update_fields=["deleted"])
        return comment