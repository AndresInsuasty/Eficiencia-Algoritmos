import requests
import time
from PIL import Image
from io import BytesIO


def fetch_and_display_dog_image() -> float:
    """
    Descarga una imagen aleatoria de perro desde la API y la muestra.

    Returns:
        float: Tiempo de respuesta en segundos
    """
    start_time = time.perf_counter()

    # Hacer solicitud a la API
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    response.raise_for_status()

    end_time = time.perf_counter()
    response_time = end_time - start_time

    # Parsear la respuesta JSON
    data = response.json()
    if data["status"] == "success":
        image_url = data["message"]

        # Descargar y mostrar la imagen
        img_response = requests.get(image_url)
        img_response.raise_for_status()

        img = Image.open(BytesIO(img_response.content))
        img.show()

        print(f"[OK] Imagen descargada exitosamente")
        print(f"URL: {image_url}")
        print(f"Tiempo de respuesta: {response_time:.4f} segundos ({response_time*1000:.2f} ms)")
    else:
        print("✗ Error en la respuesta de la API")

    return response_time


if __name__ == "__main__":
    fetch_and_display_dog_image()
