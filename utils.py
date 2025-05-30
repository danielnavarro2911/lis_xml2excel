import json
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from google.colab import userdata

def authenticate_from_colab_secret(secret_name='credenciales', temp_file='sa_key.json'):
    """
    Carga la clave JSON desde los secretos de Colab, la guarda como archivo
    temporal y autentica con Google Drive usando PyDrive2.

    Args:
        secret_name (str): Nombre del secreto en Colab.
        temp_file (str): Nombre del archivo temporal que se usará.

    Returns:
        GoogleDrive: Objeto autenticado.
    """
    secret_json = userdata.get(secret_name)
    if not secret_json:
        raise ValueError(f"No se encontró el secreto llamado '{secret_name}'.")

    with open(temp_file, 'w') as f:
        json.dump(json.loads(secret_json), f)

    gauth = GoogleAuth()
    gauth.LoadServiceConfigFile(temp_file)
    gauth.ServiceAuth()
    return GoogleDrive(gauth)
