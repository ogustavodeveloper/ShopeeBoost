from flask import Blueprint, render_template
from app.routes import main_bp

@main_bp.route('/')
def home():
    return render_template('index.html')

@main_bp.route('/about')
def about():
    return render_template('about.html')
