from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random

app = Flask(__name__)
# 'postgresql://postgres:password@localhost/databasename'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1AB1bbkim#@localhost/taskmaster'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://onxhdhrfpiljdm:bbf1add091793add6603ec7e0bc4ac7b443ddb443017118a7d1d1cbfdd3aedd9@ec2-54-145-185-178.compute-1.amazonaws.com:5432/dbmjljjha9jee1'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)
    return


@app.route('/random')
def random_select():
    tasks = Todo.query.all()
    choice = random.choice(tasks)
    return render_template('random.html', choice=choice)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
