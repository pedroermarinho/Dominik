from app import db



class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email

    def __repr__(self):
        return "<User %r>" % self.username


class TelegramToken(db.Model):
    __tablename__ = "telegramtokens"
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, unique=True)
    name = db.Column(db.String)
    
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False


    def get_id(self):
        return str(self.id)

    def __init__(self, name, token):
        self.name = name
        self.token = token

    def __repr__(self):
        return {"name":self.name,"token":self.token}


class DataBase(db.Model):
    __tablename__ = "databases"
    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String)
    database = db.Column(db.String)
    user = db.Column(db.String)
    password = db.Column(db.String)
    database_url = db.Column(db.String, unique=True)


    def get_id(self):
        return str(self.id)

    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.database_url = 'mysql+pymysql://'+str(user)+':@'+str(password)+'@'+str(host)+'/'+str(database)
        

    def __repr__(self):
        return "<Nome %r>" % self.name


# class Post(db.Model):
#     __tablename__ = "posts"

#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.Text)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

#     # user = db.relationship('User', foreign_key=user_id)

#     def __init__(self, content, user_id):
#         self.content = user_id
#         self.user_id = user_id

#     def __repr__(self):
#         return "Post %r" % self.id


# class Follow(db.Model):
#     __tablename__ = "follow"

#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     follower_id = db.Column(db.Integer, db.ForeignKey('users.id'))

#     # user = db.relationship('User', foreign_key=user_id)
#     # follower = db.relationship('User', foreign_key=follower_id)

