from ..models import Note

class NoteRepository:
    def get_all(self, include_deleted: bool=False):
        qs = Note.objects.all()
        return qs if include_deleted else qs.filter(deleted=False)
    
    def get_by_id(self, id):
        try:
            return Note.objects.get(id=id)
        except Note.DoesNotExist:
            return None
        
    def create(self, **data):
        return Note.objects.create(**data)
    
    def update(self, note: Note, **data):
        for key,value in data.items():
            setattr(note, key, value)
        note.save()
        return note
    
    def soft_delete(self, note:Note):
        note.deleted = True
        note.save(update_fields=["deleted"])
        return note
    
    def restore(self, note:Note):
        note.deleted = False
        note.save(update_fields=["deleted"])
        return note