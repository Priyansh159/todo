from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "your_secret_key"  # Needed for flash messages
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo("Asia/Kolkata")))

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        titlee = request.form.get('title', '').strip()
        descc = request.form.get('desc', '').strip()

        if not titlee or not descc:
            flash("Title and Description cannot be empty.", "error")
            return redirect('/')

        todo = Todo(title=titlee, desc=descc)
        db.session.add(todo)
        db.session.commit()
        flash("Todo added successfully!", "success")
        
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if not todo:
        flash("Todo not found.", "error")
        return redirect('/')

    if request.method == 'POST':
        titlee = request.form.get('title', '').strip()
        descc = request.form.get('desc', '').strip()

        if not titlee or not descc:
            flash("Title and Description cannot be empty.", "error")
            return redirect(f'/update/{sno}')

        todo.date_created = datetime.now(ZoneInfo("Asia/Kolkata"))
        todo.title = titlee
        todo.desc = descc
        db.session.commit()
        flash("Todo updated successfully!", "success")
        return redirect("/")
    
    return render_template('update.html', todo=todo)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if not todo:
        flash("Todo not found.", "error")
        return redirect('/')

    db.session.delete(todo)
    db.session.commit()
    flash("Todo deleted successfully!", "success")
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
