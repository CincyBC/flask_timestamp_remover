from flask import Flask, request, render_template, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
path = os.getcwd()
clean_path = os.path.join(path, 'cleaned')
ALLOWED_EXTENSIONS = set(['txt'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_location = os.path.join(path, filename)
            file.save(save_location)
            try:
                for files in os.listdir(clean_path):
                    os.remove(file)
            except:
                pass
            try:
                original_file = open(save_location, "r", encoding="utf8")
                print('opened file')
                text = original_file.readlines()
                original_file.close()
                print('closed file')
                os.remove(save_location)
                # Get list of indices with timestamp-like objects, reverse order and remove
                listofindices = []
                for x in range(len(text)):
                    try:
                        if text[x][2] and text[x][5] == ':':
                            listofindices.append(x)
                    except IndexError:
                        pass
                print('finished pulling timestamps')
                listofindices.sort(reverse=True)
                for x in range(len(listofindices)):
                    text.remove(text[listofindices[x]])
                print('finished removing timestamps')

                # Create a new file, write the new contents, and close it
                new_file = open(os.path.join(clean_path, 'cleaned_' + filename), "w")
                new_file_contents = "".join(text)

                new_file.write(new_file_contents)
                new_file.close()
                print('ready to respond')

                return send_from_directory(clean_path, 'cleaned_' + filename, as_attachment=True)


            except Exception as e:
                print('Invalid File')

    return render_template('index.html'), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True, static_folder="static/")