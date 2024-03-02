import os
import io
import uuid
import boto3
from boto3 import client
from botocore.client import Config
from mongoengine import connect
from wallpapermodel import WallpaperModel
connect('artifyme', host="mongodb+srv://avbigbuddy:nZ4ATPTwJjzYnm20@cluster0.wplpkxz.mongodb.net/artifyme")


def upload_images_to_space(folder_path: str):
    spaces_access_key = 'DO009G8J4HEUMUWVJ4Q4'
    spaces_secret_key = '+w9XGrS/zvMX6Z4mIk+cMkMTh2LtBApvYb8TfBWHOqs'
    spaces_endpoint_url = 'https://work-pool.blr1.digitaloceanspaces.com'
    spaces_bucket_name = 'artifyme'

    # Create an S3 client
    s3 = client('s3',
                 
                region_name='blr1',
                endpoint_url=spaces_endpoint_url,
                aws_access_key_id=spaces_access_key,
                aws_secret_access_key=spaces_secret_key, )

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file is an image file
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            # Generate a random filename using UUID
            random_filename = str(uuid.uuid4())

            # Extract file extension from the original filename
            file_extension = os.path.splitext(filename)[1]

            # Construct the random filename with extension
            random_filename_with_extension = f"{random_filename}{file_extension}"

            # Read file content as bytes
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'rb') as file:
                file_content = file.read()

            # Upload the file to DigitalOcean Spaces
            s3.upload_fileobj(io.BytesIO(file_content), spaces_bucket_name, random_filename_with_extension, ExtraArgs={'ACL': 'public-read'})

            # Print the URL of the uploaded image
            uploaded_image_url = f"{spaces_endpoint_url}/{spaces_bucket_name}/{random_filename_with_extension}"
            wallpaerModel = WallpaperModel(tagId = "65e16aeeba4b35ed54f0c624", imagePath = uploaded_image_url, title = "Attack on titan")
            wallpaerModel.save()
            print(f"Uploaded image: {file_path} - URL: {uploaded_image_url}")

# Example usage
folder_path = "/Users/ankitsamant/avbigbuddy/wallpaperImages/pinterest-image-scrap/Attack_on_titan"
upload_images_to_space(folder_path)
