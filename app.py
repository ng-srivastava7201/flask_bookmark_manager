from flask import Flask, render_template ,request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bmlist.db'
db = SQLAlchemy(app)

class BkmList(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  link = db.Column(db.Text, nullable=False)
  name = db.Column(db.String(20))
  date_added = db.Column(db.DateTime, default=db.func.now())

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    link_content = request.form['link']
    link_name = request.form['name']
    new_task = BkmList(link=link_content, name=link_name)
    try:
      db.session.add(new_task)
      db.session.commit()
      return redirect('/')
    except:
      return 'There was some error'
  else:
    items = BkmList.query.order_by(BkmList.date_added).all()
    return render_template('index.html', items=items)

@app.route('/delete/<int:id>')
def delete(id):
  task = BkmList.query.get_or_404(id)
  try:
    db.session.delete(task)
    db.session.commit()
    return redirect('/')
  except:
    return "There was some error"

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
  task = BkmList.query.get_or_404(id)
  if request.method == 'POST':
    task.link = request.form['link']
    task.name = request.form['name']
    try:
      db.session.commit()
      return redirect('/')
    except:
      return "There was some error"
  else:
    return render_template('update.html', item=task)

with app.app_context:
  db.create_all()

if __name__ == '__main__':
  app.run(debug=True)
