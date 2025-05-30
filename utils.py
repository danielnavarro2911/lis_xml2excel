import json
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from google.colab import userdata

def authenticate_from_colab_secret(secret_name='credenciales', json_path='sa_key.json'):
    """
    Autentica con Google Drive usando un secreto de Colab que contiene el JSON
    de una cuenta de servicio. El archivo se guarda como sa_key.json.

    Args:
        secret_name (str): Nombre del secreto en Colab.
        json_path (str): Archivo temporal donde se guardará el JSON.

    Returns:
        GoogleDrive: Objeto autenticado con PyDrive2.
    """
    # Obtener el JSON desde el secreto
    secret_json = userdata.get(secret_name)
    if not secret_json:
        raise ValueError(f"⚠️ No se encontró el secreto llamado '{secret_name}'.")

    # Guardar como archivo para usarlo con ServiceAuth
    with open(json_path, 'w') as f:
        json.dump(json.loads(secret_json), f)

    # Autenticación con cuenta de servicio
    gauth = GoogleAuth()
    gauth.settings['client_config_file'] = json_path
    gauth.ServiceAuth()

    drive = GoogleDrive(gauth)
    return drive
