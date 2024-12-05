import os

def create_project_structure(project_name: str):
    """Create the basic project structure for a Nexio application."""
    
    # Base directories
    directories = [
        f"{project_name}/controllers",
    ]
    
    # Create directories
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        create_file(f"{directory}/__init__.py", "")
    
    # Create main application files
    create_file(f"{project_name}/main.py", main_code())
    create_file(f"{project_name}/models.py", models_code())
    create_file(f"{project_name}/settings.py", settings_code())
    create_file(f"{project_name}/controllers/home_handler.py", routes_code())
    create_file(f"{project_name}/README.md", readme_code())

    print(f"\n✨ Created new Nexio project: {project_name}")
    print("\nProject structure:")
    print(f"""
{project_name}/
├── controllers/
│   └── home_handler.py
├── main.py
├── models.py
├── settings.py
└── README.md
    """)
    
    print("\nTo get started:")
    print(f"1. cd {project_name}")
    print("2. Install dependencies using `pip install -r requirements.txt`")
    print("3. Run migrations using Aerich:")
    print("   - `aerich init -t settings.TORTOISE_ORM`")
    print("   - `aerich migrate`")
    print("   - `aerich upgrade`")
    print("4. Run the app with uvicorn:")
    print("   - `uvicorn main:app --reload`")
    print("\nYour app will be available at http://localhost:8000")

def create_file(file_path: str, content: str):
    """Create a file with the given content."""
    with open(file_path, "w") as f:
        f.write(content)

def main_code():
    return '''import uvicorn
from nexio import get_application
from nexio.routers import Routes
from tortoise import Tortoise as db
from contextlib import asynccontextmanager
import traceback
import os

from settings import AppConfig
from controllers.home_handler import home_handler

# Initialize app
app = get_application(config=AppConfig)

@app.on_startup
async def connect_db():
    try:
        db_path = os.path.join(os.path.dirname(__file__), "db.sqlite3")
        await db.init(
            db_url=f"sqlite:///{db_path}",
            modules={"models": ["models"]}  # Use models.py directly
        )
        await db.generate_schemas()
        print("Database connected")
    except Exception as e:
        print(f"Database connection error: {e}")
        print(traceback.format_exc())

@app.on_shutdown
async def disconnect_db():
    try:
        await db.close_connections()
        print("Database disconnected")
    except Exception as e:
        print(f"Database disconnect error: {e}")

app.add_route(Routes("/", home_handler))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
'''

def models_code():
    return '''
'''

def settings_code():
    return '''
    import os
    from nexio.config.settings import BaseConfig

migration = {
    "connections": {
        "default": f"sqlite://{os.path.join(os.path.dirname(__file__), 'database.db')}"
    },
    "apps": {
        "models": {
            "models": ["nexio.sessions.models","aerich.models"], 
            "default_connection": "default",
        },
    },
}

class AppConfig(BaseConfig):
    SECRET_KEY = "your-secret-key"  # Change this in production!
'''

def routes_code():
    return '''from nexio.http.request import Request
from nexio.http.response import NexioResponse

async def home_handler(request: Request, response: NexioResponse, **kwargs):
    return response.json({
        "message": "Welcome to your new Nexio application!",
        "docs": "https://nexio.example.com/docs"  
    })
'''

def readme_code():
    return '''# Nexio Application Setup

## Requirements
- Python 3.8 or later
- [Aerich](https://github.com/tortoise/aerich) for migrations
- [Uvicorn](https://www.uvicorn.org/) for running the app

## Setup Instructions

1. Install the required dependencies:
   ```bash
   
Migrate the database: Run the following command to create the initial migration files:

```bash

aerich init -t settings.migration
Then, run the following command to apply the migrations to the database:
```
bash
```
aerich migrate
aerich upgrade
```
To start the application, use Uvicorn:

``bash

uvicorn main:app --reload
```
'''