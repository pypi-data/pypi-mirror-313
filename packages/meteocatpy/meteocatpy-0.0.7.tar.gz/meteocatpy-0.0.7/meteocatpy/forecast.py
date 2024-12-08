import aiohttp
from .const import (
    BASE_URL,
    MUNICIPIS_HORA_URL,
    MUNICIPIS_DIA_URL
)
from .exceptions import (
    BadRequestError,
    ForbiddenError,
    TooManyRequestsError,
    InternalServerError,
    UnknownAPIError
)

class MeteocatForecast:
    """Clase para interactuar con las predicciones de la API de Meteocat."""

    def __init__(self, api_key: str):
        """
        Inicializa la clase MeteocatForecast.

        Args:
            api_key (str): Clave de API para autenticar las solicitudes.
        """
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "X-Api-Key": self.api_key,
        }

    async def _fetch_data(self, url: str):
        """
        Método genérico para realizar solicitudes a la API.

        Args:
            url (str): URL de la API a consultar.

        Returns:
            dict: Respuesta JSON de la API.
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        return await response.json()

                    # Gestionar errores según el código de estado
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
                        raise UnknownAPIError(f"Unexpected error {response.status}: {await response.text()}")
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

    async def get_prediccion_horaria(self, town_id: str):
        """
        Obtiene la predicción horaria a 72 horas para un municipio.

        Args:
            town_id (str): Código del municipio.

        Returns:
            dict: Predicción horaria para el municipio.
        """
        url = f"{BASE_URL}{MUNICIPIS_HORA_URL.format(codi=town_id)}"
        return await self._fetch_data(url)

    async def get_prediccion_diaria(self, town_id: str):
        """
        Obtiene la predicción diaria a 8 días para un municipio.

        Args:
            town_id (str): Código del municipio.

        Returns:
            dict: Predicción diaria para el municipio.
        """
        url = f"{BASE_URL}{MUNICIPIS_DIA_URL.format(codi=town_id)}"
        return await self._fetch_data(url)

    @staticmethod
    def procesar_prediccion(prediccion_json):
        """
        Procesa el JSON de predicción y organiza los datos por variables.

        Args:
            prediccion_json (dict): JSON devuelto por la API de predicción.

        Returns:
            dict: Datos organizados por variables.
        """
        datos_por_variable = {}

        # Iterar sobre los días en el JSON
        for dia in prediccion_json.get("dies", []):
            fecha = dia.get("data")

            for variable, valores in dia.get("variables", {}).items():
                if "valors" in valores:  # Predicción horaria
                    for valor in valores["valors"]:
                        nombre_variable = variable
                        if nombre_variable not in datos_por_variable:
                            datos_por_variable[nombre_variable] = []
                        datos_por_variable[nombre_variable].append({
                            "fecha": valor["data"],
                            "valor": valor["valor"],
                            "unidad": valores.get("unitat", ""),
                        })
                else:  # Predicción diaria
                    nombre_variable = variable
                    if nombre_variable not in datos_por_variable:
                        datos_por_variable[nombre_variable] = []
                    datos_por_variable[nombre_variable].append({
                        "fecha": fecha,
                        "valor": valores["valor"],
                        "unidad": valores.get("unitat", ""),
                    })

        return datos_por_variable
