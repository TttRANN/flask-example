from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello,World"


@app.route("/login", methods={"GET", "POST"})
def login():
    if request.method == "GET":
        return render_template("02.html")
        if request.method == "POST":
            return "Login!"

    if __name__ == '__main__':
        app.run(debug=True)
