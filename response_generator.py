from random import randint

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/generate_response/", methods=["GET"])
def generate_response():
    digit = randint(100, 200)
    text_response = f"Случайное число в диапазоне от 100 до 200: {digit}"
    # return jsonify(str=text_response)
    # return render_template("generator.html", digit=digit)
    return render_template("generator_3.html", digit=digit)


if __name__ == "__main__":
    app.run(debug=True)
