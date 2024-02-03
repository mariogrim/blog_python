from sqlalchemy import Column, Integer, String, ForeignKey
import traceback
from flask import Flask, request, jsonify, render_template, Response, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


# Crear el server Flask
app = Flask(__name__)

# Indicamos al sistema (app) de donde leer la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"

# Asociamos nuestro controlador de la base de datos con la aplicacion
db = SQLAlchemy()
db.init_app(app)

class Post(db.Model):
    __tablename__= 'posteos'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String)
    titulo = db.Column(db.String)
    texto = db.Column(db.String)

    def __repr__(self):
        return f"Posteos: {self.usuario}, titulo {self.titulo}, texto {self.texto}"

@app.route("/login")
def login():
    try:
        # Renderizar el temaplate HTML login.html
        print("Renderizar login.html")
        return render_template('login.html')
    except:
        # En caso de falla, retornar el mensaje de error
        return jsonify({'trace': traceback.format_exc()})
   
@app.route("/")
def index():
    try:
        # Renderizar el temaplate HTML bog.html
        print("Renderizar blog.html")
        return render_template('blog.html')
    except:
        # En caso de falla, retornar el mensaje de error
        return jsonify({'trace': traceback.format_exc()})
    

@app.route('/posteos/', methods=['GET', 'POST', 'DELETE'])
def post():
    if request.method == 'GET':
        usuario = request.args.get('usuario')
        posteos = Post.query.filter_by(usuario=usuario).order_by(Post.id.desc()).limit(3).all()
        datos = []
        for posteo in posteos:
            datos.append({"titulo": posteo.titulo, "texto": posteo.texto})
        print('Metodo GET funcionando')
        return jsonify(datos)
    elif request.method == 'POST':
        usuario = request.form.get('usuario')
        titulo = request.form.get('titulo')
        texto = request.form.get('texto')
        posteo = Post(usuario=usuario, titulo=titulo, texto=texto)
        db.session.add(posteo)
        db.session.commit()
        print('Metodo POST funcionando')
        return Response(status=201)
    elif request.method == 'DELETE':
        usuario = request.args.get('usuario')
        Post.query.filter_by(usuario=usuario).delete()
        db.session.commit()
        return Response(status=204)
    

with app.app_context():
    # Crear aquí la base de datos
    db.create_all()
    print("Base de datos generada")

if __name__ == "__main__":

    app.run(host="127.0.0.1", port=5000)
