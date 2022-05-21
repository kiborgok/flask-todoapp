from flask import Flask, render_template, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/todosapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'todos'   
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Todo: Id: {self.id}, description: {self.description}>'

@app.route('/todos/create', methods=['POST'])
def create_todo():   
   body={}
   error = False
   try: 
       description =  request.get_json()['description']
       todo = Todo(description=description)
       db.session.add(todo)
       db.session.commit()
       body['description'] = todo.description
   except:        
        error = True
        db.session.rollback()
        print(sys.exc_info())
   finally:
        db.session.close()           
        if  error == True:
            abort(400)
        else:           
            return jsonify(body)

@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=3000)