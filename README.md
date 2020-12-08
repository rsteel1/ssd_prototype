# Secure Software Development Coursework 1 Assignment 2 S1308593

This is an assignment for my university course based around secure software design. There are obviously some bad things in here like the encryption key and app secret key (which should be held outside the repository) and no real email implementation, it all just runs inside django and stores in the sent_emails folder.

Thankfully this is just a prototype.

## Running the app

1. Install Python
2. Clone this repository
3. `virtualenv _venv`
4. `_venv\Scripts\activate` (this will be different if not on Windows)
5. `pip install -r requirements.txt`
6. `python manage.py createsuperuser`
7. `python manage.py loaddata data`
8. `python manage.py runserver`

That's it!