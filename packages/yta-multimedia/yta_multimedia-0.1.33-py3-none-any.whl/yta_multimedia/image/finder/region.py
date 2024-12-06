import numpy as np
import cv2


class RegionFinder:
    @staticmethod
    def detect_regions(image, low_range, high_range):
        # Convertir la imagen de BGR a HSV
        imagen_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Crear una máscara con los píxeles que están dentro del rango de color
        mascara = cv2.inRange(imagen_hsv, low_range, high_range)
        
        # Encontrar los contornos de las regiones detectadas
        contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Dibujar los contornos sobre la imagen original
        imagen_contornos = image.copy()
        for contorno in contornos:
            if cv2.contourArea(contorno) > 100:  # Filtrar contornos pequeños
                cv2.drawContours(imagen_contornos, [contorno], -1, (0, 255, 0), 2)
        
        return imagen_contornos, mascara

    @staticmethod
    def test():
        imagen = cv2.imread('imagen.jpg')

        # Definir el rango de color en HSV (por ejemplo, un verde brillante)
        rango_bajo = np.array([35, 50, 50])   # El valor mínimo del verde en HSV
        rango_alto = np.array([85, 255, 255])  # El valor máximo del verde en HSV

        # Llamar a la función para detectar las regiones del color
        imagen_contornos, mascara = RegionFinder.detect_regions(imagen, rango_bajo, rango_alto)

        # Mostrar los resultados
        cv2.imshow('Regiones Detectadas', imagen_contornos)
        cv2.imshow('Máscara', mascara)

        # Esperar a que se presione una tecla para cerrar las ventanas
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # TODO: This above need working, is using a HSV mask to
    # recognize regions, but this is actually a new class
    # to bring functionality from 'yta_general_utils'