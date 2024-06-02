#!/bin/sh

# Exit immediately if a command exits with a non-zero status
# set -e

# # Navigate to the app directory
# cd /app

# # Pull the latest changes from the Git repository
# echo "Pulling the latest changes from the repository..."
# git pull

# # Install any new dependencies
# pip install --no-cache-dir -r requirements.txt

# RUN python manage.py makemigrations #

# # Apply database migrations
# echo "Applying database migrations..."
# python manage.py migrate

# # Collect static files
# echo "Collecting static files..."
# python manage.py collectstatic --noinput

# # Start the Django development server
# echo "Starting the Django server..."
# # exec python manage.py runserver 0.0.0.0:8000

#!/bin/sh

# Wait for the database to be ready
while ! nc -z db 3306; do
  sleep 1
done

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files (if necessary)
python manage.py collectstatic --noinput

# Start the Django server
exec "$@"
