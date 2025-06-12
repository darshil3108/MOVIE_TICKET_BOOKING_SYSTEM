import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"✗ Error during {description}: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False
    return True

def main():
    print("Setting up complete Django Movie Booking System...")
    
    # Install required packages
    if not run_command("pip install django pillow", "Installing Django and Pillow"):
        return
    
    # Create project directory structure
    os.makedirs("movie_booking", exist_ok=True)
    os.makedirs("movie_booking/booking", exist_ok=True)
    os.makedirs("movie_booking/booking/migrations", exist_ok=True)
    os.makedirs("movie_booking/booking/templatetags", exist_ok=True)
    os.makedirs("movie_booking/templates", exist_ok=True)
    os.makedirs("movie_booking/templates/booking", exist_ok=True)
    os.makedirs("movie_booking/static", exist_ok=True)
    os.makedirs("movie_booking/static/css", exist_ok=True)
    os.makedirs("movie_booking/static/js", exist_ok=True)
    os.makedirs("movie_booking/media", exist_ok=True)
    os.makedirs("movie_booking/media/movie_posters", exist_ok=True)
    
    print("✓ Project directory structure created")
    print("\nNext steps:")
    print("1. Navigate to the movie_booking directory: cd movie_booking")
    print("2. Apply migrations: python manage.py migrate")
    print("3. Create superuser: python manage.py createsuperuser")
    print("4. Load sample data: python manage.py shell < load_sample_data.py")
    print("5. Run server: python manage.py runserver")

if __name__ == "__main__":
    main()
