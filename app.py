from flask import Flask ,request,render_template,redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///post.db'# this is for creating db file for posts
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Blogpost(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    title =db.Column(db.String(100),nullable=False)
    content =db.Column(db.Text,nullable=False)
    author2 =db.Column(db.String(20),nullable=False,default='N/A')
    user=db.Column(db.String(20),nullable=True,default='user')
    password=db.Column(db.String(20),nullable=True,default='user')
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return 'blog post '+str(self.id)+' created..'

class account(db.Model):

    user=db.Column(db.String(20),nullable=False,primary_key=True)
    password=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(40),nullable=False)






@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post',methods=['GET','POST'])
def post():
    if request.method=='POST':
        post_title=request.form['title']
        post_content=request.form['content']
        post_author=request.form['author']
        new_post=Blogpost(title=post_title,content=post_content,author2=post_author)
        db.session.add(new_post)
        db.session.commit()  #this will permently add data to database
        user=Blogpost.query.filter_by(author2=request.form['author'])
        return render_template('blogs.html',posts=user)
        #return redirect('/')
    else :
        all_posts=Blogpost.query.order_by(Blogpost.date_posted)
        return render_template('post.html',posts=all_posts)

@app.route('/blogs',methods=['GET'])
def blogs():
    all_posts=Blogpost.query.order_by(Blogpost.date_posted).all()
    #all_posts=Blogpost.query.filter_by(user=user)
    return render_template('blogs.html',posts=all_posts)




@app.route('/post/delete/<int:id>/<author>')
def delete(id,author):
    #post=Blogpost.query.get(id)
    #n=Blogpost.query.all()[id].author2
    db.session.delete(Blogpost.query.get_or_404(id))
    db.session.commit()
    user=Blogpost.query.filter_by(author2=author)
    return render_template('blogs.html',posts=user,name=author)
    


@app.route('/post/edit/<int:id>/<author>',methods=['GET','POST'])
def edit(id,author):
    post=Blogpost.query.get_or_404(id)
    if request.method=='POST':
        post.title=request.form['title']
        post.content=request.form['content']
        post.author2=request.form['author']
        db.session.commit()
        user=Blogpost.query.filter_by(author2=author)
        return render_template('blogs.html',posts=user,name=author)


    else:
        return render_template('edit.html',post=post)


@app.route('/login',methods=['GET','POST'])
def login():
    return render_template('login.html')


@app.route('/submit',methods=['POST'])
def submit():
    #form=Blogpost()
    name=request.form['user']
    user=account.query.filter_by(user=request.form['user']).first()
    if user:
        if user.password==request.form['password']:
            user=Blogpost.query.filter_by(author2=request.form['user'])
            return render_template('blogs.html',posts=user,name=name)
        else:
            return '<h1> invalid password</h1>'
    else:
            return '<h1> invalid username</h1>'

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=='POST':
            post_user=request.form['user']
            post_password=request.form['password']
            post_email=request.form['email']
            new_user=account(user=post_user,password=post_password,email=post_email)
            db.session.add(new_user)
            db.session.commit()  #this will permently add data to database
            return redirect('/login')
    else:
        return render_template('signup.html')

        


        



if __name__=="__main__":
    app.run(debug=True)