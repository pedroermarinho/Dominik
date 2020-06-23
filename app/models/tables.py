# from app import db
from app.controllers.database import db


class User(db.Model):
    """

    """
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
    """

    """
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
        return {"name": self.name, "token": self.token}


class DataBase(db.Model):
    """

    """
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
        self.database_url = 'mysql+pymysql://' + str(user) + ':@' + str(password) + '@' + str(host) + '/' + str(
            database)

    def __repr__(self):
        return "<Nome %r>" % self.database_url


class Piada(db.Model):
    """

    """
    __tablename__ = "piadas"
    id = db.Column(db.Integer, primary_key=True)
    piada = db.Column(db.String, unique=True)

    def get_id(self):
        return str(self.id)

    def __init__(self, piada):
        self.piada = piada

    def __repr__(self):
        return "<Nome %r>" % self.piada


class Curiosidade(db.Model):
    """

    """
    __tablename__ = "curiosidades"
    id = db.Column(db.Integer, primary_key=True)
    curiosidade = db.Column(db.String, unique=True)

    def get_id(self):
        return str(self.id)

    def __init__(self, curiosidade):
        self.curiosidade = curiosidade

    def __repr__(self):
        return "<Nome %r>" % self.curiosidade


class Charada(db.Model):
    """

    """
    __tablename__ = "charadas"
    id = db.Column(db.Integer, primary_key=True)
    charada = db.Column(db.String, unique=True)
    resposta = db.Column(db.String)

    def get_id(self):
        return str(self.id)

    def __init__(self, charada, resposta):
        self.charada = charada
        self.resposta = resposta

    def __repr__(self):
        return "<Nome %r>" % self.charada


class Citacao(db.Model):
    """

    """
    __tablename__ = "citacoes"
    id = db.Column(db.Integer, primary_key=True)
    citacao = db.Column(db.String, unique=True)
    autor = db.Column(db.String)

    def get_id(self):
        return str(self.id)

    def __init__(self, citacao, autor):
        self.citacao = citacao
        self.autor = autor

    def __repr__(self):
        return "<Nome %r>" % self.citacao


class Proverbio(db.Model):
    """

    """
    __tablename__ = "proverbios"
    id = db.Column(db.Integer, primary_key=True)
    proverbio = db.Column(db.String, unique=True)
    autor = db.Column(db.String)

    def get_id(self):
        return str(self.id)

    def __init__(self, proverbio, autor):
        self.proverbio = proverbio
        self.autor = autor

    def __repr__(self):
        return "<Nome %r>" % self.proverbio


class Pergunta(db.Model):
    """

    """
    __tablename__ = "perguntas"
    id = db.Column(db.Integer, primary_key=True)
    pergunta = db.Column(db.String, unique=True)
    resposta = db.Column(db.String)

    def get_id(self):
        return str(self.id)

    def __init__(self, pergunta, resposta):
        self.pergunta = pergunta
        self.resposta = resposta

    def __repr__(self):
        return "<Nome %r>" % self.pergunta


class Quiz(db.Model):
    """

    """
    __tablename__ = "quiz"
    id = db.Column(db.Integer, primary_key=True)
    pergunta = db.Column(db.String, unique=True)
    alternativa1 = db.Column(db.String)
    alternativa2 = db.Column(db.String)
    alternativa3 = db.Column(db.String)
    alternativa4 = db.Column(db.String)
    alternativa5 = db.Column(db.String)
    resposta = db.Column(db.Integer)
    url_imagem = db.Column(db.String)

    def get_id(self):
        return str(self.id)

    def __init__(self, pergunta, alternativa1, alternativa2, alternativa3, alternativa4, alternativa5, resposta,
                 url_imagem=None):
        self.pergunta = pergunta
        self.alternativa1 = alternativa1
        self.alternativa2 = alternativa2
        self.alternativa3 = alternativa3
        self.alternativa4 = alternativa4
        self.alternativa5 = alternativa5
        self.resposta = resposta
        self.url_imagem = url_imagem

    def __repr__(self):
        return "<Nome %r>" % self.pergunta

# class Post(db.Model):
#     __tablename__ = "posts"

#     id = db.db.Column(db.db.Integer, primary_key=True)
#     content = db.db.Column(db.Text)
#     user_id = db.db.Column(db.db.Integer, db.ForeignKey('users.id'))

#     # user = db.relationship('User', foreign_key=user_id)

#     def __init__(self, content, user_id):
#         self.content = user_id
#         self.user_id = user_id

#     def __repr__(self):
#         return "Post %r" % self.id


# class Follow(db.Model):
#     __tablename__ = "follow"

#     id = db.db.Column(db.db.Integer, primary_key=True)
#     user_id = db.db.Column(db.db.Integer, db.ForeignKey('users.id'))
#     follower_id = db.db.Column(db.db.Integer, db.ForeignKey('users.id'))

#     # user = db.relationship('User', foreign_key=user_id)
#     # follower = db.relationship('User', foreign_key=follower_id)
