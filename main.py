from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = '66lshjeIHOI59HJO'
Bootstrap(app)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Create TODO DB
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(500), unique=True, nullable=False)


# with app.app_context():
#     db.create_all()

##Create Formular
class Task(FlaskForm):
    task = StringField("New Task", validators=[DataRequired()])
    submit = SubmitField("Submit")



@app.route("/", methods=["GET", "POST"])
def home():
    form = Task()
    if form.validate_on_submit():
        new_task = Todo(task=form.task.data)
        db.session.add(new_task)
        db.session.commit()
    all_tasks = db.session.query(Todo).all()
    return render_template("index.html", form=form, tasks=all_tasks)

@app.route("/done/<int:index>")
def remove_task(index):
    task_to_delete = Todo.query.get(index)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)