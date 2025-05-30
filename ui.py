import ipywidgets as widgets
from IPython.display import display, clear_output
from lis_xml2excel.converter import convert_files_in_drive_folder
from lis_xml2excel.utils import authenticate_from_colab_secret

def render_interface_from_colab_secret(folder_id):
    """
    Interfaz para convertir archivos .lis y .xml desde Drive con autenticación
    usando un secreto almacenado en Colab.
    """
    convert_button = widgets.Button(
        description='Convertir Archivos',
        button_style='success'
    )

    output = widgets.Output()

    def convertir_handler(change):
        with output:
            clear_output()
            print("🔐 Autenticando con secreto 'credenciales'...")

            drive = authenticate_from_colab_secret(secret_name='credenciales')
            mensaje = convert_files_in_drive_folder(drive, folder_id)
            print(mensaje)

    convert_button.on_click(convertir_handler)


    display(widgets.HTML("Haz clic para procesar los archivos de la carpeta compartida."))
    display(convert_button)
    display(output)
