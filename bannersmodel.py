from mongoengine import Document, StringField
from pydantic import BaseModel

class BannerModel(Document):
    tagID = StringField(required=True)
    bannerImage =StringField(required=True)
    title = StringField(required=True)


class BannerJson(BaseModel):
    tagID: str
    bannerImage: str
    title: str