from enum import Enum

class NoteAndCommentsResult(str, Enum):
    NOT_FOUND = "not_found"
    ALREADY_DELETED = "already_deleted"
    DELETED = "deleted"
    ALREADY_ACTIVE = "already_active"
    RESTORED = "restored"