#
# Correction: Technologies Web serie-07
# Author: Peterson Yuhala <petersonyuhala@gmail.com>
#

from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chat.db"

db = SQLAlchemy(app)


#
# NB: flask creates constructors for python classes that inherit from db.Model
# but we will still create the constructors anyway for clarify
#
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, name, email):
        self.name = name
        self.email = email


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text)
    pub_date = db.Column(db.DateTime, default=db.func.now())
    

    def __init__(self, author, content, date):
        self.author = author
        self.content = content
        self.pub_date = date
        # self.time = time


#
# create the databases and tables
# if you do changes to models and wish to mirror them to the db, you will have to drop
# the dbs with db.drop_all()
# both db.drop_all() and db.create_all() don't need to be recalled again once the db has been created.
#

'''
with app.app_context():
    #db.drop_all()
    db.create_all()
'''


#
# GET route to show home page
#
@app.route("/")
def home():
    return render_template("home.html")


# @app.route("/login")
# def login():
#     return render_template("login.html")

#
# GET route to show edit page
# the commend id is passed as a parameter to the GET route
#
@app.route("/edit/<int:comment_id>")
def edit_page(comment_id):
    comment = Comment.query.get(comment_id)
    return render_template("edit.html", comment=comment)


#
# GET route to show profile page
#
@app.route("/profile")
def profile():
    # comments = Comment.query.filter_by(author = session['name']).all()
    comments = Comment.query.all()  
    name=session['name']
    email=session['email']   
    return render_template("profile.html", all_comments=comments, name=name)


#
# POST route to create new user in db
#
@app.route("/register", methods=["POST"])
def register():
    name = request.form["name"]
    email = request.form["email"]
    user = User(name, email)
    session["name"] = request.form["name"]
    session["email"] = request.form["email"]

    db.session.add(user)
    db.session.commit()

    return redirect(url_for("profile"))

#
# POST route to add new comment in db
#
@app.route("/add-comment", methods=["POST"])
def add_comment():
    content = request.form["comment"]
    author = session["name"]
    date = datetime.today()
    comment = Comment(author, content, date)

    db.session.add(comment)
    db.session.commit()
    return redirect(url_for("profile"))

#
# POST route to update/edit existing comment 
#
@app.route("/edit-comment/<int:comment_id>", methods=["POST"])
def edit_comment(comment_id):
    new_content = request.form["comment"]
    # get comment object from database
    comment_object = Comment.query.get(comment_id)
    # update comment content
    comment_object.content = new_content
    db.session.commit()
    return redirect(url_for("profile"))


#
# POST route to delete comment from db
#
@app.route("/delete-comment/<int:comment_id>", methods=["POST"])
def delete_comment(comment_id):
    Comment.query.filter(Comment.id == comment_id).delete()   
    db.session.commit()
    return redirect(url_for("profile"))


# you can run app with python3 chat.py
if __name__ == "__main__":
    app.debug = True
    app.run()
