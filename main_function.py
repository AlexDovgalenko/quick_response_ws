import json
from datetime import datetime
from random import randint
from typing import Optional

from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

timer = None
CONFIG_FILE = "config_file.json"
BACKUP_CONFIG_FILE = "default_config_file.json"


class CodeStatus:
    def __init__(self):
        self.__pass_code = None
        self.__is_valid_code = None
        self.__generator_start_time = None
        self.__await_time = None
        self.__access_code = None

    @property
    def pass_code(self):
        if not self.__pass_code:
            with open(CONFIG_FILE, 'r') as config_file:
                config = json.loads(config_file.read())
                self.__pass_code = config["pass_code"]
        return self.__pass_code

    @property
    def validity_status(self) -> bool:
        with open(CONFIG_FILE, 'r') as config_file:
            config = json.loads(config_file.read())
            self.__is_valid_code = config["is_valid_code"]
            return self.__is_valid_code

    @validity_status.setter
    def validity_status(self, status: bool):
        with open(CONFIG_FILE, 'r') as config_file:
            config = json.loads(config_file.read())

        config["is_valid_code"] = status

        with open(CONFIG_FILE, 'w') as config_file:
            json.dump(config, config_file, ensure_ascii=False, indent=4)

    @property
    def generator_start_time(self) -> Optional["datetime"]:
        with open(CONFIG_FILE, 'r') as config_file:
            config = json.loads(config_file.read())
            if not config["generator_start_time"]:
                return None
            self.__generator_start_time = datetime.strptime(config["generator_start_time"], "%Y-%m-%dT%H:%M:%S")
        return self.__generator_start_time

    @generator_start_time.setter
    def generator_start_time(self, start_time: "datetime"):
        with open(CONFIG_FILE, 'r') as config_file:
            config = json.loads(config_file.read())

        config["generator_start_time"] = start_time.strftime("%Y-%m-%dT%H:%M:%S")

        with open(CONFIG_FILE, 'w') as config_file:
            json.dump(config, config_file, ensure_ascii=False, indent=4)

    @property
    def await_time(self) -> int:
        if not self.__await_time:
            with open(CONFIG_FILE, 'r') as config_file:
                config = json.loads(config_file.read())
                self.__await_time = config["await_time"]
        return self.__await_time

    @property
    def access_code(self) -> int:
        if not self.__access_code:
            with open(CONFIG_FILE, 'r') as config_file:
                config = json.loads(config_file.read())
                self.__access_code = config["access_code"]
        return self.__access_code


code_status = CodeStatus()


def check_time():
    if not code_status.generator_start_time:
        return False
    return int((datetime.utcnow() - code_status.generator_start_time).total_seconds()) > code_status.await_time


@app.route("/access_code_gen", methods=["GET"])
def generate_access_code():
    if not code_status.validity_status and not check_time():
        return render_template("pass_form.html")
    if check_time():
        return render_template("result.html", access_code=code_status.access_code)
    return render_template("code_generator.html")


@app.route("/validate_access_code", methods=["POST"])
def validate_pass_code():
    pass_code = request.form["pass-code"]
    if pass_code == code_status.pass_code:
        code_status.validity_status = True
        code_status.generator_start_time = datetime.utcnow()
        return redirect(url_for("generate_access_code"))
    return render_template("error_form.html")


@app.route("/re-enter_access_code", methods=["POST"])
def re_enter_pass_code():
    return redirect(url_for("generate_access_code", access_code=code_status.access_code))


@app.route("/reset_defaults", methods=["GET"])
def reset_defaults():
    with open(BACKUP_CONFIG_FILE, 'r') as backup_file, open(CONFIG_FILE, 'w') as config_file:
        config = json.loads(backup_file.read())
        json.dump(config, config_file, ensure_ascii=False, indent=4)
    return redirect(url_for("generate_access_code"))


@app.route("/generate_response/", methods=["GET"])
def generate_response():
    digit = randint(100, 200)
    text_response = f"Случайное число в диапазоне от 100 до 200: {digit}"
    # return jsonify(str=text_response)
    # return render_template("generator.html", digit=digit)
    return render_template("rnd_digit_generator.html", digit=digit)


if __name__ == "__main__":
    app.run(debug=True)
