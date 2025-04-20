import pymongo
import gridfs
import os

uri = os.getenv("MONGO_URI")
# Connect to MongoDB Atlas
client = pymongo.MongoClient(uri)

# Select Database and Collection
db = client["student_detail"]
fs = gridfs.GridFS(db)  # GridFS for storing large files

def upload_images_from_folder(folder_path):
    """Uploads all images from a folder to MongoDB GridFS."""
    student_collection = db["student_data"]

    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):  # Only process images
            image_path = os.path.join(folder_path, filename)
            
            # Extract student name from filename (without extension)
            student_name = os.path.splitext(filename)[0]  
            
            with open(image_path, "rb") as img_file:
                image_id = fs.put(img_file, filename=filename)
            
            # Store metadata in student_data collection
            student_collection.insert_one({"name": student_name, "Image": image_id})
            
            print(f"Uploaded {filename} with ID: {image_id}")

# Example Usage
folder_path = "Face_Images"  # Replace with your folder path
upload_images_from_folder(folder_path)