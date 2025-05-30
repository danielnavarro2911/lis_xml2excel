import ipywidgets as widgets
from IPython.display import display, clear_output
from lis_xml2excel.utils import build_drive_service_from_colab_secret
from lis_xml2excel.converter import convert_files_in_drive_folder

def render_interface(folder_id):
    convert_button = widgets.Button(description='Convertir Archivos', button_style='success')
    output = widgets.Output()

    def convertir_handler(change):
        with output:
            clear_output()
            print("🔐 Autenticando y conectando con Google Drive...")
            service = build_drive_service_from_colab_secret()
            mensaje = convert_files_in_drive_folder(service, folder_id)
            print(mensaje)

    convert_button.on_click(convertir_handler)


    display(widgets.HTML("Haz clic para convertir los archivos."))
    display(convert_button)
    display(output)
