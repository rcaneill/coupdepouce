from flask_app import app, db, Classroom, Teacher, Student, Activity, Question, HelpingHand, HelpingHandLog
from flask_login import current_user
from flask import redirect, render_template, url_for, flash, Markup

import markdown
from pathlib import Path

POSTS_DIR = Path('mysite/templates/posts/')

@app.route("/post/")
def list_posts():
    return 'liste des postes'

@app.route("/post/<name>/")
def post(name):
    template = 'templates/posts.html'
    if not (POSTS_DIR / f'{name}.md').exists():
        return redirect(url_for('list_posts'))
    content_file = open(POSTS_DIR / f"{name}.md", "r")
    body = Markup(markdown.markdown(content_file.read())) # Markup is to say to jinja that the string is html
    return render_template(template, body=body)