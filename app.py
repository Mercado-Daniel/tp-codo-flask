from flask import Flask ,jsonify ,request
# del modulo flask importar la clase Flask y los métodos jsonify,request
from flask_cors import CORS       # del modulo flask_cors importar CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app=Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend


# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://acuastel:eoraptor5193@acuastel.mysql.pythonanywhere-services.com/acuastel$proyecto'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow


class Product(db.Model):   # la clase Producto hereda de db.Model
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    title=db.Column(db.String(100))
    description=db.Column(db.String(400))
    price=db.Column(db.Integer)
    stock=db.Column(db.Integer)
    brand=db.Column(db.String(100))
    category=db.Column(db.String(100))
    imagen1=db.Column(db.String(400))
    imagen2=db.Column(db.String(400))
    imagen3=db.Column(db.String(400))
    def __init__(self,title,price, description,stock, brand,category,imagen1,imagen2,imagen3):   #crea el  constructor de la clase
        self.title=title   # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.description=description
        self.price=price
        self.stock=stock
        self.brand=brand
        self.category=category
        self.imagen1=imagen1
        self.imagen2=imagen2
        self.imagen3=imagen3

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(100))
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    direccion = db.Column(db.String(100))
    telefono = db.Column(db.Integer)
    email = db.Column(db.String(100))
    contrasena = db.Column(db.String(100))
    saldo = db.Column(db.Integer)
    def __init__(self,usuario, nombre, apellido, direccion, telefono, email, contrasena, saldo):
        self.usuario = usuario
        self.nombre = nombre
        self.apellido =apellido
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
        self.contrasena = contrasena
        self.saldo = saldo



    #  si hay que crear mas tablas , se hace aqui




with app.app_context():
    db.create_all()  # aqui crea todas las tablas
#  ************************************************************
class ProductSchema(ma.Schema):
    class Meta:
        fields=('id','title','description','price','stock','brand','category','imagen1','imagen2','imagen3')




product_schema=ProductSchema()            # El objeto producto_schema es para traer un producto
products_schema=ProductSchema(many=True)  # El objeto productos_schema es para traer multiples registros de producto

class ClienteSchema(ma.Schema):
    class Meta:
        fields = ('id', 'usuario', 'nombre', 'apellido', 'direccion', 'telefono', 'email', 'contrasena', 'saldo')

cliente_schema = ClienteSchema()
clientes_schema = ClienteSchema(many=True)



# crea los endpoint o rutas (json)
@app.route('/products',methods=['GET'])
def get_Products():
    all_products=Product.query.all()         # el metodo query.all() lo hereda de db.Model
    result=products_schema.dump(all_products)  # el metodo dump() lo hereda de ma.schema y
                                                 # trae todos los registros de la tabla
    return jsonify(result)                       # retorna un JSON de todos los registros de la tabla

@app.route('/clientes', methods=['GET'])
def get_Clientes():
    all_clientes = Cliente.query.all()
    result=clientes_schema.dump(all_clientes)

    return jsonify(result)


@app.route('/products/<id>',methods=['GET'])
def get_product(id):
    product=Product.query.get(id)
    return product_schema.jsonify(product)   # retorna el JSON de un producto recibido como parametro

@app.route('/clientes/<id>', methods=['GET'])
def get_cliente(id):
    cliente=Cliente.query.get(id)
    return cliente_schema.jsonify(cliente)



@app.route('/products/<id>',methods=['DELETE'])
def delete_product(id):
    product=Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)   # me devuelve un json con el registro eliminado

@app.route('/clientes/<id>', methods=['DELETE'])
def delete_cliente(id):
    cliente=Cliente.query.get(id)
    db.session.delete(cliente)
    db.session.commit()
    return cliente_schema.jsonify(cliente)


@app.route('/products', methods=['POST']) # crea ruta o endpoint
def create_product():
    #print(request.json)  # request.json contiene el json que envio el cliente
    title=request.json['title']
    description=request.json['description']
    price=request.json['price']
    stock=request.json['stock']
    brand=request.json['brand']
    category=request.json['category']
    imagen1=request.json['imagen1']
    imagen2=request.json['imagen2']
    imagen3=request.json['imagen3']
    new_product=Product(title,description,price,stock,brand,category,imagen1,imagen2,imagen3)
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)

@app.route('/clientes', methods=['POST'])
def create_cliente():
    usuario=request.json['usuario']
    nombre=request.json['nombre']
    apellido=request.json['apellido']
    direccion=request.json['direccion']
    telefono=request.json['telefono']
    email=request.json['email']
    contrasena=request.json['contrasena']
    saldo=request.json['saldo']
    new_cliente=Cliente(usuario,nombre,apellido,direccion,telefono,email,contrasena,saldo)
    db.session.add(new_cliente)
    db.session.commit()
    return cliente_schema.jsonify(new_cliente)


@app.route('/products/<id>' ,methods=['PUT'])
def update_product(id):
    product=Product.query.get(id)

    product.title=request.json['title']
    product.description=request.json['description']
    product.price=request.json['price']
    product.stock=request.json['stock']
    product.brand=request.json['brand']
    product.category=request.json['category']
    product.imagen1=request.json['imagen1']
    product.imagen2=request.json['imagen2']
    product.imagen2=request.json['imagen2']


    db.session.commit()
    return product_schema.jsonify(product)

@app.route('/clientes/<id>', methods=['PUT'])
def update_cliente(id):
    cliente=Cliente.query.get(id)

    cliente.usuario = request.json['usuario']
    cliente.nombre = request.json['nombre']
    cliente.apellido = request.json['apellido']
    cliente.direccion = request.json['direccion']
    cliente.telefono = request.json['telefono']
    cliente.email = request.json['email']
    cliente.contrasena = request.json['contrasena']
    cliente.saldo = request.json['saldo']

    db.session.commit()
    return cliente_schema.jsonify(cliente)

@app.route('/')
def hello_world():
    return 'Trabajo practico final codo a codo'

