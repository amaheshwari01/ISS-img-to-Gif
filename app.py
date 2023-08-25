import os
from datetime import datetime
from flask import Flask, request, redirect, send_file, url_for
from werkzeug.utils import secure_filename
import shutil
import imageio.v2 as imageio
from waitress import serve

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'


def move_jpg_files(source_folder, destination_folder):
    print(os.walk(source_folder))
    for root, dirs, files in os.walk(source_folder):

        for file in files:
            if file.lower().endswith('.jpg'):
                source_path = os.path.join(root, file)
                destination_path = os.path.join(destination_folder, file)
                shutil.move(source_path, destination_path)
                # print(f"Moved {source_path} to {destination_path}")


def generate_images(img_dir):
    dir_list = sorted(os.listdir(img_dir))
    images = []


    for filename in dir_list:
        images.append(imageio.imread(img_dir+"/"+filename))

    imageio.mimsave(img_dir+'/movie.gif', images)
    return img_dir+'/movie.gif'

@app.route('/', methods=['GET'])
def upload_form():
    return '''
    <html>
        <body>
            <form action = "/upload" method = "POST" enctype = "multipart/form-data">
                <input type = "file" name = "file" multiple/>
                <input type = "submit"/>
            </form>   
        </body>
    </html>
    '''


@app.route('/upload', methods=['POST'])
def upload_directory():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    new_dir_path = os.path.join(app.config['UPLOAD_FOLDER'], timestamp)
    os.makedirs(new_dir_path, exist_ok=True)

    file = request.files.getlist("file")[0]

    filename = secure_filename(file.filename)
    new_dir_path=os.path.join(new_dir_path, filename)
    file.save(new_dir_path)

    return redirect(url_for('show_path', path=new_dir_path))


@app.route('/path/<path:path>')
def show_path(path):
    dir_path = os.path.dirname(path)

    shutil.unpack_archive('./'+path, './'+dir_path+'/out')
    os.makedirs('./'+dir_path+'/imgout', exist_ok=True)
    move_jpg_files('./'+dir_path+'/out', './'+dir_path+'/imgout')
    return send_file(generate_images( './'+dir_path+'/imgout'))
    


def run():
    # app.run(debug=False)

    serve(app, host='0.0.0.0', port=8080)
