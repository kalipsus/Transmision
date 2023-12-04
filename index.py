from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_socketio import SocketIO
import cv2

app = Flask(__name__)
app.secret_key = '123asd123'
socketio = SocketIO(app)

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        usuario=(request.form['username'])
        contraseña=(request.form['password'])
        if usuario == 'admin' :
            if contraseña=='admin':
                return redirect(url_for('home'))
            else:
                flash("Contraseña incorrecta...")
                return render_template('auth/login.html')
        else:
            flash("Usuario no encontrado...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@app.route('/logout')
def logout():
    return redirect(url_for('login'))


@app.route('/home')
def home():
    return render_template('home.html')
def gen_frames():  
    camera = cv2.VideoCapture(0)  # Usa 0 para la cámara predeterminada
    while True:
        success, frame = camera.read()  # Lee el frame de la cámara
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Concatena los datos del frame

    camera.release()  # Libera la cámara cuando termines

@app.route('/viewer')
def viewer():
    return render_template('viewer.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    socketio.run(app, debug=True)
