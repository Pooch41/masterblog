from flask import Flask, render_template, request, redirect, url_for
import json
app = Flask(__name__)


@app.route('/')
def index():

    with open('data/blog.json', 'r') as file:
        blog_posts = json.load(file)

    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        content = request.form['content']
        title = request.form['title']
        with open('data/blog.json', 'r') as file:
            blog_posts = json.load(file)

        #generartes unique ID
        id = blog_posts[-1]['id'] + 1
        all_id = []
        for post in blog_posts:
            all_id.append(post['id'])

        while True: #loop tests that ID is unique, if not, iterates
            if id not in all_id:
                break
            id += 1

        new_post = {
            "id": id,
            "author": name,
            "title": title,
            "content": content
        }

        blog_posts.append(new_post)
        with open('data/blog.json', 'w') as file:
            json.dump(blog_posts, file)

        return redirect(url_for('index'))

    return render_template('add.html' )

@app.route('/delete/<int:post_id>', methods = ['POST'])
def delete(post_id):
    with open('data/blog.json', 'r') as file:
        blog_posts = json.load(file)

    for post in blog_posts:
        if post['id'] == post_id:
            del blog_posts[blog_posts.index(post)]

    with open('data/blog.json', 'w') as file:
        json.dump(blog_posts, file)

    return redirect(url_for('index'))




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)