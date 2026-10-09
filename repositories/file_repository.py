from pathlib import Path
from uuid import uuid4

import aiofiles
from fastapi import UploadFile

UPLOAD_DIR = Path("uploads")


async def save_file(file: UploadFile) -> str:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # Generate a unique filename to avoid overwriting files
    extension = Path(file.filename or "").suffix.lower()
    filename = f"{uuid4().hex}{extension}"

    file_path = UPLOAD_DIR / filename

    async with aiofiles.open(file_path, "wb") as output:
        while chunk := await file.read(1024 * 1024):
            await output.write(chunk)

    await file.close()

    return str(file_path)
