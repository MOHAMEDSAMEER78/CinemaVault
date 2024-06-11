# Movie_Library

# Create Virtual Environment
  python3 -m venv myenv

# Run Virtual Environment
  source myenv/bin/activate

# Install Requirements.txt
  pip install -r requirements.txt

# Make Migration and migrate
  python3 manage.py makemigrations
  python3 manage.py migrate

# Run Django Application
  python3 manage.py runserver
