from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

app = Flask(__name__)
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


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        # print(request.form['title'])
        titlee = request.form['title']
        descc = request.form['desc']
        todo = Todo(title=titlee, desc=descc)
        db.session.add(todo)
        db.session.commit()
        
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)  # Correct way to render an HTML file



# @app.route('/bootstrap/')
# def bootstrap():
#     return render_template('boot.html')

@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return "this is product page"

@app.route('/update/<int:sno>',methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        titlee = request.form['title']
        descc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.date_created = datetime.now(ZoneInfo("Asia/Kolkata"))
        todo.title = titlee
        todo.desc = descc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=False)