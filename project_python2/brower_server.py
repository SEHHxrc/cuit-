from flask import Flask
from flask import request  # communicate to client
from flask import render_template  # render the template of page, the template must in the templates
# from flask import redirect, abort, url_for  # used to redirect page and catch web status
import crypto


app = Flask(__name__)  # build an instance


@app.route('/')  # send a parameter which kind of URL can trigger this function(just one function)
def render():
    return render_template('index.html')


@app.route('/encrypt')
def encrypt():
    return render_template('encrypt.html')


@app.route('/encrypted', methods=['GET', 'POST'])  # http's get and post
def encrypted():
    if request.method == 'POST':  # get parameters from form
        message, key = request.form['message'], request.form['key']
    else:  # get parameters from URL
        message, key = request.args.get('message'), request.args.get('key')
    message, message_iv = crypto.formats(message, 'message')
    key, key_iv = crypto.formats(key)
    if key != 'input error' or message != 'input error':
        des = crypto.des()
        cipher = crypto.encrypt(des, key, message)
    else:
        return render_template('error.html', error=message)
    return render_template('encrypt_result.html', cipher=cipher, key=key, message_iv=message_iv, key_iv=key_iv)


@app.route('/decrypt')
def decrypt():
    return render_template('decrypt.html')


@app.route('/decrypted', methods=['GET', 'POST'])
def decrypted():
    if request.method == 'POST':  # get parameters from form
        cipher, key, cipher_iv = request.form['cipher'], request.form['key'], request.form['cipher_iv']
    else:  # get parameters from URL
        cipher, key, cipher_iv = request.args.get('cipher'), request.args.get('key'), request.args.get('cipher_iv')
    cipher_test, test = crypto.formats(cipher, 'message')
    if test or cipher_test != cipher:
        return render_template('error.html', error='cipher error')
    key_test, test = crypto.formats(key, 'key')
    if test or key_test != key:
        return render_template('error.html', error='key error')
    des = crypto.des()
    message = crypto.decrypt(des, key, cipher, cipher_iv)
    return render_template('decrypt_result.html', message=message, key=key)


if __name__ == '__main__':
    app.run(debug=True)  # this function can make this apply run on the localhost
