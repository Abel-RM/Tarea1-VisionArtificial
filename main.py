import numpy as np
import cv2

cap = cv2.VideoCapture(0)

def deteccion_color(frame, ret):
    while ret:
        Im1lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        L = Im1lab[:, :, 0]
        a = Im1lab[:, :, 1]  # Tomamos canal a (verdes negativo (0-127) y rojos positivo (128-25))
        b = Im1lab[:, :, 2]  # tomamos canal b (positivos amarillo, negativos azules)

        a = np.double(a)
        b = np.double(b)
        a = a - 128
        b = b - 128

        # Detección de azules
        z = np.bitwise_and(b < 0, np.abs(b) > np.abs(a))

        new_a = a
        new_b = b
        # Se invierte el signo de los canales 'a' y 'b' para obtener el color verde
        new_a[z == 1] *= -1
        new_b[z == 1] *= -1

        Im1lab[:, :, 0] = L
        Im1lab[:, :, 1] = new_a + 128
        Im1lab[:, :, 2] = new_b + 128

        Im1lab = np.uint8(Im1lab)
        Im2 = cv2.cvtColor(Im1lab, cv2.COLOR_LAB2BGR)

        return Im2


while True:
    ret, frame = cap.read()

    img = deteccion_color(frame, ret)

    cv2.imshow('Original', frame)
    cv2.imshow('Cambio de color', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
