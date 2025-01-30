from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///expense.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Expense(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    category = db.Column(db.String(100),nullable=False)
    amount = db.Column(db.Integer,nullable=False)
    date = db.Column(db.DateTime,nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.category}"

with app.app_context():
    db.create_all()

@app.route("/", methods=['GET','POST'])
def home():
    if request.method == 'POST':
        category = request.form['category']
        amount = request.form['expense']  
        date = request.form['date']

        if not category or not amount or not date:
            return "All fields are required!"
        try:
            date = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return "Invalid Amount Format!"
        
        category = category.lower()
        expense =Expense(category=category,amount=amount,date=date)
        db.session.add(expense)
        db.session.commit()

    expenses = Expense.query.all()
    return render_template("index.html", expenses=expenses)

@app.route("/summary")
def summary():
    expenses = Expense.query.all()

    totalExp = sum(expense.amount for expense in expenses)

    category_summary = {}
    for expense in expenses:
        category = expense.category
        category = category.capitalize()
        category_summary[category] = category_summary.get(category, 0) + expense.amount

    return render_template('summary.html', expenses=expenses, totalExp=totalExp, category_summary=category_summary)

@app.route("/delete/<int:sno>")
def delete(sno):
    expense = Expense.query.get(sno)
    if not expense:
        return "Expense not found!", 404
    db.session.delete(expense)
    db.session.commit()
    return redirect("/summary")

@app.route('/show')
def products():
    expenses = Expense.query.all()
    print(expenses)

if __name__=="__main__":
    app.run(debug=True)