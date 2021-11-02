# For the purpose of styling I have used Symentic ui
from flask import Flask, render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Setting the config variable
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' ## the three  backward slash means that it is a realtive path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # creating the acutall datbase

'''Creating class for to-do item'''
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route('/')
def index(): 
    # Show all todo's
    todo_list = Todo.query.all() # this will return list of all the items
    return render_template('base.html', todo_list = todo_list)
@app.route('/add', methods=["POST"])
def add():
    # add new item
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/update/<int:todo_id>')    
def update(todo_id):
    todo = Todo.query.filter_by(id = todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))  

@app.route('/delete/<int:todo_id>')    
def delete(todo_id):
    todo = Todo.query.filter_by(id = todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))
  
if __name__ == "__main__":
    db.create_all() # Creating database
    
    # new_todo = Todo(title = "todo 1", complete = False)
    # db.session.add(new_todo)
    # db.session.commit()
    app.run(debug=True) 