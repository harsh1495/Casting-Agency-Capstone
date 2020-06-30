import os
import json

from datetime import datetime

from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_moment import Moment
from flask_migrate import Migrate

import config
from models import setup_db, Actor, Movie, ActorMovie
from auth import AuthError, requires_auth

app = Flask(__name__)

# app.config.from_object('config')
moment = Moment(app)

# cross-origin resource sharing
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

db = setup_db(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

@app.route("/", methods=["GET"])
def index():
    return("Welcome to The Movie Company!")

@app.route("/actors", methods=["GET"], endpoint="get_actors")
@requires_auth('view:actor')
def get_actors(jwt):
    try:
        actors = Actor.query.all()

        data = {
            "success": True,
            "actors": [actor.format() for actor in actors]
            }

        return json.dumps(data), 200

    except:
        return json.dumps({
            "success": False,
            "error": "An error occurred"
        }), 500

@app.route("/movies", methods=["GET"], endpoint="get_movies")
@requires_auth('view:movie')
def get_movies(jwt):
    try:
        movies = Movie.query.all()

        data = {
            "success": True,
            "movies": [movie.format() for movie in movies]
            }

        return json.dumps(data, default=str), 200

    except:
        return json.dumps({
            "success": False,
            "error": "An error occurred"
        }), 500

@app.route("/actors", methods=["POST"], endpoint="post_actor")
@requires_auth('post:actor')
def post_actors(jwt):
    data = request.get_json()

    name = data.get("name")
    age = int(data.get("age"))
    gender = data.get("gender")

    try:
        actor = Actor(name=name, age=age, gender=gender)
        actor.insert()

        return json.dumps({
            "success": True,
            "actors": [actor.format() for actor in Actor.query.all()]
        }), 200

    except:
        return json.dumps({
            "success": False,
            "error": "An error occured"
        }), 500

@app.route("/movies", methods=["POST"], endpoint="post_movie")
@requires_auth('post:movie')
def post_movies(jwt):

    data = request.get_json()

    title = data.get("title")
    release_date = datetime.strptime(data.get("release_date"), "%Y-%m-%d")

    try:
        movie = Movie(title=title, release_date=release_date)
        movie.insert()

        return json.dumps({
            "success": True,
            "movies": [movie.format() for movie in Movie.query.all()]
        }, default=str), 200

    except:
        return json.dumps({
            "success": False,
            "error": "An error occured"
        }), 500

@app.route("/actors/<actor_id>", methods=["DELETE"], endpoint="delete_actor")
@requires_auth('delete:actor')
def delete_actors(jwt, actor_id):

    actor = Actor.query.filter_by(id=actor_id).one_or_none()

    if not actor:
        abort(404)

    try:
        actor.delete()

        return json.dumps({
            "success": True,
            "delete": actor_id
        }), 200

    except:
        return json.dumps({
            "success": False,
            "error": "An error occured"
        }), 500

@app.route("/movies/<movie_id>", methods=["DELETE"], endpoint="delete_movie")
@requires_auth('delete:movie')
def delete_movies(jwt, movie_id):

    movie = Movie.query.filter_by(id=movie_id).one_or_none()

    try:
        movie.delete()

        return json.dumps({
            "success": True,
            "delete": movie_id
        }), 200

    except:
        return json.dumps({
            "success": False,
            "error": "An error occured"
        }), 500


@app.route("/actors/<actor_id>", methods=["PATCH"], endpoint="patch_actor")
@requires_auth('patch:actor')
def patch_actors(jwt, actor_id):

    actor = Actor.query.filter_by(id=actor_id).one_or_none()

    data = request.get_json()

    if not actor:
        abort(404)

    name = data.get("name")
    age = int(data.get("age"))
    gender = data.get("gender")

    try:
        actor.name = name
        actor.age = age
        actor.gender = gender

        actor.update()

        return json.dumps({
            "success": True,
            "actors": [actor.format() for actor in Actor.query.all()]
        }), 200

    except:
        return json.dumps({
            "success": False,
            "error": "An error occured"
        }), 500

@app.route("/movies/<movie_id>", methods=["PATCH"], endpoint="patch_movie")
@requires_auth('patch:movie')
def patch_movies(jwt, movie_id):

    movie = Movie.query.filter_by(id=movie_id).one_or_none()

    data = request.get_json()

    if not movie:
        abort(404)

    title = data.get("title")
    release_date = datetime.strptime(data.get("release_date"), "%Y-%m-%d")

    try:
        movie.title = title
        movie.release_date = release_date

        movie.update()

        return json.dumps({
            "success": True,
            "movies": [movie.format() for movie in Movie.query.all()]
        }, default=str), 200

    except:
        return json.dumps({
            "success": False,
            "error": "An error occured"
        }), 500


## Error Handling
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found"
    }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
    }), 400


@app.errorhandler(AuthError)
def handle_auth_error(e):
    response = jsonify(e.error)
    response.status_code = e.status_code
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)