import pyautogui
import webbrowser
import cv2
import qrcode
import sqlite3
from time import sleep

# Conectar a la base de datos
conn = sqlite3.connect('registros.db')
cursor = conn.cursor()

# Función para agregar un alumno
def agregar_alumno():
    nombre_alumno = input("Nombre del alumno (o escriba 'salir'): ")
    if nombre_alumno.lower() == 'salir':
        return None  

    telefono = numero_telefono
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

    return contenido_qr, qr_filename, telefono

# Solicitar al usuario el número de teléfono al que se enviará el mensaje
numero_telefono = input("Ingresa el número de teléfono al que deseas enviar el mensaje: ")

# Permitir agregar alumnos y enviar mensajes
while True:
    alumno_data = agregar_alumno()
    if alumno_data is None:
        break

    contenido_qr, qr_filename, telefono = alumno_data

    # Escanear el código QR (como en tu código original)
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

    # Abrir WhatsApp web en el navegador con el número de teléfono ingresado
    webbrowser.open(f'https://web.whatsapp.com/send?phone={telefono}')
    sleep(20)

    # Enviar el código QR a través de WhatsApp
    for i in range(1):
        pyautogui.typewrite(f'Ingreso {qr_filename}')
        pyautogui.press('enter')

# Cerrar la conexión a la base de datos
conn.close()
