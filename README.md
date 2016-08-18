# flaskpost
A simple blog created with Flask. Utilizes sqlite3 for storage.

## Prerequisites
* Flask - the web framework
* Flask-Login - provides user session management
* Flask-SQLAlchemy - ORM
* passlib - provides hashing for passwords

All of the above can be installed through pip:

    pip install <module>

## Usage
1. Clone the repo
2. Run "./flaskpost.py" in your terminal
3. Open "127.0.0.1:5000" in your browser
4. Walk through the quick setup
5. You may now post to the blog through the post-link and view all blog-posts on
   the main-link

## List of things that needs to be done
1. Wrap SQL with SQLAlchemy (done)
2. Add a login system (done)
3. Require authorization from said login system to make posts (done)
4. Expand setup and make it work properly (done)
5. Add "staggered" post loading
6. Make the entire thing look better

## A warning that must be heeded
Do not deploy flaskpost without HTTPS. It will in its current state transmit
password on setup and login in plaintext, which is not good if you're not
running it over HTTPS.

## License
MIT License. See LICENSE-file.
