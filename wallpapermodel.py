from mongoengine import Document,  StringField, IntField, ListField
from pydantic import BaseModel

class WallpaperModel(Document):
    tagId = StringField(required=True)
    imagePath = StringField(required=True)
    downloadsCount = IntField(default= 0, required=False)
    like = ListField(required=False)

class WallpaperModelAdd(BaseModel):
    tagId: str


class WallPaperModelupdatelike(BaseModel):
    userId: str


class WallpaperDownloadCount(BaseModel):
    downloadsCount: str