from flask import Flask, render_template, request, redirect, url_for
from upload import upload_file_to_s3
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'gltf'}

app = Flask(__name__)

# function to check file extension
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def test():
    return "<p>hello test from docker compsoe</p>"



@app.route('/test')
def test_route():
    return "<p>hello test from docker compsoe</p>"


@app.route('/success')
def test_success():
    return "<p>upload success</p>"


@app.route('/failure')
def test_failure():
    return "<p>failed....</p>"



@app.route("/upload", methods=["POST"])
def create():

    # check whether an input field with name 'user_file' exist
    if 'user_file' not in request.files:
        print('No user_file key in request.files')
        return redirect(url_for('new'))

    # after confirm 'user_file' exist, get the file from input
    file = request.files['user_file']

    # check whether a file is selected
    if file.filename == '':
        print('No selected file')
        return redirect(url_for('new'))

    # check whether the file extension is allowed (eg. png,jpeg,jpg,gif)
    if file and allowed_file(file.filename):
        output = upload_file_to_s3(file) 
        
        # if upload success,will return file name of uploaded file
        if output:
            # write your code here 
            # to save the file name in database

            print("Success upload")
            return redirect(url_for('test_success'))

        # upload failed, redirect to upload page
        else:
            print("Unable to upload, try again")
            return redirect(url_for('test_failure'))
        
    # if file extension not allowed
    else:
        print("File type not accepted,please try again.")
        return redirect(url_for('test_failure'))
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)