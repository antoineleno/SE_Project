from flask import Flask, redirect, render_template, url_for

app = Flask(__name__)

@app.route('/')
def profile():
    return render_template("teacher_course.html")

if __name__ == '__main__':
    app.run(debug=True)
