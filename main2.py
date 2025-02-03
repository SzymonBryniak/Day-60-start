from flask import Flask, render_template, request
import requests
# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index2.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/contact", methods =['GET', 'POST'])
def receive_data():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']
    print(name,"\n",email,"\n",phone,"\n",message)
    if request.method == 'POST':
        return render_template('message.html', h1 = "Successfully sent your message. POST")
    elif request.method == 'GET':
        return render_template('message.html', h1 = "Successfully sent your message. GET")


if __name__ == "__main__":
    app.run(debug=True)
