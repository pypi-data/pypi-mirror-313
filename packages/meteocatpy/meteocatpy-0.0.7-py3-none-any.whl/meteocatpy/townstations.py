import aiohttp
from .stations import MeteocatStations  # Importamos la clase MeteocatStations
from .const import BASE_URL, STATIONS_MUNICIPI_URL
from .exceptions import (
    BadRequestError,
    ForbiddenError,
    TooManyRequestsError,
    InternalServerError,
    UnknownAPIError,
)

class MeteocatTownStations:
    """
    Clase para interactuar con la API de Meteocat y obtener
    las estaciones representativas de un municipio para una variable específica.
    """

    def __init__(self, api_key: str):
        """
        Inicializa la clase MeteocatTownStations.

        Args:
            api_key (str): Clave de API para autenticar las solicitudes.
        """
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "X-Api-Key": self.api_key,
        }
        self.stations_service = MeteocatStations(api_key)  # Instancia de MeteocatStations

    async def get_town_stations(self, town_id: str, variable_id: str):
        """
        Obtiene la lista de estaciones representativas para un municipio y una variable específica,
        enriqueciendo los datos con el nombre de las estaciones.

        Args:
            codi_municipi (str): Código del municipio.
            codi_variable (str): Código de la variable.

        Returns:
            list: Datos de las estaciones representativas con nombres añadidos.
        """
        # Obtener la lista completa de estaciones
        all_stations = await self.stations_service.get_stations()

        # Crear un diccionario para acceder rápidamente a los nombres por código
        station_names = {station["codi"]: station["nom"] for station in all_stations}

        # URL para obtener las estaciones del municipio y la variable
        url = f"{BASE_URL}{STATIONS_MUNICIPI_URL}".format(
            codi_municipi=town_id, codi_variable=variable_id
        )

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()

                        # Enriquecer el JSON con los nombres de las estaciones
                        for town in data:
                            for variable in town.get("variables", []):
                                for station in variable.get("estacions", []):
                                    codi = station["codi"]
                                    station["nom"] = station_names.get(codi, "Nombre desconocido")

                        return data

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

