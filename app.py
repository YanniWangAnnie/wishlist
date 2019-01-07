from flask import Flask, render_template, request
from werkzeug.exceptions import BadRequest
from flask_sqlalchemy import SQLAlchemy
import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=os.environ['DATABASE_URL']
app.debug = True
db = SQLAlchemy(app)

class Item(db.Model):
    __tablename__='items'
    item_id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(1000))
    description=db.Column(db.String(100000))
    state=db.Column(db.String(100))
    date=db.Column(db.TIMESTAMP,default=datetime.datetime.utcnow)

@app.route('/')
def index():
    items=Item.query.order_by(Item.date.desc())
    return render_template('index.html', items=items)
    
@app.route('/add_item')
def add_items():
    return render_template("add_item.html")

@app.route('/post_item',methods=['POST'])
def post_item():
    if request.form['auth'] == os.environ['AUTH']:
        item = Item()
        item.title=request.form['title']
        item.description=request.form['description']
        item.state='active'
        db.session.add(item)
        db.session.commit()
        return 'success'
    else:
        return 'wrong auth token'

if __name__ == '__main__':
    app.run()