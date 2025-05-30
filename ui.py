import ipywidgets as widgets
from IPython.display import display, clear_output
from lis_xml2excel.converter import convert_drive_folder

def render_interface(drive_folder_path):
    """
    Crea una interfaz con botón para convertir y guardar archivos .xlsx en Drive.
    """
    convert_button = widgets.Button(
        description='Convertir Archivos',
        button_style='success'
    )

    output = widgets.Output()

    def convertir_handler(change):
        with output:
            clear_output()
            print("📂 Procesando carpeta:", drive_folder_path)

            mensaje = convert_drive_folder(drive_folder_path)
            print(mensaje)

    convert_button.on_click(convertir_handler)

    display(convert_button)
    display(output)
