# python-django-MovieRec Movie Recommendation App

This Django project recommends movies to users through emotional content analysis. The user enters the emotion content and the system recommends movies that are compatible with that emotion.

## Start

1. Copy the project files to your local machine.

2.Create and enable the virtual environment:
```
python -m venv venv
source venv/bin/activate (Linux/Mac)
venv\Scripts\activate (Windows)
```
3.Install required dependencies:
```
pip install -r requirements.txt
```
4.Create the database and run the application:
```
python manage.py migrate
python manage.py runserver
```
5.You can run the application by going to http://127.0.0.1:8000/ in your browser.

## Usage

* Users can get recommended movies after they sign up and log in, and those who use them to their personal watchlists to watch.

* Users can also make movie reviews and mark movies they've watched when they watch movies.

## Requirements
* Python 3.6 or higher
* Django 3.x
* requests
* django-crispy-forms

## Licence
[MIT](https://choosealicense.com/licenses/mit/)
