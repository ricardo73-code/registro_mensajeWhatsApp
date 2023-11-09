import pyautogui
import webbrowser
import cv2
import qrcode
import sqlite3
from time import sleep

# Conectar a la base de datos
conn = sqlite3.connect('registros.db')
cursor = conn.cursor()

def agregar_alumno():
    nombre_alumno = input("Nombre del alumno (o escriba 'salir'): ")
    if nombre_alumno.lower() == 'salir':
        return None  

    telefono = input("Teléfono del alumno: ")
    numero_cuenta = input("Número de cuenta del alumno: ")

    # Crear el contenido del QR
    contenido_qr = f"Nombre: {nombre_alumno}\nTeléfono: {telefono}\nCuenta: {numero_cuenta}"

    # Generar el código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(contenido_qr)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Guardar la imagen del código QR en un archivo
    qr_filename = f"{nombre_alumno}_qr.png"
    img.save(qr_filename)

    # Insertar los datos en la base de datos
    cursor.execute("INSERT INTO Alumnos (nombre, telefono, cuenta, qr_code) VALUES (?, ?, ?, ?)",
                   (nombre_alumno, telefono, numero_cuenta, qr_filename))
    conn.commit()

    return contenido_qr, qr_filename

while True:
    alumno_data = agregar_alumno()
    if alumno_data is None:
        break

    contenido_qr, qr_filename = alumno_data

    # Escanear el código QR
    print("Escanea el código QR para confirmar el registro.")
    camera = cv2.VideoCapture(1)
    while True:
        ret, frame = camera.read()
        if ret:
            detector = cv2.QRCodeDetector()
            decoded_info, _, _ = detector.detectAndDecode(frame)
            if decoded_info:
                # Compara el contenido del código QR con el contenido del alumno
                if contenido_qr == decoded_info:
                    print("Registro confirmado.")
                    break
                else:
                    print("Código QR no coincide con el registro.")
            cv2.imshow("QR Code Scanner", frame)
        if cv2.waitKey(1) == 27:  # Salir con la tecla Esc
            break
    camera.release()
    cv2.destroyAllWindows()

# Abrir WhatsApp web en el navegador
webbrowser.open('https://web.whatsapp.com/send?phone=+525632507504')
sleep(20)

# Enviar el código QR a través de WhatsApp
for i in range(1):
    pyautogui.typewrite(f'Ingreso {qr_filename}')
    pyautogui.press('enter')

# Cerrar la conexión a la base de datos
conn.close()