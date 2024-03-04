from fastapi import FastAPI, File, UploadFile
from mongoengine import connect
from usermodel import UserCreate, UserLogin, UserLoginId, UserModel, UserCreateById
from tagsmodel import TagsModel, TagsCreateModel
from bannersmodel import BannerModel, BannerJson
from wallpapermodel import WallpaperModel, WallpaperModelAdd, WallPaperModelupdatelike
import io
import os
import uuid
import random
from boto3 import client
from typing import List
import json
from bson import ObjectId
from math import ceil


app = FastAPI()
connect('artifyme', host="mongodb+srv://avbigbuddy:nZ4ATPTwJjzYnm20@cluster0.wplpkxz.mongodb.net/artifyme")


def upload_image_to_space(file_content: bytes, filename: str):
    spaces_access_key = 'DO009G8J4HEUMUWVJ4Q4'
    spaces_secret_key = '+w9XGrS/zvMX6Z4mIk+cMkMTh2LtBApvYb8TfBWHOqs'
    spaces_endpoint_url = 'https://work-pool.blr1.digitaloceanspaces.com'
    spaces_bucket_name = 'artifyme'

    # Generate a random filename using UUID
    # Generate a random filename using UUID
    random_filename = str(uuid.uuid4())
    file_extension = os.path.splitext(filename)[1]  # Extract file extension from the original filename

    random_filename_with_extension = f"{random_filename}{file_extension}"

    s3 = client('s3',
                 
                region_name='blr1',
                endpoint_url=spaces_endpoint_url,
                aws_access_key_id=spaces_access_key,
                aws_secret_access_key=spaces_secret_key, )

    # Create a BytesIO object to read file content from memory
    file_content_stream = io.BytesIO(file_content)

    s3.upload_fileobj(file_content_stream, spaces_bucket_name, random_filename_with_extension,  ExtraArgs={'ACL': 'public-read'})

    return f"{spaces_endpoint_url}/{spaces_bucket_name}/{random_filename_with_extension}"



@app.get("/api/v1/user-list")
async def userList():
    user = UserModel.objects.all()
    tojson = user.to_json()
    fromjson = json.loads(tojson)
    return {
        "message": "User List",
        "data":fromjson,
        "status":True
    }
    
@app.post("/api/v1/user-create")
async def userCreate(userJson: UserCreate):
    findUser = UserModel.objects(email=userJson.email).first()
    if(findUser):
        return {
            "message":"User already have",
            "data":None,
            "status":False
        }
    user = UserModel(name = userJson.name, email=userJson.email, gender=userJson.gender, password=userJson.password)
    user.save()
    tojson = user.to_json()
    fromjson = json.loads(tojson)
    return {
        "message":"User Create Succes",
        "data":fromjson,
        "status":True
    }
    
@app.post("/api/v1/user-create-by-id")
async def userCreateByid(data: UserCreateById):
    findUser = UserModel.objects(en_login_id=data.en_login_id).first()
    if(findUser):
        return {
            "message":"User already have",
            "data":None,
            "status":False
        }
    user = UserModel(en_login_id = data.en_login_id ,name = data.name, email=data.email, gender=data.gender, password=data.password)
    user.save()
    tojson = user.to_json()
    fromjson = json.loads(tojson)
    return {
        "message":"User Create Succes",
        "data":fromjson,
        "status":True
    }
    
@app.post("/api/v1/user-login")
async def userLogin(userJson: UserLogin):
    finduser = UserModel.objects(email=userJson.email).first()
    if(finduser):
        if(finduser.password == userJson.password):
            tojson = finduser.to_json()
            fromjson = json.loads(tojson)
            return {
                "message":"Login Success",
                "data":fromjson,
                "status":True
            }
        else:
            return {
                "message":"Password not match",
                "data":None,
                "status": False
            }
    else:
        {
            "message":"User not found",
            "data":None,
            "status": False
        }
        
        
@app.post("/api/v1/user-login-by-id")
async def userLoginbyGoogle(userjson: UserLoginId):
    finduser = UserModel.objects(en_login_id=userjson.en_login_id).first()
    if(finduser):
        tojson = finduser.to_json()
        fromjson = json.loads(tojson)
        return {
            "messsage": "user login succes",
            "data": fromjson,
            "status":True        
        }      
        
        
@app.put("/api/v1/tags-create/{tagName}")
async def tagsUserCreate(tagName: str, file: UploadFile = File(...)):
    findtags = TagsModel.objects(tagsName = tagName).first()
    if(findtags):
        
        return {
            "message":"Tag Aleready",
            "data": None,
            "statu": False
        }  
    else:
        file_content = await file.read()
        uploaded_path = upload_image_to_space(file_content, file.filename)
        tags = TagsModel(tagsName = tagName, imagePath = uploaded_path )
        tags.save()
        tojson = tags.to_json()
        fromjson = json.loads(tojson)
        return {
            "message":"Tags creted",
            "data": fromjson,
            "statu": True
        }
        
@app.get("/api/v1/tags-get")
async def tagsGet():
    finduser = TagsModel.objects.all()
    tojson = finduser.to_json()
    fromjson = json.loads(tojson)
    return {
        "data": fromjson
    }

@app.get("/api/v1/tags/search/{query}")
async def search(query: str):
    # Query TagsModel collection
    results = TagsModel.objects(tagsName__icontains=query).limit(10)
    if not results:
        raise {
            "message":"Tags not found",
            "data":None,
            "status":True
        }
    tojson = results.to_json()
    fromjson = json.loads(tojson)
    return {
            "message":"Tags not found",
            "data":fromjson,
            "status":True
        }

@app.get("/api/v1/get-banners")
async def bannerList():
    data = BannerModel.objects.all()
    tojson = data.to_json()
    fromjson = json.loads(tojson)
    return {
        "data":fromjson,
        "status": True
    }
    
@app.post("/api/v1/upload-image")
async def uploadimage(file: UploadFile = File(...)):
    file_content = await file.read()
    
    # Call the upload function with the random filename and the original file extension
    uploaded_path = upload_image_to_space(file_content, file.filename)
    return {"path": uploaded_path}
    
@app.post("/api/v1/create-banners")
async def createBanners(body: BannerJson):
    banner = BannerModel(tagID=body.tagID, bannerImage = body.bannerImage, title = body.title)
    banner.save()
    return {
        "message": "new banner update",
        "status": True
    }

@app.put("/api/v1/upload-wallpapers/{tagid}")
async def uploadWallpapers(tagid: str, files: List[UploadFile] = File(...)):
    uploaded_paths = []
    for file in files:
        # Read file content into memory
        file_content = await file.read()
        
        # Call the upload function with the random filename and the original file extension
        uploaded_path = upload_image_to_space(file_content, file.filename)
        uploaded_paths.append(uploaded_path)
        addWallpaper = WallpaperModel(tagId= tagid, imagePath=uploaded_path)
        addWallpaper.save()
    wallpaperList = WallpaperModel.objects(tagId=tagid).first()
    tojson = wallpaperList.to_json()
    fromjson = json.loads(tojson)
    return {
        "message": "New Wallpaper added",
        "data":fromjson,
        "status":True
    }
    
@app.get("/api/v1/get-wallpapers/tagsid/{tagid}")
async def wallpapersByTagsId(tagid: str):
    wallpaperList = WallpaperModel.objects(tagId=tagid)
    data_list = list(wallpaperList)
    random.shuffle(data_list)
    data_json = json.loads(json.dumps([obj.to_mongo().to_dict() for obj in data_list], default=str))
    
    if(wallpaperList):
        return {
        "message": "Wallpapers by Tag id",
        "data":data_json,
        "status":True
        }
    else:
        return {
        "message": "wallpapers not found",
        "data":None,
        "status":False
    }

@app.get("/api/v1/wallpaper-by-tags/random/{tag_id}")
async def pick_random_row(tag_id: str):
    # Query WallpaperModel collection
    results = WallpaperModel.objects(tagId=tag_id)
    if not results:
        raise {
            "message":"Wallpaer not found on this tag",
            "data":None,
            "status":False
        }
    
    # Pick a random result
    random_result = random.choice(results)
    tojson = json.loads(random_result)
    fromjson = json.loads(tojson)
    return {
            "message":"Wallpaer not found on this tag",
            "data":fromjson,
            "status":False
        }
    
@app.get("/api/v1/get-all-wallpapers")
async def allWallpapers():
    wallpaperList = WallpaperModel.objects.all()
    tojson = wallpaperList.to_json()
    fromjson = json.loads(tojson)
    return {
        "message": "ALl Wallpaper List",
        "data":fromjson,
        "status":True
    }
    

@app.put("/api/v1/wallpaper-like-update/{wallpaperid}")
async def updateLikeWallpaper(body: WallPaperModelupdatelike, wallpaperid: str):
    findWallpaper = WallpaperModel.objects.get(id=ObjectId(wallpaperid))
    if findWallpaper :
        likesId = findWallpaper.like
        for like in likesId:
            if like == body.userId:
                return {
                    "Message": "already added",
                    "status": True
                }
                break
        likesId.append(body.userId)
        findWallpaper.like = likesId
        findWallpaper.save()
        return {
            "message": "Like Update",
            "status":True
        }
                 



@app.put("/api/v1/wallpaper-update-download/{wallpaperid}")
async def wallpaperUpdateDownload(wallpaperid: str):
    findWallpaper = WallpaperModel.objects.get(id=ObjectId(wallpaperid))
    if findWallpaper :
        findWallpaper.downloadsCount = findWallpaper.downloadsCount+1
        findWallpaper.save()
        return {
            "message":"Download count update",
            "count": findWallpaper.downloadsCount,
            "status":True
        }
    else:
         return {
            "message":"Something went wrong",
            "count":None,
            "status":False
        }

@app.get("/api/v1/perticular-wallpaper-by-id/{wallpaperid}")
async def perticularWallpaperData(wallpaperid: str):
    findWallpaper = WallpaperModel.objects.get(id=ObjectId(wallpaperid))
    if findWallpaper :
        tojson = findWallpaper.to_json()
        fromjson = json.loads(tojson)
        return{
            "message":"Wallpaper data",
            "data": fromjson,
            "status":True
        }
    else:
        return{
            "message":"Wallpaper not found",
            "data": None,
            "status":False
        }
        



@app.delete("/api/v1/delete-tag/{id}")
async def deleteTag(id: str):
    TagsModel.objects(id=ObjectId(id)).delete()
    return {
        'message':"tag Deleted",
        "status":True
    }

@app.get("/api/v1/search-wallpaper/{keyword}/{page}/{page_size}")
async def search_wallpaper(keyword: str = None, page: int = 1, page_size: int = 10):
    # Query all data matching the keyword
    all_data = WallpaperModel.objects(title__icontains=keyword)

    if not all_data:
        return {
            "message": "Wallpapers not found",
            "data": None,
            "status": False
        }
    else:
        # Convert queryset to a list
        data_list = list(all_data)

        # Shuffle the list
        random.shuffle(data_list)

        # Calculate total count of wallpapers matching the keyword
        total_count = len(data_list)

        # Calculate total pages
        total_pages = ceil(total_count / page_size)

        # Calculate skip value for pagination
        skip = (page - 1) * page_size

        # Get the data for the current page
        data_for_page = data_list[skip: skip + page_size]

        # Convert the data to JSON, converting ObjectId to string
        data_json = json.loads(json.dumps([obj.to_mongo().to_dict() for obj in data_for_page], default=str))

        return {
            "message": "Here are the shuffled wallpapers with pagination",
            "data": data_json,
            "status": True,
            "page": page,
            "total_pages": total_pages,
            "total_count": total_count
        }
