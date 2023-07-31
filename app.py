from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# Custom filter to convert UTC time to IST in the template
@app.template_filter('utc_to_ist')
def utc_to_ist(value):
    if value is not None:
        utc_time = value.replace(tzinfo=pytz.utc)
        ist_time = utc_time.astimezone(pytz.timezone('Asia/Kolkata'))
        return ist_time.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return ""

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200),nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, server_default=db.func.now())
    def __repr__(self):
        return '<Task %r>' % self.id
    


@app.route('/', methods=['POST','GET'])
def index():
    if request.method=='POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content, date_created=datetime.utcnow())

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error adding your task"
        
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting that task"
    
@app.route('/update/<int:id>', methods=['GET','POST'])

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
        return render_template('update.html',task=task)
     

if __name__ == "__main__":
    app.run(debug=True)
