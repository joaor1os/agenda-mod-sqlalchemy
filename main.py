from flask import Flask, render_template, request, redirect, session

from flask_sqlalchemy import SQLAlchemy

app = Flask('app')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class users(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String())
  email = db.Column(db.String())
  password = db.Column(db.String())
  created_at = db.Column(db.String())
  updated_at = db.Column(db.String())

class contacts(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100))
  name = db.Column(db.String())
  email = db.Column(db.String())
  phone = db.Column(db.String())
  image = db.Column(db.String())
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  created_at = db.Column(db.String())
  updated_at = db.Column(db.String())
  

@app.route('/')
def index():
  contact = contacts.query.all()
  return render_template(
    'index.html',
    contacts=contact
  )

@app.route('/create/', methods=['POST'])
def create():
  name = request.form.get('name')
  email = request.form.get('email')
  phone = request.form.get('phone')
  
  new_contacts = contacts(
    name=name,
    email=email,
    phone=phone
  )
  db.session.add(new_contacts)
  db.session.commit()
  return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
  name = request.form.get('name')
  email = request.form.get('email')
  phone = request.form.get('phone')

  contact = contacts.query.filter_by(id=id).first()
  contact.name = name
  contact.email = email
  contact.phone = phone
  db.session.commit()
  return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
  contact = contacts.query.filter_by(id=id).first()
  db.session.delete(contact)
  db.session.commit()
  return redirect('/')

if __name__ == '__main__':
  db.create_all()
  app.run(host='0.0.0.0', port=8080) 