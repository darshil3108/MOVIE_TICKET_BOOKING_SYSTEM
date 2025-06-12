import os
import subprocess
import sys

# Check if Django is installed
try:
    import django
    print(f"Django {django.get_version()} is already installed.")
except ImportError:
    print("Installing Django...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "django", "pillow"])
    print("Django installed successfully.")

# Create Django project
project_name = "movie_booking"
app_name = "booking"

# Check if project directory already exists
if os.path.exists(project_name):
    print(f"Project directory '{project_name}' already exists.")
else:
    print(f"Creating Django project '{project_name}'...")
    subprocess.check_call([sys.executable, "-m", "django", "startproject", project_name])
    print(f"Django project '{project_name}' created successfully.")

# Change to project directory
os.chdir(project_name)

# Create Django app
if os.path.exists(app_name):
    print(f"App directory '{app_name}' already exists.")
else:
    print(f"Creating Django app '{app_name}'...")
    subprocess.check_call([sys.executable, "-m", "django", "startapp", app_name])
    print(f"Django app '{app_name}' created successfully.")

print("Project setup completed successfully!")
