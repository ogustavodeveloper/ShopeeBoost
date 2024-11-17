from . import db, app
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ContentIdea(db.Model):
    __tablename__ = 'content_ideas'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(200), nullable=False)
    audience = db.Column(db.String(200), nullable=False)
    video_idea = db.Column(db.String(500), nullable=False)
    caption = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='content_ideas')


class ShortenedLink(db.Model):
    __tablename__ = 'shortened_links'
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    shortened_code = db.Column(db.String(10), unique=True, nullable=False)  # Código único numérico
    source = db.Column(db.String(100), nullable=False)  # Fonte do tráfego (Instagram, TikTok, etc.)
    click_count = db.Column(db.Integer, default=0)  # Contador de cliques
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='shortened_links')


class ProductFeedback(db.Model):
    __tablename__ = 'product_feedback'
    id = db.Column(db.Integer, primary_key=True)
    product_url = db.Column(db.String(500), nullable=False)
    audience = db.Column(db.String(500), nullable=False)
    marketing_strategies = db.Column(db.Text, nullable=False)
    viral_video_ideas = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='product_feedback')

class Video(db.Model):
    url = db.Column(db.String(), primary_key=True)
    user = db.Column(db.String())
    product = db.Column(db.String())

    def __init__(self, url, user, product):
        self.url = url 
        self.user = user 
        self.product = product 

class Product(db.Model):
    id = db.Column(db.String(), primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    price = db.Column(db.Float)
    url = db.Column(db.String())
    urlEncurtado = db.Column(db.String())

    # Dados da IA
    analise = db.Column(db.String())
    publico = db.Column(db.String())
    ideias_videos = db.Column(db.String())

    def __init__(self, id, title, description, price, analise, publico, ideias_videos, url, urlEncurtado):
        self.id = id
        self.title = title 
        self.description = description 
        self.price = price 
        self.analise = analise 
        self.publico = publico 
        self.ideias_videos = ideias_videos
        self.url = url
        self.urlEncurtado = urlEncurtado

with app.app_context():
      db.create_all()