from io import BytesIO
from dataclasses import dataclass
import os
import hashlib
from typing import AsyncGenerator,Optional
import asyncio
import mimetypes

@dataclass
class UploadedFile:
    """Represents an uploaded file in the request."""
    filename: str
    content_type: str
    body: BytesIO
    size: int

    def __post_init__(self):
        # Reset pointer when initialized
        self.body.seek(0)
        
    @property
    def extension(self) -> str:
        """Get file extension from filename."""
        return os.path.splitext(self.filename)[1].lower()

    async def read(self) -> bytes:
        """Read the entire file content."""
        # Use asyncio to prevent blocking
        loop = asyncio.get_event_loop()
        self.body.seek(0)
        content = await loop.run_in_executor(None, self.body.read)
        self.body.seek(0)  # Reset for future reads
        return content
    
    async def save(self, path: str = None) -> str:
        """
        Save the file to the specified path.
        Creates directories if they don't exist.
        """
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        content = await self.read()
        
        
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._sync_save, path, content)
        return path

    def _sync_save(self, path: str, content: bytes) -> None:
        """Synchronous save operation to be run in executor."""
        with open(path, 'wb') as f:
            f.write(content)

    def seek(self, offset: int, whence: int = 0) -> int:
        """Seek to a specific position in the file."""
        return self.body.seek(offset, whence)

    def tell(self) -> int:
        """Return current position in the file."""
        return self.body.tell()

    async def calculate_hash(self, algorithm: str = 'sha256') -> str:
        """Calculate file hash using specified algorithm."""
        content = await self.read()
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync_calculate_hash, content, algorithm)

    def _sync_calculate_hash(self, content: bytes, algorithm: str) -> str:
        """Synchronous hash calculation to be run in executor."""
        hasher = hashlib.new(algorithm)
        hasher.update(content)
        return hasher.hexdigest()

    def validate_mimetype(self, allowed_types: list[str]) -> bool:
        """Validate if file mimetype is allowed."""
        return self.content_type in allowed_types

    def validate_size(self, max_size: int) -> bool:
        """Validate if file size is within limit."""
        return self.size <= max_size

    async def chunks(self, chunk_size: int = 8192) -> AsyncGenerator[bytes, None]:
        """
        Yield file contents in chunks for memory-efficient processing.
        """
        loop = asyncio.get_event_loop()
        self.body.seek(0)
        
        while True:
            chunk = await loop.run_in_executor(None, self.body.read, chunk_size)
            if not chunk:
                break
            yield chunk
            
        self.body.seek(0)

    def file(self) -> BytesIO:
        """
        Return the file itself as a BytesIO object.
        """
        self.body.seek(0)
        return self.body
    
    def close(self) -> None:
        """Close the underlying BytesIO object."""
        self.body.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __repr__(self) -> str:
        return f"<UploadedFile name={self.filename} type={self.content_type} size={self.size}>"
    
    def __str__(self) -> str:
        return f"<UploadedFile name={self.filename}>"

    def __len__(self) -> int:
        return self.size




def get_mime_type(filename: str) -> str:
    """
    Determine the MIME type of a file based on its filename.
    
    Args:
        filename (str): The name of the file, including its extension.
    
    Returns:
        str: The detected MIME type, or 'application/octet-stream' if unknown.
    """
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type or "application/octet-stream"



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

        

   
    


    