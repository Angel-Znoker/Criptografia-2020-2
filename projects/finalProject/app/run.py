# export FLASK_APP=node_server.py
# flask run --port 8000
# export FLASK_APP=run.py
# flask run

from flask import Flask
from flask import render_template, request, redirect, url_for, jsonify
from forms import SignupForm, PostForm,LoginForm
from werkzeug.urls import url_parse
from models import User
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
import hashlib
import requests
import json
import datetime

# Creación de la instancia
# __name__: Nombre del módulo o paquete de la aplicación
app = Flask(__name__)

app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

posts = []
numposts = 0

CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8000"

def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["hash"] = block["previous_hash"]
                content.append(tx)

        global posts
        posts = sorted(content, key=lambda k: k['timestamp'],
                       reverse=True)

# Decorador route encargado de indicar a Flask qué URL debe ejecutar su correspondiente función
@app.route('/')
def index():
	return render_template("base_template.html")

@app.route('/admin/post/', methods=["GET", "POST"])
@login_required
def post_form():
    form = PostForm()

    global numposts

    if form.validate_on_submit():
        total = form.total.data
        content = form.content.data

        post_object = {"author": current_user.name, "content": content, "total": total}

        numposts += 1

        new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

        requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})

        return redirect(url_for('post_form'))

    return render_template('admin/post_form.html', form = form)

@app.route('/admin/postShopping', methods=["POST"])
@login_required
def postShopping():

    new_tx_address = "{}/new_transaction_".format(CONNECTED_NODE_ADDRESS)

    response = requests.post(new_tx_address,
                  json=request.get_json(),
                  headers={'Content-type': 'application/json'})

    if response.status_code == 201:
        return jsonify({
            "status": 201
        })

    return jsonify({
        "status": 400
    })

@app.route('/admin/lectura/', methods=["GET", "POST"])
@login_required
def post_read():
    fetch_posts()

    if current_user.is_admin:
        return render_template('admin/post_read.html', title = 'Ventas realizadas', posts = posts, node_address=CONNECTED_NODE_ADDRESS, readable_time=timestamp_to_string)

    return redirect(url_for('index'))

# Flask responde por defecto ante peticiones GET. Si se quiere responder otro tipo de petición, se debe indicar con el parámetro methods
@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if not current_user.is_admin:
        return redirect(url_for('index'))

    form = SignupForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        # Creamos el usuario y lo guardamos
        user_id = int(hashlib.md5(email.encode()).hexdigest()[:8], 16)

        user = User(user_id, name, email, password)

        # Guardar en la base de datos los datos del usuario
        user.register(user)

        # Dejamos al usuario logueado
        # login_user(user, remember=True)

        next_page = request.args.get('next', None)

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)
    return render_template("signup_form.html", form=form)


@app.route("/admin/deleteUser", methods=["GET"])
def deleteUser():
    if not current_user.is_admin:
        return redirect(url_for('index'))

    return render_template("admin/delete_user.html")

@app.route("/getSellers", methods=["GET"])
def getSellers():
    return jsonify({
        "users": User.getUsers()
    })

@app.route("/deleteAuser", methods=["POST"])
def deleteAuser():
    content = request.get_json()

    if not User.deleteUser(content["email"]):
        return "Error", 400
    return "User Deleted", 200

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():

        userInfo = User.get_by_email(form.email.data, form.password.data)

        if userInfo is not None:

            user = User(userInfo.get('user_id'), userInfo.get('name'), userInfo.get('email'), userInfo.get('password'), userInfo.get('is_admin'))
            user.set_object(user)

            login_user(user, remember=form.remember_me.data)

            next_page = request.args.get('next')

            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')

            return redirect(next_page)
    return render_template('login_form.html', form=form)

@app.route('/logout')
def logout():

    mine = "{}/mine".format(CONNECTED_NODE_ADDRESS)
    requests.get(mine)

    logout_user()
    return redirect(url_for('index'))

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%a, %B %d, %Y %H:%M')

@app.route('/defServer', methods=['POST'])
def defServer():
    global CONNECTED_NODE_ADDRESS
    content = request.get_json()
    if "server" not in content:
        return "Error", 400
    CONNECTED_NODE_ADDRESS = content["server"]
    print(CONNECTED_NODE_ADDRESS)
    return "Success", 200


@app.route('/getServer', methods=['GET'])
def getServer():
    return jsonify({
        "server":CONNECTED_NODE_ADDRESS
    })

app.run(debug=True)
