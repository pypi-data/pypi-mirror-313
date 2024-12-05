import os
from typing import Optional, Union
from tortoise.fields.base import Field
from nexios.utils.files import UploadedFile
import mimetypes,asyncio,uuid
from io import BytesIO
from nexios.filestorage import LocalFileStorage



def get_mime_type(filename: str) -> str:
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type or "application/octet-stream"

class FileField(Field):
    """
    Custom field for handling image uploads in Tortoise ORM.
    Supports direct Flask request.files uploads.
    """
    
    def __init__(
        self,
        upload_to: str = "uploads",
        null: bool = False,
        storage = LocalFileStorage,
        **kwargs
    ):
        super().__init__(null=null, **kwargs)
        self.upload_to = upload_to
        self.storage = storage()
        
        os.makedirs(upload_to, exist_ok=True)
    def to_db_value(
        self, 
        value: Union[UploadedFile, str, bytes, None], 
        instance
    ) -> Optional[str]:
        """Convert the Python value to a database value"""
        if value is None:
            return None
        
        if not isinstance(value, UploadedFile):
            return ""
       
        def wrapper():
            asyncio.run(self.storage.store(value))
            return value.filename
        return wrapper()

    def to_python_value(
        self, 
        value: Optional[str]
    ) -> Optional[str]:

        if not value:
            return
        class wrapper:
    
                
            def __repr__(cls) -> str:
                return value
            
            @property
            async def file(cls):
                return await self.storage.load(value)
            
            async def delete(cls):
                try:
                    await self.storage.delete(value)
                    return

                except ValueError:
                    return
                    
        return wrapper()
    



