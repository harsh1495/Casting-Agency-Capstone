# Casting Agency

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP Dependencies

Install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.


## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
python app.py
```

## Authentication

The API uses Auth0 for 3rd-party authentication of users. These are the Auth0-specific settings:

```
AUTH0_DOMAIN = 'coffechats.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'capstonecast'
```

The API has 3 users, each with their own pre-configured permissions:

1. Assistant

```
username: assistant@moviecompany.com
password: Assistant@123
```

2. Director

```
username: director@moviecompany.com
password: Director@123
```

3. Executive Producer

```
username: producer@moviecompany.com
password: Producer@123
```

## Demo URL

<https://capstonecast.herokuapp.com>

Every API endpoint can be tested by first generating a valid JWT for each user by accessing this link:

<https://coffechats.auth0.com/authorize?audience=capstonecast&response_type=token&client_id=49SAF4GfFbFsFNyZix0t5ywzk8oNQjLy&redirect_uri=http://localhost:8080/login-results>

The JWTs are valid for 48 hours. Once, you have the access token, use Postman or CURL to hit and test the endpoints.

## API Endpoints

### GET ```"/actors"```

- Fetches a list of dictionary of all the actors
- Request arguments: None
- Returns: A list of dictionaries of actors which contain key-value pairs about the attributes of the actor


#### Sample Response

```

{
    "success": true,
    "actors": [
        {
            "id": 1,
            "name": "Tom Hanks",
            "ager": 48,
            "gender": "Male"
        },
        {
            "id": 2,
            "name": "Megan Fox",
            "ager": 30,
            "gender": "Female"
        }
    ]
}
```

### GET ```"/movies"```

- Fetches a list of dictionary of movies
- Request arguments: None
- Returns: List of dictionaries of movies which contain key-value pairs of information about the movies

#### Sample Response

```

{
    "success": true,
    "movies": [
        {
            "id": 1,
            "title": "Apollo 13",
            "release_date": "2005-05-05"
        },
        {
            "id": 2,
            "title": "Forrest Gump",
            "release_date": "2002-02-02"
        }
    ]
}

```


### POST ```"/actors"```

- Inserts a new actor in the database
- Request body: name, age and gender
- Returns: true if successfully inserts the actor and returns the updated list of actors

#### Sample request payload

```

{
    "name": "Vin Diesel",
    "age": 35,
    "gender": "Male"
}

```

#### Sample Response

```

{
    "success": true,
    "actors": [
        {
            "id": 1,
            "name": "Tom Hanks",
            "ager": 45,
            "gender": "Male"
        },

        {
            "id": 2,
            "name": "Megan Fox",
            "ager": 30,
            "gender": "Female"
        },
        {
            "id": 3,
            "name": "Vin Diesel",
            "ager": 35,
            "gender": "Male"
        }
    ]
}

```

### POST ```"/movies"```

- Inserts a new movie in the database
- Request body: title and release_date
- Returns: true if successfully inserts the movie and returns the updated list of movies

#### Sample request payload

```

{
    "title": "The Shawshank Redemption",
    "release_date": "1995-03-03"
}

```

#### Sample Response

```

{
    "success": true,
    "movies": [
        {
            "id": 1,
            "title": "Apollo 13",
            "release_date": "2005-05-05"
        },
        {
            "id": 2,
            "title": "Forrest Gump",
            "release_date": "2002-02-02"
        },
        {
            "id": 3,
            "title": "The Shawshank Redemption",
            "release_date": "1995-03-03"
        }
    ]
}

```


### DELETE ```"/actors/<actor_id>"```

- Delete an actor from the list of actors
- Request arguments: <actor_id>
- Returns: true if successfully deleted and id of the deleted actor

#### Sample Response

```

{
    "success": true,
    "delete": "3"
}

```

### DELETE ```"/movies/<movie_id>"```

- Delete a movie from the list of movies
- Request arguments: <movie_id>
- Returns: true if successfully deleted and id of the deleted movie

#### Sample Response

```

{
    "success": true,
    "delete": "3"
}

```

### PATCH ```"/actors/<actor_id>"```

- Updates an existing actor in the database
- Request body: name, age and gender
- Returns: true if successfully updates the actor and returns the updated list of actors

#### Sample request payload

```

{
    "name": "Vin Diesel",
    "age": 40,
    "gender": "Male"
}

```

#### Sample Response

```

{
    "success": true,
    "actors": [
        {
            "id": 1,
            "name": "Tom Hanks",
            "ager": 45,
            "gender": "Male"
        },

        {
            "id": 2,
            "name": "Megan Fox",
            "ager": 30,
            "gender": "Female"
        },
        {
            "id": 3,
            "name": "Vin Diesel",
            "ager": 40,
            "gender": "Male"
        }
    ]
}

```

### PATCH ```"/movies/<movie_id>"```

- Updates an existing movie in the database
- Request body: title and release_date
- Returns: true if successfully updates the movie and returns the updated list of movies

#### Sample request payload

```

{
    "title": "The Shawshank Redemption",
    "release_date": "1998-03-03"
}

```

#### Sample Response

```

{
    "success": true,
    "movies": [
        {
            "id": 1,
            "title": "Apollo 13",
            "release_date": "2005-05-05"
        },
        {
            "id": 2,
            "title": "Forrest Gump",
            "release_date": "2002-02-02"
        },
        {
            "id": 3,
            "title": "The Shawshank Redemption",
            "release_date": "1998-03-03"
        }
    ]
}

```

## Testing
To run the tests, run
```
python test_app.py
```