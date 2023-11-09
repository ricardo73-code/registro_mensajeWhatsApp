import cv2

# Abre la cámara, 0 es el índice de la cámara (normalmente la cámara web integrada)
cap = cv2.VideoCapture(0)

# Verifica si la cámara se ha abierto correctamente
if not cap.isOpened():
    print("No se pudo abrir la cámara.")
    exit()

while True:
    # Captura un fotograma de la cámara
    ret, frame = cap.read()

    # Si no se pudo capturar el fotograma, sal del bucle
    if not ret:
        print("No se pudo capturar el fotograma.")
        break

    # Muestra el fotograma en una ventana
    cv2.imshow("Cámara", frame)

    # Si se presiona la tecla 'q', sale del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera la cámara y cierra la ventana
cap.release()
cv2.destroyAllWindows()
