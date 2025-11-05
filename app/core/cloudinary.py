"""
Cloudinary configuration and utilities for image upload.
"""
import os
import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

async def upload_client_photo(file: UploadFile, client_id: int) -> str:
    """
    Upload a client house photo to Cloudinary.
    
    Args:
        file: The uploaded file from FastAPI
        client_id: The client ID for folder organization
        
    Returns:
        The secure URL of the uploaded image
        
    Raises:
        HTTPException: If upload fails or file type is invalid
    """
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_types)}"
        )
    
    # Validate file size (max 5MB)
    file_content = await file.read()
    if len(file_content) > 5 * 1024 * 1024:  # 5MB in bytes
        raise HTTPException(status_code=400, detail="File size must be less than 5MB")
    
    try:
        # Upload to Cloudinary with folder organization
        result = cloudinary.uploader.upload(
            file_content,
            folder=f"trebolsoft/clients/{client_id}",
            public_id=f"house_photo",
            overwrite=True,
            resource_type="image",
            transformation=[
                {"width": 1200, "height": 1200, "crop": "limit"},
                {"quality": "auto:good"}
            ]
        )
        
        return result["secure_url"]
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload image: {str(e)}"
        )
