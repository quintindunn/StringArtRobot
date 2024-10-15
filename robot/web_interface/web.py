import pathlib

from flask import Flask, render_template, request
import os

app = Flask(__name__,
            template_folder="./web/templates/",
            static_folder="./web/static/")

UPLOAD_FOLDER = pathlib.Path("./stringart_files/").absolute()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("upload/upload_file.html")

    file = request.files['files']

    if file and file.filename.endswith('.stringart'):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return "File uploaded successfully!"
    return render_template("upload/upload_file.html")


if __name__ == '__main__':
    app.run("0.0.0.0", port=8080, debug=True)