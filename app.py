from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__)

# Database URI setup
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(ZoneInfo("Asia/Kolkata")))

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Automatically create the database (for development purposes only)
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        # Debug: Log received form data
        titlee = request.form['title']
        descc = request.form['desc']
        print(f"Received title: {titlee}, description: {descc}")  # Debug log
        todo = Todo(title=titlee, desc=descc)
        db.session.add(todo)
        db.session.commit()
    
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    try:
        if request.method == 'POST':
            titlee = request.form['title']
            descc = request.form['desc']
            todo = Todo.query.filter_by(sno=sno).first()
            todo.date_created = datetime.now(ZoneInfo("Asia/Kolkata"))
            todo.title = titlee
            todo.desc = descc
            db.session.commit()
            return redirect("/")
        
        todo = Todo.query.filter_by(sno=sno).first()
        return render_template('update.html', todo=todo)

    except Exception as e:
        print(f"Error: {e}")  # Debug log
        return str(e), 500

@app.route('/delete/<int:sno>')
def delete(sno):
    try:
        todo = Todo.query.filter_by(sno=sno).first()
        db.session.delete(todo)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f"Error: {e}")  # Debug log
        return str(e), 500

# For favicon.ico handling (in case you don't have one)
@app.route('/favicon.ico')
def favicon():
    return '', 204  # Returns no content for favicon requests

if __name__ == "__main__":
    # Debugging: Print when server starts
    print("Starting the Flask app...")
    app.run(debug=True)
