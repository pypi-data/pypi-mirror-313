import aiohttp
from .const import BASE_URL, MUNICIPIS_LIST_URL
from .exceptions import BadRequestError, ForbiddenError, TooManyRequestsError, InternalServerError, UnknownAPIError

class MeteocatTown:
    """Clase para interactuar con la lista de municipios de la API de Meteocat."""

    def __init__(self, api_key: str):
        """
        Inicializa la clase MeteocatTown.

        Args:
            api_key (str): Clave de API para autenticar las solicitudes.
        """
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "X-Api-Key": self.api_key,
        }

    async def get_municipis(self):
        """
        Obtiene la lista de municipios desde la API de Meteocat.

        Returns:
            dict: Datos de los municipios.
        """
        url = f"{BASE_URL}{MUNICIPIS_LIST_URL}"
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
