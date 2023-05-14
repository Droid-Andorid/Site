from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    #Создание колонок
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    text = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id

@app.route("/")
def start_screen():
    return render_template("start.html")


@app.route('/state')
def index():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("home.html", articles=articles)


@app.route("/create_comment", methods=["POST", "GET"])
def create_comment():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        article = Article(title=title, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/state')
        except:
            return "При додаванні коментаря виникла проблема"
    else:
        return render_template("create_comment.html")


@app.route("/state/<int:id>/update", methods=['POST', 'GET'])
def update_comment(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect("/state")
        except:
            return "При оновлені коментаря виникла проблема"
    else:
        return render_template("update_comment.html", article=article)


@app.route("/state/<int:id>/delete", methods=['POST', 'GET'])
def delete_comment(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect("/state")
    except:
        return "При видалені коментаря виникла проблема"


if __name__=="__main__":
    app.run(debug=True)