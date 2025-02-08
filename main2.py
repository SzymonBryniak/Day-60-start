from flask import Flask, render_template, request
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index2.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")
     

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)



def send_email(uname, uemail, uphone, umessage):
    password = "pmac cmbj xjyc ribw"  # App Password for Gmail
    sender_email = "szymonbryniakproject@gmail.com"
    receiver_email = "oneplusszymonbryniak@gmail.com"
    
    # Create the email message
    msg = MIMEMultipart()
    msg['Subject'] = 'New Contact Form Submission'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Email body content
    body = f"""
    Name: {uname}
    Email: {uemail}
    Phone: {uphone}
    Message: {umessage}
    """

    # Attach the body text to the message
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server and send the email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, password)
            server.sendmail(from_addr=sender_email, to_addrs=receiver_email, msg=msg.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

@app.route("/contact", methods =['GET', 'POST'])
def contact():
    print(f"Request Method: {request.method}")
    try:
        if request.method == "GET" and request.args.get('name'):
            print("Handling GET request...")
            print(request.args.get('name'))
            name = request.args.get('name')
            email = request.args.get('email')
            phone = request.args.get('phone')
            message = request.args.get('message')
            send_email(name, email, phone, message)
            return render_template('contact.html', h1 = "Successfully sent your message. GET")
        
        elif request.method == 'POST' and request.form['name']:
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            message = request.form['message']
            send_email(name, email, phone, message)
            return render_template('contact.html', h1 = "Successfully sent your message. POST")
    
        print(name,"\n",email,"\n",phone,"\n",message)
        send_email(name, email, phone, message)
    except:
        print('No data ')

    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
