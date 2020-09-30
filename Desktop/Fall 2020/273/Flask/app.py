# import flask
from flask import Flask, render_template, url_for, request,redirect
# import databse
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# set up our application
# reference this file
app = Flask(__name__)

# tell our app where our database is located
# sqlite:/// relative path, reside in the project location 
# sqlite://// absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# initial the database
db = SQLAlchemy(app)


#create a model
class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(200),nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    #get a function when we create the string everytime, we create a new element
    def __repr__(self):
        #return task, and the id of the task that just been created
        return '<Task %r>' % self.id



# create an index route
# @app.route('/')
@app.route('/',methods=['POST','GET'])
# define function for that route
def index():
    if request.method =='POST':
        #create a variable call task_content
        # content is the name in index.html-> form
        task_content = request.form['content']
        #create a Todo object
        new_task = Todo(content=task_content)
        
        try:
            # add this to the database
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        # create a variable called tasks, 
        # query in our database, ordering them by the day create
        tasks = Todo.query.order_by(Todo.date_created).all()
        #pass the tasks to the template
        return render_template('index.html',tasks=tasks)
       

if __name__ == "__main__":
    # if there are any errors they will pop up on the webpage
    app.run(debug=True)