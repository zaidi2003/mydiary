from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
@app.route('/', methods = ['POST','GET'])
def home():
    if request.method == 'POST':
        entry_title   = request.form['title']
        entry_content = request.form['content']
        new_entry = Things(title = entry_title ,content = entry_content)

        try:
            db.session.add(new_entry)
            db.session.commit()
            return redirect('/')
        except:
            return "didnt work"
    else:
        entries = Things.query.order_by(Things.date_created).all()
        return render_template('home.html',entries=entries)


class Things(db.Model):
    id           = db.Column(db.Integer, primary_key = True)
    title        = db.Column(db.String(200), nullable=False)
    content      = db.Column(db.String(400), nullable = False)
    completed    = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    def __repr__(self):
        return '<Entry %r>' % self.id

@app.route("/delete/<int:id>")
def delete(id):
    entry_to_delete = Things.query.get_or_404(id)

    try:
        db.session.delete(entry_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "we faced a problem"

@app.route("/view/<int:id>", methods = ['GET'])
def view(id):
    entry = Things.query.get_or_404(id)
    current_title = entry.title
    current_content = entry.content
    return render_template('view.html', entry=entry)




@app.route("/update/<int:id>", methods=['GET','POST'])
def update(id):
    entry = Things.query.get_or_404(id)

    if request.method == 'POST':
        entry.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "issue"

    else:
        return render_template('update.html', entry=entry)




if __name__ == "__main__":
    app.run(debug=True)
