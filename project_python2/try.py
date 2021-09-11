from flask import Flask
from flask import request # communicate to client
from flask import render_template # render the template of page, the template must in the templates
from flask import redirect, abort, url_for # used to redirect page and catch web status


app = Flask(__name__) # build an instance


@app.route('/') # send a parameter which kind of URL can trigger this function(just one function)
def render():
    return render_template('index.html')


@app.route('/hello/<username>') # send a variable parameter
def hello(username):
    return 'Hello %s' % username


@app.route('/upload', methods=['GET', 'POST']) # http's get and post
def upload():
    if request.method == 'POST': # get parameters from form
        cipher = request.form['key'] + request.form['message'] 
        return cipher
    else: # get parameters from URL
        print request.args.get('message'), request.args.get('key')
        cipher = request.args.get('message') + request.args.get('key')
        return cipher


@app.route('/upload_files', methods=['GET', 'POST']) # upload files, which needs html form set enctype="multipart/form-data"
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('upload/' + f.filename)


@app.route('/index')
def index():
    return redirect(url_for('forbidden'))


@app.route('/forbidden')
def forbidden():
    abort(401) # return http status


if __name__ == '__main__':
    app.run(debug = True) # this function can make this apply run on the localhost
