from pathlib import Path
# Initialize app

from pathlib import Path

import os
from typing import Union
      
class StaticFilesHandler:
    def __init__(self, directory: Union[str, Path], url_prefix: str = "/static/"):
        
        self.directory = Path(directory).resolve()
        self.url_prefix = url_prefix.strip("/") + "/"
        
        if not self.directory.exists():
            os.makedirs(self.directory)
        
        if not self.directory.is_dir():
            raise ValueError(f"{directory} is not a directory")

    def _is_safe_path(self, path: Path) -> bool:
        """Check if the path is safe to serve"""
        try:
            # Resolve the full path to handle any '..' or '.' in the path
            full_path = path.resolve()
            # Check if the resolved path starts with the base directory
            return str(full_path).startswith(str(self.directory))
        except (ValueError, RuntimeError):
            return False

    async def __call__(self, request, response, **kwargs):
        # Get the relative path from the URL
        path = request.url.path
        if path.startswith("/"):
            path = path[1:]
        
        # Remove the url prefix
        if path.startswith(self.url_prefix.strip("/")):
            path = path[len(self.url_prefix.strip("/")):]
        
        # Construct the full file path
        # file_path = (self.directory / path).resolve()
        file_path = f"{self.directory}{path}"
        # Security check
        if not self._is_safe_path(Path(file_path)):
            return response.status(403)
            
        
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            return response.json("Not found",status_code = 404)
            

        response.file(file_path)
  