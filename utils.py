from google.colab import userdata
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json

def build_drive_service_from_colab_secret(secret_name='credenciales', scopes=None):
    """
    Construye un servicio de Google Drive desde un secreto JSON guardado en Colab.

    Args:
        secret_name (str): Nombre del secreto que contiene el JSON.
        scopes (list): Scopes requeridos para el acceso a Drive.

    Returns:
        googleapiclient.discovery.Resource: Objeto drive autenticado.
    """
    if scopes is None:
        scopes = ['https://www.googleapis.com/auth/drive']

    secret_json = userdata.get(secret_name)
    if not secret_json:
        raise ValueError(f"⚠️ Secreto '{secret_name}' no encontrado.")

    info = json.loads(secret_json)
    credentials = service_account.Credentials.from_service_account_info(info, scopes=scopes)

    service = build('drive', 'v3', credentials=credentials)
    return service
