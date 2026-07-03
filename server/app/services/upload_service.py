from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import UPLOAD_DIR

ALLOWED_IMAGE_CONTENT_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


class UploadService:
    @staticmethod
    def save_image(file: UploadFile, folder: str = "gallery") -> str:
        extension = ALLOWED_IMAGE_CONTENT_TYPES.get(file.content_type or "")
        if extension is None:
            raise ValueError("Only JPEG, PNG, and WEBP images are allowed.")

        target_dir = UPLOAD_DIR / folder
        target_dir.mkdir(parents=True, exist_ok=True)
        file_name = f"{uuid4().hex}{extension}"
        target_path = target_dir / file_name

        with target_path.open("wb") as output_file:
            while chunk := file.file.read(1024 * 1024):
                output_file.write(chunk)

        return str(Path("uploads") / folder / file_name)


def save_upload(file):
    return UploadService.save_image(file)
