import os
import unittest
import json
import random
from flask_sqlalchemy import SQLAlchemy
from app import app
from models import setup_db, Actor, Movie

# Get JWTs stored in environment variables
assistant = os.getenv('ASSISTANT')
director = os.getenv('DIRECTOR')
producer = os.getenv('PRODUCER')


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.assistant = assistant
        self.director = director
        self.producer = producer
        self.db = setup_db(self.app)

    def tearDown(self):
        """Executed after reach test"""
        pass

    # GET REQUESTS
    def test_get_actors_by_assistant(self):
        res = self.client().get('/actors', headers={
                                         "Authorization": "Bearer {}".format(self.assistant)
                                     })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_actors_401_error(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')

    def test_get_movies_by_assistant(self):
        res = self.client().get('/movies', headers={
                                         "Authorization": "Bearer {}".format(self.assistant)
                                     })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_get_movies_401_error(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')

    def test_get_actors_by_director(self):
        res = self.client().get('/actors', headers={
                                         "Authorization": "Bearer {}".format(self.director)
                                     })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_actors_by_producer(self):
        res = self.client().get('/actors', headers={
                                         "Authorization": "Bearer {}".format(self.producer)
                                     })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_movies_by_director(self):
        res = self.client().get('/movies', headers={
                                         "Authorization": "Bearer {}".format(self.director)
                                     })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_movies_by_producer(self):
        res = self.client().get('/movies', headers={
                                         "Authorization": "Bearer {}".format(self.producer)
                                     })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    # POST REQUESTS
    def test_post_actors_by_director(self):
        num_actors = len(Actor.query.all())

        res = self.client().post('/actors',headers={
                                          "Authorization": "Bearer {}".format(self.director)
                                      }, json={
                                          "name": "Margot Robbie",
                                          "gender": "Female",
                                          "age": 30
                                      })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data["actors"]), num_actors+1)

    def test_post_actors_by_producer(self):
        num_actors = len(Actor.query.all())

        res = self.client().post('/actors',headers={
                                          "Authorization": "Bearer {}".format(self.producer)
                                      }, json={
                                          "name": "Dwayne Johnson",
                                          "gender": "Male",
                                          "age": 32
                                      })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data["actors"]), num_actors+1)

    def test_post_actors_by_assistant_401_error(self):
        res = self.client().post('/actors',headers={
                                          "Authorization": "Bearer {}".format(self.assistant)
                                      }, json={
                                          "name": "Dwayne Johnson",
                                          "gender": "Male",
                                          "age": 32
                                      })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'invalid_permissions')

    def test_post_movies_by_director_401_error(self):
        res = self.client().post('/movies',headers={
                                          "Authorization": "Bearer {}".format(self.director)
                                      }, json={
                                          "title": "Wolf of the Wall Street",
                                          "release_date": "2011-07-07"
                                      })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'invalid_permissions')

    def test_post_movies_by_producer(self):
        num_movies = len(Movie.query.all())

        res = self.client().post('/movies',headers={
                                          "Authorization": "Bearer {}".format(self.producer)
                                      }, json={
                                          "title": "Prestige",
                                          "release_date": "2013-06-06"
                                      })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data["movies"]), num_movies+1)

    def test_post_movies_by_assistant_401_error(self):
        res = self.client().post('/movies',headers={
                                          "Authorization": "Bearer {}".format(self.assistant)
                                      }, json={
                                          "title": "Prestige",
                                          "release_date": "2013-06-06"
                                      })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'invalid_permissions')

    def test_post_actors_401_error(self):
        res = self.client().post('/actors',headers={}, json={
                                          "name": "Dwayne Johnson",
                                          "gender": "Male",
                                          "age": 32
                                      })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')

    def test_post_movies_401_error(self):
        res = self.client().post('/movies',headers={}, json={
                                          "title": "Prestige",
                                          "release_date": "2013-06-06"
                                      })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')

    # PATCH REQUESTS
    def test_patch_actors_by_director(self):
        res = self.client().post('/actors',headers={
                                          "Authorization": "Bearer {}".format(self.director)
                                      }, json={
                                          "name": "Morgan Freemann",
                                          "gender": "Male",
                                          "age": 58
                                      })

        data = json.loads(res.data)

        for actor in data["actors"]:
            if actor["name"] == "Morgan Freemann":
                actor_id = actor["id"]
                break

        res = self.client().patch('/actors/{}'.format(actor_id),
                                       headers={"Authorization": "Bearer {}".format(self.director)
                                        },
                                        json={
                                        "name": "Morgan Freeman",
                                        "gender": "Male",
                                        "age": 58
                                    })

        data = json.loads(res.data)

        actor = Actor.query.filter_by(id=actor_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor.name, "Morgan Freeman")

    def test_patch_actors_by_producer(self):
        res = self.client().post('/actors',headers={
                                          "Authorization": "Bearer {}".format(self.producer)
                                      }, json={
                                          "name": "Test Director",
                                          "gender": "Male",
                                          "age": 65
                                      })

        data = json.loads(res.data)

        for actor in data["actors"]:
            if actor["name"] == "Test Director":
                actor_id = actor["id"]
                break

        res = self.client().patch('/actors/{}'.format(actor_id),
                                       headers={"Authorization": "Bearer {}".format(self.producer)
                                        },
                                        json={
                                        "name": "Test Director",
                                        "gender": "Female",
                                        "age": 65
                                    })

        data = json.loads(res.data)

        actor = Actor.query.filter_by(id=actor_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor.gender, "Female")

    def test_patch_actors_by_assistant_401_error(self):

        res = self.client().patch('/actors/{}'.format(1),
                                       headers={"Authorization": "Bearer {}".format(self.assistant)
                                        },
                                        json={
                                        "name": "Test Assistant",
                                        "gender": "Female",
                                        "age": 65
                                    })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'invalid_permissions')

    def test_patch_actors_401_error(self):

        res = self.client().patch('/actors/{}'.format(1),
                                       headers={},
                                        json={
                                        "name": "Test Assistant",
                                        "gender": "Female",
                                        "age": 65
                                    })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')


    def test_patch_movies_by_director(self):
        res = self.client().post('/movies',headers={
                                          "Authorization": "Bearer {}".format(self.producer)
                                      }, json={
                                          "title": "Test Movie Director",
                                          "release_date": "2010-05-01"
                                      })

        data = json.loads(res.data)

        for movie in data["movies"]:
            if movie["title"] == "Test Movie Director":
                movie_id = movie["id"]
                break

        res = self.client().patch('/movies/{}'.format(movie_id),
                                       headers={"Authorization": "Bearer {}".format(self.director)
                                        },
                                        json={
                                        "title": "Test Movie Director New",
                                        "release_date": "2020-05-01"
                                    })

        data = json.loads(res.data)

        movie = Movie.query.filter_by(id=movie_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie.title, "Test Movie Director New")

    def test_patch_movies_by_producer(self):
        res = self.client().post('/movies',headers={
                                          "Authorization": "Bearer {}".format(self.producer)
                                      }, json={
                                          "title": "Test Movie Producer",
                                          "release_date": "2010-05-01"
                                      })

        data = json.loads(res.data)

        for movie in data["movies"]:
            if movie["title"] == "Test Movie Producer":
                movie_id = movie["id"]
                break

        res = self.client().patch('/movies/{}'.format(movie_id),
                                       headers={"Authorization": "Bearer {}".format(self.producer)
                                        },
                                        json={
                                        "title": "Test Movie Producer New",
                                        "release_date": "2020-05-01"
                                    })

        data = json.loads(res.data)

        movie = Movie.query.filter_by(id=movie_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie.title, "Test Movie Producer New")

    def test_patch_movies_by_assistant_401_error(self):

        res = self.client().patch('/movies/{}'.format(1),
                                       headers={"Authorization": "Bearer {}".format(self.assistant)
                                        },
                                        json={
                                        "title": "Test Movie Assistant",
                                        "release_date": "2010-02-09"
                                    })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'invalid_permissions')

    def test_patch_movies_401_error(self):

        res = self.client().patch('/movies/{}'.format(1),
                                       headers={},
                                        json={
                                        "title": "Test Movie Assistant",
                                        "release_date": "2010-02-09"
                                    })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')


    # DELETE REQUESTS

    def test_delete_actors_by_director(self):
        res = self.client().post('/actors',headers={
                                          "Authorization": "Bearer {}".format(self.director)
                                      }, json={
                                          "name": "Morgan Freeman",
                                          "gender": "Male",
                                          "age": 58
                                      })

        data = json.loads(res.data)

        for actor in data["actors"]:
            if actor["name"] == "Morgan Freeman":
                actor_id = actor["id"]
                break

        res = self.client().delete('actors/{}'.format(actor_id),
                                        headers={
                                            "Authorization": "Bearer {}".format(self.director)
                                        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(int(data["delete"]), actor_id)

    def test_delete_actors_by_producer(self):
        res = self.client().post('/actors',headers={
                                          "Authorization": "Bearer {}".format(self.producer)
                                      }, json={
                                          "name": "Morgan Freeman",
                                          "gender": "Male",
                                          "age": 58
                                      })

        data = json.loads(res.data)

        for actor in data["actors"]:
            if actor["name"] == "Morgan Freeman":
                actor_id = actor["id"]
                break

        res = self.client().delete('actors/{}'.format(actor_id),
                                        headers={
                                            "Authorization": "Bearer {}".format(self.producer)
                                        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(int(data["delete"]), actor_id)

    def test_delete_actors_by_assistant_401_error(self):

        res = self.client().delete('actors/{}'.format(1),
                                        headers={
                                            "Authorization": "Bearer {}".format(self.assistant)
                                        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'invalid_permissions')


    def test_delete_actors_401_error(self):

        res = self.client().delete('actors/{}'.format(1),
                                        headers={})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')

    def test_delete_movies_by_producer(self):
        res = self.client().post('/movies',headers={
                                          "Authorization": "Bearer {}".format(self.producer)
                                      }, json={
                                          "title": "Test Movie Producer",
                                          "release_date": "2011-01-04"
                                      })

        data = json.loads(res.data)

        for movie in data["movies"]:
            if movie["title"] == "Test Movie Producer":
                movie_id = movie["id"]
                break

        res = self.client().delete('movies/{}'.format(movie_id),
                                        headers={
                                            "Authorization": "Bearer {}".format(self.producer)
                                        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(int(data["delete"]), movie_id)

    def test_delete_movies_by_director_401_error(self):

        res = self.client().delete('movies/{}'.format(1),
                                        headers={
                                            "Authorization": "Bearer {}".format(self.director)
                                        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'invalid_permissions')

    def test_delete_movies_by_assistant_401_error(self):

        res = self.client().delete('movies/{}'.format(1),
                                        headers={
                                            "Authorization": "Bearer {}".format(self.assistant)
                                        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'invalid_permissions')


    def test_delete_actors_401_error(self):

        res = self.client().delete('movies/{}'.format(1),
                                        headers={})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')


if __name__ == '__main__':
    unittest.main()

