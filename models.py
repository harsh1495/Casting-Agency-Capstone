from sqlalchemy import Integer, String, Boolean, DateTime, ARRAY, Column, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


def setup_db(app):
    '''
    Connect to the database by reading database settings from the config file
    '''
    app.config.from_object('config')
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    return db

ActorMovie = db.Table("actor_movie",
                        db.Column('id', db.Integer, primary_key=True),
                        db.Column('actor_id', db.Integer, db.ForeignKey('actors.id', ondelete='cascade')),
                        db.Column('movie_id', db.Integer, db.ForeignKey('movies.id', ondelete='cascade'))
                    )

class Actor(db.Model):
    '''
    Model that defines an actor and his attributes
    '''
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)

    # movies =  db.relationship("Movie", secondary=ActorMovie, backref=db.backref("actors"))

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'name': self.name,
        'ager': self.age,
        'gender': self.gender
        }

    def __repr__(self):
        return f'<Actor ID: {self.id}, Actor Name: {self.name}>'


class Movie(db.Model):
    '''
    Model that defines a movie and its attributes
    '''
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    actors = db.relationship("Actor", secondary=ActorMovie, backref=db.backref("movies"))

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'title': self.title,
        'release_date': self.release_date
        }

    def __repr__(self):
        return f'<Movie ID: {self.id}, Movie Title: {self.title}>'


# class ActorMovie(db.Model):
#     '''
#     Helper association model for many-to-many relationships
#     '''

