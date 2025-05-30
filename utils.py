import json
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from google.colab import userdata

def authenticate_from_colab_secret(secret_name='credenciales', json_path='sa_key.json'):
    """
    Autentica con PyDrive2 usando una clave de servicio guardada como secreto en Colab.

    Args:
        secret_name (str): Nombre del secreto donde está el JSON.
        json_path (str): Ruta temporal donde se guardará el archivo JSON.

    Returns:
        GoogleDrive: Objeto autenticado para interactuar con Google Drive.
    """
    secret_json = userdata.get(secret_name)
    if not secret_json:
        raise ValueError(f"⚠️ No se encontró el secreto llamado '{secret_name}'.")

    # Guardar la clave como archivo temporal para usar ServiceAuth()
    with open(json_path, 'w') as f:
        json.dump(json.loads(secret_json), f)

    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(json_path)  # Cargar archivo como configuración
    gauth.ServiceAuth()  # Autenticación con cuenta de servicio

    return GoogleDrive(gauth)
