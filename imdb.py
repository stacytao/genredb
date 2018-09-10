from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<any(title, name):type>/<id>')
def profile(type, id):
    return render_template('profile.html', type=type, id=id)


@app.route('/<any(title, name):type>/create')
def create(type):
    return render_template('create.html', type=type)


@app.route('/<any(title, name):type>/<id>/edit')
def edit(type, id):
    return render_template('edit.html', type=type, id=id)


@app.route('/<any(title, name):type>/<id>/save')
def save(type, id):
    return


@app.route('/<any(title, name):type>/<id>/delete')
def delete(type, id):
    return
