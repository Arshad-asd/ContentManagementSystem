
# Content Management System



This repository contains the source code for a Content Management System developed using Python Django REST Framework. The system handles Users authentication with Role based, Admin can mange users and authors and contents, Author can mange own content.

## Table of Contents

- [Core Features](#core-features)

- [Setup & Running Instructions](#project-set-up-and-running)

- [API Endpoints](#api-endpoints)

- [API Documentation](#api-documentation)

- [Testing](#testing)

## Core Features


#### 1. Authentication :


The Content Management System users a token-based authentication system to secure API endpoints. This system enhances security and ensures that only authenticated users have access to sensitive operations. The authentication mechanism is based on JSON Web Tokens (JWT), providing a stateless and secure approach.


#### 2. Content Management by Admin:


They give the admin the control and flexibility needed to keep digital content management  running smoothly and efficiently seeing everything that's been created,editing titles, descriptions, or even the content itself to keep it fresh and accurate.Delete anything that's outdated or no longer needed - keeping the library tidy and organized.


#### 3. Content Management by Author:


Own Content Management by Author gives the freedom and control to create, manage, and share content with ease.Create new content items of all sorts – articles, blog posts, tutorials.Edit and refine Don't like something wrote? No problem! Easily edit titles, descriptions, See a list of all author content items, including their status



## Project set up and running.

1. Clone the repository:

```bash
git clone https://github.com/Arshad-asd/ContentManagementSystem.git
```

2. Create and activate a virtual environment
   
```bash
python -m venv venv
```
```bash
# On Windows: .\venv\Scripts\activate
# On macOS/Linux: source venv/bin/activate
```
```bash
cd VendorManagementSystem
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Setup your database connections or you can use default Sqllite:

```bash
DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config('DB_NAME'),
        "USER": config('DB_USER'),
        "PASSWORD": config('DB_PASSWORD'),
        "HOST": config('DB_HOST'),
        "PORT": config('DB_PORT'),
    }
}
```
5. Apply database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser for administrative access:

```bash
python manage.py createsuperuser
```

7. Run the development server:

```bash
python manage.py runserver
```

8. Access the API at [http://localhost:8000/api/](http://localhost:8000/api/)

## Table of Contents

- [Core Features](#core-features)

- [Setup & Running Instructions](#project-setup-and-running)

- [API Endpoints](#api-endpoints)

- [API Documentation](#api-documentation)

- [Testing](#testing)

## API Endpoints

#### 1.Authentication:

- `POST /api/users/register`: Create a new user and author role based.

- `POST /api/users/token/`: Sign a new author or user or admin Role based.

#### 2. Admin side Users and Content Management:
          
- `GET /api/admin/users-list/`: All users list role based.


 
- `PATCH /api/admin/user/{user_id}/`: Block-Unblock user and author.

- `GET /api/content/contents-list/`: List all contents.

- `PUT /api/content/admin/edit/{content_id}/`: Edit s specific content.

- `DELETE /api/content/admin/delete/{content_id}/`: Delete specific content.


#### 3. Author side Own Content Management:

- `POST /api/content/author/create/`: Create own content.

- `GET /api/content/author/content-list/`: List all own contents .

- `GET /api/content/author/detail/{content_id}/`: Get detaild view of specific content.


- `PUT /api/content/author/edit/{content_id}/`: Edit s specific content own.

- `DELETE /api/content/author/delete/{content_id}/`: Delete specific content own.

## API Documentation


#### `POST /api/users/register/`

**Description:**

Create a new User Role based.

**Request:**
- **Method:** `POST`
- **Endpoint:** `/api/users/register/`
- **Body:**
  - `phone_number` (intiger, required): User's phone_number."phone_number must be +91-1122003300 this format country code mention".

  - `email` (string, required): User's email "email should be standard email fromat".

  - `password` (string, required): User's password. "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one digit."
  - `address` (object, optional):

    - `city` (string): User's city.
    - `state` (string): User's state.
    - `country` (string): User's country.
    - `pincode` (string): User's pincode.
  - `role` (string, required): User's role (author or user).



**Response:**
- **Success Response:**
  - **Status Code:** 201 Created
  - **Body:**
     ```json
     {
            "id": 42,
            "email": "user@gmail.com",
            "first_name": "User1",
            "last_name": "A A",
            "phone_number": "+911322114455",
            "address": {
                "city": Thrissur,
                "state": kerala,
                "country": India,
                "pincode": 680586
            },
            "role": "user"
     }
     ```

- **Error Response:**
  - **Status Code:** 400 Bad Request
  - **Body:**
    ```json
    {
      "error": "Invalid data. Please provide valid information."
    }
    ```

**Example:**
```bash
curl -X POST http://localhost:8000/api/register/ -d '{"email": "user@gmail.com", "password": "Password123", "first_name": "User1", "last_name": "A A", "phone_number": "+911322114455", "address": {"city": null, "state": null, "country": null, "pincode": null}, "role": "user"}' -H 'Content-Type: application/json'

```

#### `POST /api/token/`

**Request:**
- **Method:** `POST`
- **Endpoint:** `/api/token/`
- **Body:**
  - `email` (string, required): User's email.
  - `password` (string, required): User's password.

**Response:**
- **Success Response:**
  - **Status Code:** 200 OK
  - **Body:**
    ```json
    {
      "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...",
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9..."
    }
    ```

- **Error Response:**
  - **Status Code:** 401 Unauthorized
  - **Body:**
    ```json
    {
      "error": "Invalid credentials"
    }
    ```

**Example:**
```bash
curl -X POST http://localhost:8000/api/token/ -d '{"username": "example_user", "password": "Password123"}' -H 'Content-Type: application/json'
```


#### `POST /api/admin/users-list/`

**Request:**
- **Method:** `GET`
- **Endpoint:** `/api/admin/users-list/`
- **Header:** `Autherization`(JWT access_token as set token admin) :
  - `Type` : `Bearer Token`
  - `Token`: `eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...`
- **Parameters:**

  - search (string, optional): Search query to filter  users by email or phone number.
  - role (string, optional): Role to filter users by (e.g., "user" or "author").

**Response:**
- **Success Response:**
  - **Status Code:** 200 OK
  - **Body:**
    ```json
      [
        {
            "id": 1,
            "email": "user1@gmail.com",
            "first_name": "User",
            "last_name": "One",
            "phone_number": "+123456789",
            "address": {
            "city": "City1",
            "state": "State1",
            "country": "Country1",
            "pincode": "12345"
            },
            "role": "user"
        },
        {
            "id": 2,
            "email": "user2@gmail.com",
            "first_name": "User",
            "last_name": "Two",
            "phone_number": "+987654321",
            "address": {
            "city": "City2",
            "state": "State2",
            "country": "Country2",
            "pincode": "54321"
            },
            "role": "user"
        }
    ]
    ```

- **Error Response:**
  - **Status Code:** 401 Unauthorized
  - **Body:**
    ```json
    {
      "error": "Unauthorized"
    }
    ```
  - **Status Code:**  403 Forbidden
  - **Body:**
    ```json
    {
       "error": "Permission denied"
    }
    ```


**Example:**
```bash
curl -X GET http://localhost:8000/api/users/?search=user@gmail.com&role=user

```
