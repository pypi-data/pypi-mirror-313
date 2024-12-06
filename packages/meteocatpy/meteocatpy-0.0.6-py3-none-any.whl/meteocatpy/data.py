import aiohttp
from datetime import datetime
from .variables import MeteocatVariables
from .const import BASE_URL, STATION_DATA_URL
from .exceptions import (
    BadRequestError,
    ForbiddenError,
    TooManyRequestsError,
    InternalServerError,
    UnknownAPIError,
)


class MeteocatStationData:
    """Clase para interactuar con los datos de estaciones de la API de Meteocat."""

    def __init__(self, api_key: str):
        """
        Inicializa la clase MeteocatStationData.

        Args:
            api_key (str): Clave de API para autenticar las solicitudes.
        """
        self.api_key = api_key
        self.headers = {"X-Api-Key": self.api_key}
        self.variables = MeteocatVariables(api_key)
    
    @staticmethod
    def get_current_date():
        """
        Obtiene la fecha actual en formato numérico.

        Returns:
            tuple: Año (YYYY), mes (MM), día (DD) como enteros.
        """
        now = datetime.now()
        return now.year, now.month, now.day

    async def get_station_data(self, station_id: str):
        """
        Obtiene los datos meteorológicos de una estación desde la API de Meteocat.

        Args:
            station_id (str): Código de la estación.

        Returns:
            dict: Datos meteorológicos de la estación.
        """
        any, mes, dia = self.get_current_date()  # Calcula la fecha actual
        url = f"{BASE_URL}{STATION_DATA_URL}".format(
            codiEstacio=station_id, any=any, mes=f"{mes:02d}", dia=f"{dia:02d}"
        )
    
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
                        raise UnknownAPIError(
                            f"Unexpected error {response.status}: {await response.text()}"
                        )

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

    async def get_station_data_with_variables(self, station_id: str, force_update=False):
        """
        Obtiene los datos meteorológicos de una estación, organizados por variables.

        Args:
            station_id (str): Código de la estación.
            force_update (bool): Si True, fuerza la actualización de las variables desde la API.

        Returns:
            dict: Datos organizados por variables.
        """
        # Obtener datos de la estación
        station_data = await self.get_station_data(station_id)

        # Obtener las variables desde el caché o API
        variables = await self.variables.get_variables(force_update=force_update)

        # Crear una estructura para organizar los datos por variables
        datos_por_variable = {}

        for lectura in station_data.get("lectures", []):
            codi_variable = lectura.get("codi_variable")
            variable_info = next((v for v in variables if v["codi"] == codi_variable), None)
            if variable_info:
                nombre_variable = variable_info["nom"]
                if nombre_variable not in datos_por_variable:
                    datos_por_variable[nombre_variable] = []
                datos_por_variable[nombre_variable].append(
                    {
                        "data": lectura["data"],
                        "valor": lectura["valor"],
                        "estat": lectura.get("estat", ""),
                        "base_horaria": lectura.get("base_horaria", ""),
                    }
                )

        return datos_por_variable
