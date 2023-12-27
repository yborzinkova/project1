from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__,template_folder='templates')
app.config['SEND_FILE_MAX_AGE_DEFAULT']
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Article(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    intro=db.Column(db.String(300),nullable=False)
    text=db.Column(db.Text,nullable=False)
    data=db.Column(db.DateTime,default=datetime)

    def __repr__(self):
        return '<Article%r>'% self.id





@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/about')
def about():#put application's code here
    return render_template("about.html")

@app.route('/posts/<int:id>')
def post_detail(id):
    article=Article.query.get(id)
    return render_template('post_detail.html',article=article)

@app.route('/create_article',methods=['POST','GET'])
def create_article():
    if request.method == "POST":
        title=request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        article=Article(title=title,intro=intro,text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except Exception as err:
            print(err)
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template("create_article.html")

if __name__=='__main__':
    app.run(debug=True)





