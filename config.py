DEBUG = False # True for development
SECRET_KEY = "your secret key"

ADMIN_USERNAME = 'username of the admin'

##############
# SQL database
##############
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="your username",
    password="your password",
    hostname="your hostname",
    databasename="your database name",
)
SQLALCHEMY_POOL_RECYCLE = 299
SQLALCHEMY_TRACK_MODIFICATIONS = False

############
# flask mail
############
MAIL_SERVER='smtp.your_mail_server.com'
MAIL_PORT = 465 # whaterver is the port
MAIL_USERNAME = 'username@your_mail_server.com'
MAIL_PASSWORD = 'your password'
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_SENDER = 'username@your_mail_server.com'