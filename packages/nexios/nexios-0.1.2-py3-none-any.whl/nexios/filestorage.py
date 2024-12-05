import os
from nexios.utils.files import UploadedFile,get_mime_type
from typing import Optional
from io import BytesIO
import asyncio
class LocalFileStorage:
    def __init__(self, storage_path :str = "uploads"):
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(os.path.abspath(storage_path)), exist_ok=True)
        

    
    async def store(self, file :UploadedFile, name :Optional[str] = None):

        return await self.save(
            name=name,
            file=file
        )

        
    async def save(self, name: str = None, file :UploadedFile = None) -> str:
        """
        Save the file to the specified path.
        Creates directories if they don't exist.
        """
        extention = file.extension
        filename = name or file.filename
        path = f"{self.storage_path}/{filename}{extention if name else ""}"
        content = await file.read()
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._sync_save, path, content)
        return path

    async def load(self, filepath):
        try:
            with open(filepath,"rb") as file:
                body = BytesIO(file.read())
                filename = filepath
                content_type: str = get_mime_type(filepath)
                size: int = len(file.read().strip())
                return UploadedFile(
                    filename=filename,
                    body=body,
                    content_type=content_type,
                    size=size
                )
        except FileNotFoundError:
            return None
    def _sync_save(self, path: str, content: bytes) -> None:
        """Synchronous save operation to be run in executor."""
        with open(path, 'wb') as f:
            f.write(content)

        
    async def delete(self, path :str) -> None:
         if os.path.exists(path):
            os.remove(path)
            return 
         raise ValueError("File Does not exists !")

   
    


    