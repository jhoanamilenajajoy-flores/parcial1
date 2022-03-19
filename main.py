
from flask import Flask, render_template, request, redirect,flash
import mysql.connector,hashlib
import email
from smtplib import SMTP
from email.message import EmailMessage

db= mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="carta_virtual",
    port=3306, 
)
cursor=db.cursor(dictionary=True)




def guardar(nombre,email,email2,contra):
    print(nombre)
    print(email)
    print(email2)
    print(contra)
    

    contra_Encripted = hashlib.sha256(contra.encode())
    print(contra_Encripted.hexdigest())
    cursor.execute('''INSERT INTO clientes(nombre,email,contraseña) VALUES (%s,%s,%s); ''',(nombre,email,str(contra_Encripted.hexdigest())))
    db.commit()
    cursor.close()
    flash("Correo no concuerda")
        

def buscar_usuario(nombre):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM `clientes` WHERE email=%s"),(nombre)
    usuario=cursor.fetchall()
    return usuario
def buscar_contra(contra):
    contra_Encripted = hashlib.sha256(contra.encode())
    print(contra_Encripted.hexdigest())
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM `clientes` WHERE contrasena=%s"),(str(contra_Encripted.hexdigest()))
    contras = cursor.fetchall()
    return contras


app = Flask(__name__, template_folder = './templates' , static_folder = './templates' )
app.secret_key="jhon"
@app.get("/")
def inicio():
    return render_template("index.html")
@app.post("/registro")
def registro():
   data=request.form
   if data["email"]==data["email2"]:
       msg = EmailMessage()
       msg.set_content('Verificacion correo')
       msg['Subject'] = 'Su cuenta se ha creado con exito'
       msg['From'] = 'juanpuentes2020@itp.edu.co'
       msg['To'] = data["email"]

       username = 'juanpuentes2020@itp.edu.co'
       password = '1002462375'

       server = SMTP('smtp.gmail.com:587')
       server.starttls()
       server.login(username, password)
       server.send_message(msg)
       server.quit()

       guardar(
           nombre=data["nombre"],
           email=data["email"],
           email2=data["email2"],
           contra=data["contra"])
   else:
       flash("es incorrecto")
       print("es incorrecto")


   return redirect("/ingreso")


@app.route("/ingreso",methods=['GET','POST'])
def ingreso():
    return render_template("iniciar_sesion.html")

app.route("/ingreso",methods=['GET','POST'])
def inicios():
    dato = request.form

    user=buscar_usuario(
        nombre=dato["usuario"]
       )
    contra=buscar_contra( contra=dato["contras"])




app.run(debug=True)
