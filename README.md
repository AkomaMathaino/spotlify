# Spotlify

This is the back end for an app similar to spotify. It includes:
* User registration and authentication
* Account verification to verify users as artists
* A way for verified artists to create both albums and songs associated with specific albums
* Playlist creation for users
* A way for songs to be added to playlists by users

Django is being used to model the data and handle HTTP requests. The app has also been containerized using Docker Compose.

## Usage

1. Make sure you have Python 3.x, PostgreSQL, and Docker installed on your system.
2. Set up a virtual environment with the command `python -m venv venv`.
3. Install the dependencies with the command `pip install -r requirements.txt`.
4. Run the docker containers with the command `docker compose up -d`.
5. Make the database migrations with the commands `python manage.py makemigrations` followed by `python manage.py migrate`.
6. API requests can now be made using an API testing tool, such as Insomnia, and data will be created, retrieved, updated, or deleted accordingly.