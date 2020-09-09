### Installing the application

1. Get the source code:

        git clone https://github.com/catalinjitea/swproject
        cd swproject

1. Create and run virtual environment:

        python3 -m venv <venv_name>
        source <venv_name>/bin/activate

1. Install dependencies:

        pip install -r requirements.txt

1. Run migrations:
    
        python manage.py migrate

1. Create superuser:

        python manage.py createsuperuser

1. Import the dataset

        python manage.py import_vulnerabilities django_vulnerabilities.csv

1. Run the server

        python manage.py runserver

1. See the results on http://localhost:8000/
