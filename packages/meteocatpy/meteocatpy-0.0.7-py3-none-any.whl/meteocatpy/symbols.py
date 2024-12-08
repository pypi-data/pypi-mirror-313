import aiohttp
from .const import BASE_URL, SYMBOLS_URL
from .exceptions import BadRequestError, ForbiddenError, TooManyRequestsError, InternalServerError, UnknownAPIError


class MeteocatSymbols:
    """Clase para interactuar con la API de símbolos de Meteocat."""

    def __init__(self, api_key: str):
        """
        Inicializa la clase MeteocatSymbols.

        Args:
            api_key (str): Clave de API para autenticar las solicitudes.
        """
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "X-Api-Key": self.api_key,
        }
        self.symbols_map = {}

    async def fetch_symbols(self):
        url = f"{BASE_URL}{SYMBOLS_URL}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        print(data)  # Esto te mostrará la estructura completa en la consola

                        # Asegurarse de que `data` sea una lista de categorías
                        if isinstance(data, list):
                            self.symbols_map = {}
                            for category in data:
                                if "valors" in category:
                                    # Guardamos los valores de cada categoría
                                    self.symbols_map[category["nom"]] = category["valors"]
                            return data  # Devolvemos todo el conjunto de datos

                        else:
                            raise UnknownAPIError(f"Unexpected structure of data: {data}", status_code=response.status)

                    # Gestionar errores de respuesta
                    if response.status == 400:
                        raise BadRequestError(await response.json())
                    elif response.status == 403:
                        error_data = await response.json()
                        if error_data.get("message") == "Forbidden":
                            raise ForbiddenError(error_data)
                        elif error_data.get("message") == "Missing Authentication Token":
                            raise ForbiddenError(error_data)
                    elif response.status == 429:
                        raise TooManyRequestsError(await response.json())
                    elif response.status == 500:
                        raise InternalServerError(await response.json())
                    else:
                        raise UnknownAPIError(f"Unexpected error {response.status}: {await response.text()}", status_code=response.status)

            except aiohttp.ClientError as e:
                raise UnknownAPIError(
                    message=f"Error al conectar con la API de Meteocat: {str(e)}",
                    status_code=0,
                )

            except Exception as ex:
                raise UnknownAPIError(
                    message=f"Error inesperado: {str(ex)}",
                    status_code=0,
                )



    def get_description(self, category: str, code: int) -> str:
        """
        Obtiene la descripción de un código de símbolo dentro de una categoría.

        Args:
            category (str): Nombre de la categoría (e.g., "cel").
            code (int): Código del símbolo.

        Returns:
            str: Descripción del símbolo. Retorna 'Desconocido' si el código no está en el mapeo.
        """
        category_symbols = self.symbols_map.get(category, [])
        for symbol in category_symbols:
            if symbol["codi"] == str(code):  # El código es devuelto como string por la API
                return symbol["descripcio"]
        return "Desconocido"
