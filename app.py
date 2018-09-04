from flask import Flask,render_template,flash,request
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SECRET_KEY'] = "random string"

db=SQLAlchemy(app)

class users(db.Model):
    id= db.Column('user_id',db.Integer, primary_key=True)
    mail=db.Column(db.String(100))
    name=db.Column(db.String(100))
    pss=db.Column(db.String(100))

    def __init__(self,name,mail,pss):
        self.mail = mail
        self.name = name
        self.pss  = pss

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/view',methods=['POST'])
def view():
    if request.method == 'POST':
      if not request.form['mail'] or not request.form['name'] or not request.form['pss']:
         flash('Please enter all the fields', 'error')
      else:
         user = users(request.form['mail'], request.form['name'],
            request.form['pss'])
         
         db.session.add(user)

         db.session.commit()
         flash('REGISTRATION SUCCESSFUL')
         return render_template('loginform.html')
    return 'error_method'
 
@app.route('/all')
def all():
     return render_template('view.html', users = users.query.all())



@app.route('/signinform')
def sign():
    return render_template('loginform.html')


@app.route('/login' ,methods=['POST'])
def login():
    if request.method == 'POST':
      if not request.form['mail'] or not request.form['pss']:
         flash('Please enter all the fields', 'error')
      else:
         ma=request.form['mail']
         ps=request.form['pss']
         user = users.query.filter_by(mail=ma,pss=ps).first()
         if user is not None:
           return "LOGIN SUCCESFUL"
         else :
           return "INVALID EMAIL OR PASSWORD"

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)
