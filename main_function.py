from random import randint

from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

is_valid_code = False
timer = None
PASS_CODE = "QX4ED7"


@app.route("/access_code_gen", methods=["GET"])
def generate_access_code():
    if not is_valid_code:
        return render_template("pass_form.html")
    return render_template("generator_3.html")


@app.route("/validate_access_code", methods=["POST"])
def validate_pass_code():
    pass_code = request.form["pass-code"]
    global is_valid_code
    if pass_code == PASS_CODE:
        is_valid_code = True
        return redirect(url_for("generate_access_code"))
    return render_template("pass_form.html")


@app.route("/generate_response/", methods=["GET"])
def generate_response():
    digit = randint(100, 200)
    text_response = f"Случайное число в диапазоне от 100 до 200: {digit}"
    # return jsonify(str=text_response)
    # return render_template("generator.html", digit=digit)
    return render_template("generator_2.html", digit=digit)


if __name__ == "__main__":
    app.run(debug=True)
