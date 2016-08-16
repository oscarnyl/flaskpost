# flaskpost
A simple blog created with Flask. Utilizes sqlite3 for storage.

## Prerequisites
* Flask (can be installed through pip: "pip install Flask"
* passlib (can be installed through pip: "pip install passlib"

## Usage
1. Clone the repo
2. Run "./flaskpost.py" in your terminal
3. Open "127.0.0.1:5000" in your browser
4. Walk through the quick setup
5. You may now post to the blog through the post-link and view all blog-posts on
   the main-link

## List of things that needs to be done
1. Add a login system (Half-done)
2. Require authorization from said login system to make posts
3. Expand setup and make it work properly (Half-done)

## A warning that must be heeded
Do not deploy flaskpost without HTTPS. It will in its current state transmit
password on setup and login in plaintext, which is not good if you're not
running it over HTTPS.

## License
MIT License. See LICENSE-file.
