from yta_multimedia.image.region.image_region import ImageRegion
from yta_general_utils.image.color.picker import PixelFilterFunction
from yta_general_utils.image.parser import ImageParser
from typing import Union
from PIL import Image

import numpy as np
import cv2


MIN_REGION_SIZE = (1920 / 20, 1080 / 20)
"""
The minimum size a region must have to be accepted
as a valid region.
"""

class ImageRegionFinder:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    @classmethod
    def is_valid(cls, x, y, image, visited, filter_func: callable):
        """
        This method verifies if the pixel is between the limits
        and is transparent and unvisited.
        """
        rows, cols, _ = image.shape

        return (0 <= x < rows and 0 <= y < cols and not visited[x, y] and filter_func(image[x, y]))

    @classmethod
    def dfs(cls, image: np.ndarray, visited, x, y, region, filter_func: callable):
        """
        A Deep First Search algorithm applied to the image to 
        obtain all the pixels connected in a region.
        """
        if not isinstance(image, np.ndarray):
            raise Exception('The provided "image" parameter is not a valid np.ndarray.')

        stack = [(x, y)]
        visited[x, y] = True
        region.append((x, y))
        
        while stack:
            cx, cy = stack.pop()
            for dx, dy in cls.directions:
                nx, ny = cx + dx, cy + dy
                if cls.is_valid(nx, ny, image, visited, filter_func):
                    visited[nx, ny] = True
                    region.append((nx, ny))
                    stack.append((nx, ny))

    @classmethod
    def is_inside(cls, small_bounds, large_bounds):
        """
        This method verifies if the bounds of a found region are
        inside another bounds to discard the smaller regions.
        """
        min_x_small, max_x_small, min_y_small, max_y_small = small_bounds
        min_x_large, max_x_large, min_y_large, max_y_large = large_bounds
        
        return (
            min_x_small >= min_x_large and max_x_small <= max_x_large and
            min_y_small >= min_y_large and max_y_small <= max_y_large
        )

    @classmethod
    def find_regions(cls, image: np.ndarray, filter_func: PixelFilterFunction) -> list[ImageRegion]:
        """
        This method looks for all the existing regions of transparent
        pixels that are connected ones to the others (neighbours). The
        'filter_func' parameter is the one that will classify the pixels
        as, for example, transparent or green. That 'filter_func' must
        be a method contained in the PixelFilterFunction class.

        This method returns the found regions as objects with 'top_left'
        and 'bottom_right' fields that are arrays of [x, y] positions
        corresponding to the corners of the found regions.
        """
        if not isinstance(image, np.ndarray):
            raise Exception('The provided "image" parameter is not a valid np.ndarray.')

        rows, cols, _ = image.shape
        visited = np.zeros((rows, cols), dtype=bool)
        regions = []
        
        for row in range(rows):
            for col in range(cols):
                # If we find a transparent pixel, we search
                if filter_func(image[row, col]) and not visited[row, col]:
                    region = []
                    cls.dfs(image, visited, row, col, region, filter_func)

                    for i, p in enumerate(region):
                        if i == 10:
                            break
                    
                    if region:
                        min_x = min(px[0] for px in region)
                        max_x = max(px[0] for px in region)
                        min_y = min(px[1] for px in region)
                        max_y = max(px[1] for px in region)

                        # These are the limits of the region
                        bounds = (min_x, max_x, min_y, max_y)
                        
                        # We need to avoid small regions contained in others and
                        # also use a minimum size to accept a region as valid
                        if max_x - min_x >= MIN_REGION_SIZE[0] and max_y - min_y >= MIN_REGION_SIZE[1] and not any(cls.is_inside(bounds, r['bounds']) for r in regions):
                            regions.append({
                                'bounds': bounds
                            })

        # I want another format, so:
        for index, region in enumerate(regions):
            regions[index] = ImageRegion(region['bounds'][2], region['bounds'][0], region['bounds'][3], region['bounds'][1])

        return regions
    
    @classmethod
    def find_green_regions(cls, image: Union[str, Image.Image, np.ndarray]) -> list[ImageRegion]:
        """
        This method returns the found green regions as objects with
        'top_left' and 'bottom_right' fields that are arrays of [x, y] 
        positions corresponding to the corners of the found regions.
        """
        image = ImageParser.to_numpy(image, 'RGB')
            
        return cls.find_regions(image, PixelFilterFunction.is_green)
    
    @classmethod
    def find_transparent_regions(cls, image: Union[str, Image.Image, np.ndarray]) -> list[ImageRegion]:
        """
        This method returns the found transparent regions as objects
        with 'top_left' and 'bottom_right' fields that are arrays of
        [x, y] positions corresponding to the corners of the found
        regions.
        """
        image = ImageParser.to_numpy(image, 'RGBA')
            
        return cls.find_regions(image, PixelFilterFunction.is_transparent)









# TODO: This below need work, is using a HSV mask to
# recognize regions, but this is actually a new class
# to bring functionality from 'yta_general_utils'

class RegionFinderTest:
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
        imagen_contornos, mascara = RegionFinderTest.detect_regions(imagen, rango_bajo, rango_alto)

        # Mostrar los resultados
        cv2.imshow('Regiones Detectadas', imagen_contornos)
        cv2.imshow('Máscara', mascara)

        # Esperar a que se presione una tecla para cerrar las ventanas
        cv2.waitKey(0)
        cv2.destroyAllWindows()

