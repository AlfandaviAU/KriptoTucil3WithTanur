from flask import Flask, render_template, request, redirect, url_for
from forms import Todo
from steganography import *
from modified_rc4 import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'


@app.route('/', methods=['GET', 'POST'])
def main():
    request_method = request.method
    return render_template('index.html',request_method=request_method)


@app.route('/rc4', methods=['GET', 'POST'])
def page_rc4():
    request_method = request.method
    return render_template('rc4.html',request_method=request_method)


@app.route('/stegano', methods=['GET', 'POST'])
def page_stegano():
    request_method = request.method
    return render_template('stegano.html',request_method=request_method)

@app.route('/process_stegano', methods=['GET', 'POST'])
def process_stegano():
    request_method = request.method
    return render_template('stegano.html',request_method=request_method)



# @app.route('/name/<string:first_name>')
# def name(first_name):
#     return f'{first_name}'

# @app.route('/todo', methods=['GET','POST'])
# def todo():
#     todo_form = Todo()
#     return render_template('todo.html', form=todo_form)


if __name__ == '__main__':
    app.run(debug=True)
    