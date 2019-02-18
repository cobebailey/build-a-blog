from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Cobe@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.String(600))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        tit_err = ''
        blog_err = ''
        title_name = request.form['title']
        blog_body = request.form['blog']
        if title_name == '' or blog_body == '':
            if title_name == '':
                tit_err = 'Error: Your blog was empty!'
            if blog_body == '':
                blog_err = 'Error: Your blog was empty!'
            return render_template('blog.html', title='Build a  blog', body=blog_body, tit_err=tit_err, blog_err=blog_err, btitle=title_name )
        else:
            new_blogb = Blog(title_name, blog_body)
            db.session.add(new_blogb)
            db.session.commit()
            blogs = Blog.query.all()
            return redirect('/blog?id={0}'.format(new_blogb.id))
    else:
        return render_template('blog.html')

@app.route('/blog')
def display_blogs():

    blogs = Blog.query.all()

    return render_template('main.html', title = "Blogs!", blogs = blogs)

@app.route('/blog')
def display_blog():
    blog_id = request.args.get('id')
    blog = Blog.query.get(blog_id)
    return render_template('post.html', title = "Blogs!", blog = blog)

@app.route('/deletarate', methods=['POST'])
def deletarate():

    blog_id = int(request.form['blog-id'])
    blog = Blog.query.get(blog_id)
    db.session.delete(blog)
    db.session.commit()

    return redirect('/blogs')


if __name__ == '__main__':
    app.run()