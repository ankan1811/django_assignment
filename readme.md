## Overview

This project provides a set of RESTful APIs for managing users, posts, and comments. It allows users to create, view, and edit their profiles, create posts, retrieve posts, and comment on posts.

### Purposefully, I have kept the .env file so that the setup becomes easy. Obviously,it will be gitignored in a real scenario

## Base URL

The base URL for all endpoints is: `http://127.0.0.1:8000/`

## To Run :-

### 1. First navigate and cd to the project directory

### 2. pip install -r requirements.txt

### 3. Apply migrations to create database tables: (python manage.py makemigrations , python manage.py migrate )

### 4. python manage.py runserver

## Routes Documentation

Below are the available routes along with their JSON bodies:

- `/signup`: Create a new user account.
- **Method:** `POST`

  ```json
  {
    "username": "your_username",
    "email": "your_email@example.com",
    "password": "your_password"
  }
  ```

- `/login`: Log in to an existing user account.
- **Method:** `POST`

  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```

- `/notes/create`: Create a new note. (Put header as authorization : "Token token" token=long string which you received for login route)
- **Method:** `POST`

```json
{
  "title": "Note Title",
  "content": "Note Content",
  "owner":"1" ,(put id of the user,which is 1 for the first created user auto incremented)
  "shared_with":[2] (array of user ids)
}
```

- `/notes/{id}`: Retrieve a specific note by its ID.(Put header as authorization : "Token token" token=long string which you received for login route)
- **Method:** `GET`

- `/notes/get`: Retrieve all notes.(Put header as authorization : "Token token" token=long string which you received for login route)
- **Method:** `GET`

- `/notes/update/{id}`: Update an existing note.(Put header as authorization : "Token token" token=long string which you received for login route)
- **Method:** `PUT`

```json
{
  "title": "Updated Note Title",
  "content": "Updated Note Content"
}
```

- `/notes/share`: Share a note with other users.(Put header as authorization : "Token token" token=long string which you received for login route)
- **Method:** `POST`

```json
{
  "users": [1, 2, 3]
}
```

- `/notes/version-history/{id}`: View the version history of a note.

```

```

```

```
