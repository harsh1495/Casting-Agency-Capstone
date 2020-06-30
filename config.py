# Connect to the database
SCHEME = 'postgresql'
DATABASE_NAME = "capstone"
USER = "capstoneuser"
PASSWORD = "capstonepass123"
HOST = "localhost"
PORT = 5432

SQLALCHEMY_DATABASE_URI = f'{SCHEME}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}'
SQLALCHEMY_TRACK_MODIFICATIONS = False