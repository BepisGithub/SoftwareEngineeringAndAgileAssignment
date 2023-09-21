# Introduction
A web app was created as a proof of concept to make it easier for users of Prime Video to browse through all the movies and quickly see information about it as well as reviews that are associated with it.

The app involves a home page that displays all movies in the database. There is a navigation bar at the top that is present on all pages, it includes a hyperlink to go to the home page or to login (or logout, if the user is already logged in). On the login page, the user can enter their account details to login, but if they do not have an account, they can click the link on the login page to allow them to register an account.

# Run unit tests

Tests must be run per app, which this project has 3 of: user, review and movie

Navigate to the root folder that has the manage.py file and then run:

python manage.py test {app.name}.tests

Replace {app.name} with one of the app names, e.g:

python manage.py test user.tests

# How to run the app and test it locally

This program uses python 3.9 and django

You must have python 3.9 and django installed to run this project

Open the command line and navigate to the primeVideoReviewPlatform folder

If you use the terminal to display the contents of this folder, you should see a file called manage.py

![img.png](README media/img.png)

Run the terminal command 'python manage.py runserver'
(Note that this project uses python 3.9)

![img.png](README media/img2.png)

The console should output something like below

![img.png](README media/img3.png)

Navigate to the link provided (often is http://127.0.0.1:8000/)

You can now access the website

# Sample user login details

Below are the account details of a regular user which can be used to log in to the website, please note that the username and password are both case sensitive:

Username – theDudeHimself

Password – hunter2

An admin account is also provided below to login to the website from the admin’s perspective:

Username – random_guy

Password - Adminpassword123


