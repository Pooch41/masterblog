from flask import Flask, render_template, request, redirect, url_for, flash
import json

app = Flask(__name__)
app.secret_key = "not_so_secret"
@app.route('/')
def index():

    with open('data/blog.json', 'r', encoding='utf-8') as file:
        blog_posts = json.load(file)

    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        content = request.form['content']
        title = request.form['title']
        with open('data/blog.json', 'r', encoding='utf-8') as file:
            blog_posts = json.load(file)

        #generartes unique ID
        if blog_posts:
            id = blog_posts[-1]['id'] + 1
        else:
            id = 1

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
            "content": content,
            "likes": 0
        }

        blog_posts.append(new_post)
        with open('data/blog.json', 'w', encoding='utf-8') as file:
            json.dump(blog_posts, file, indent=4)
        flash("Post added successfully!")
        return redirect(url_for('index'))

    return render_template('add.html' )

@app.route('/delete/<int:post_id>', methods = ['POST'])
def delete(post_id):
    with open('data/blog.json', 'r', encoding='utf-8') as file:
        blog_posts = json.load(file)

    for post in blog_posts:
        if post['id'] == post_id:
            del blog_posts[blog_posts.index(post)]
            break

    with open('data/blog.json', 'w', encoding='utf-8') as file:
        json.dump(blog_posts, file, indent=4)
    flash("Post deleted successfully!")
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    def fetch_post_by_id(id_of_post):
        with open('data/blog.json', 'r', encoding='utf-8') as file:
            posts = json.load(file)

        for blog_post in posts:
            if blog_post['id'] == id_of_post:
                return blog_post

        return None

    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    likes = post['likes']
    if request.method == 'POST':
        with open('data/blog.json', 'r', encoding='utf-8') as file:
            blog_posts = json.load(file)

        for post in blog_posts:
            if post['id'] == post_id:
                del blog_posts[blog_posts.index(post)]

        name = request.form['author']
        content = request.form['content']
        title = request.form['title']
        new_post = {
            "id": post_id,
            "author": name,
            "title": title,
            "content": content,
            "likes": likes
        }


        blog_posts.append(new_post)
        with open('data/blog.json', 'w', encoding='utf-8') as file:
            json.dump(blog_posts, file, indent=4)

        flash("Post updated successfully!")
        return redirect(url_for('index'))
    return render_template('update.html', post=post)

@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    with open('data/blog.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    for post in data:
        if post['id'] == post_id:
            post['likes'] += 1
            break

    with open('data/blog.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    flash("Now that's a good post!")
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)