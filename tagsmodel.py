from mongoengine import Document, StringField, DateTimeField, BooleanField
from pydantic import BaseModel

class TagsModel(Document):
    tagsName = StringField(required=True)
    imagePath = StringField(required=True)
    
class TagsCreateModel(BaseModel):
    tagsName: str