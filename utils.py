
import json
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from google.colab import userdata

def authenticate_from_colab_secret(secret_name='credenciales'):
    """
    Autentica con Google Drive usando un secreto guardado en Google Colab.
    El secreto debe ser el JSON de una cuenta de servicio (como string).

    Args:
        secret_name (str): Nombre del secreto en Colab (ej. 'credenciales').

    Returns:
        GoogleDrive: Objeto autenticado para operaciones con Drive.
    """
    secret_json = userdata.get(secret_name)
    if not secret_json:
        raise ValueError(f"No se encontró el secreto llamado '{secret_name}'.")

    # Convertimos string JSON a diccionario
    service_account_info = json.loads(secret_json)

    # Creamos el archivo temporal para pasárselo a ServiceAuth
    gauth = GoogleAuth()
    gauth.ServiceAuth(service_account_info)

    drive = GoogleDrive(gauth)
    return drive
