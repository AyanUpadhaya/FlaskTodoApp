from flask import Flask,render_template,url_for,request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#add database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tasks.db'

#initialize db

db = SQLAlchemy(app)

#create model
class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	task = db.Column(db.String(100),nullable = False)
	date_added = db.Column(db.DateTime, default=datetime.utcnow)

	#create string

	def __repr__(self):
		return '<Task %r>' %self.id

#add task
@app.route('/',methods=["POST","GET"])
def index():
	if request.method == "POST":
		task_content = request.form['content']
		new_task=Todo(task=task_content)
		try:
			db.session.add(new_task)
			db.session.commit()
			return redirect('/')
		except:
			return "There was a problem adding your task"

	else:
		tasks = Todo.query.order_by(Todo.date_added).all() # fetchisng all data
		return render_template('index.html',title="Todo App", tasks = tasks)


@app.route('/delete/<int:id>')
def delete(id):
	task_to_delete = Todo.query.get_or_404(id)
	try:
		db.session.delete(task_to_delete)
		db.session.commit()
		return redirect('/')
	except:
		return "There was a problem in deleting that task"


#add task
@app.route('/update/<int:id>',methods=["POST","GET"])
def update(id):
	#get the task first for updating
	task = Todo.query.get_or_404(id)
	if request.method == "POST":
		task.task = request.form['content']
		try:
			db.session.commit()
			return redirect('/')
		except:
			return "There was a problem updating your task"

	else:
		return render_template('update.html',title="Update", task = task)

if __name__=="__main__":
	app.run(debug=True)