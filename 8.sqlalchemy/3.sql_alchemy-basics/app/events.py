from sqlalchemy import event
from sqlalchemy.orm import Mapper
from datetime import datetime
from .database import BaseModel


def _set_created_at(mapper, connection, target):  # the _ means this function is private to this module
    if hasattr(target, 'created_at') and getattr(target, 'created_at') is None:
        target.created_at = datetime.now()

def _set_updated_at(mapper, connection, target):  # the _ means this function is private to this module
    if hasattr(target, 'updated_at'):
        target.updated_at = datetime.now()


def get_all_subclass(cls):
    for subclass in cls.__subclasses__():
        yield subclass
        yield from get_all_subclass(subclass)


for cls in get_all_subclass(BaseModel):
    event.listen(cls, 'before_insert', _set_created_at)
    event.listen(cls, 'before_update', _set_updated_at)