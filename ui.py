from google.colab import files
import ipywidgets as widgets
from IPython.display import display, clear_output
from converter import save_uploaded_files, convert_files_to_excel, zip_files

def render_interface():
    upload_button = widgets.FileUpload(
        accept='.lis,.xml',
        multiple=True  # ahora acepta múltiples archivos
    )

    convert_button = widgets.Button(
        description='Convertir a Excel',
        button_style='success'
    )

    output = widgets.Output()

    def convertir_handler(change):
        with output:
            clear_output()
            if not upload_button.value:
                print("⚠️ Por favor, sube al menos un archivo .lis o .xml.")
                return

            # Verifica que todos los archivos sean del mismo tipo
            files_list = list(upload_button.value.values())
            exts = set([f['metadata']['name'].split('.')[-1] for f in files_list])
            if len(exts) > 1:
                print("❌ Todos los archivos deben ser del mismo tipo (.lis o .xml).")
                return

            # Guardar archivos subidos
            saved_files = save_uploaded_files(upload_button.value)

            # Convertirlos a Excel
            excel_files, error = convert_files_to_excel(saved_files)
            if error:
                print(f"❌ Error al convertir archivos: {error}")
                return

            # Descargar individual o en zip
            if len(excel_files) == 1:
                files.download(excel_files[0])
                print(f"✅ Archivo convertido: {excel_files[0]}")
            else:
                zip_path = zip_files(excel_files)
                files.download(zip_path)
                print(f"✅ Archivos convertidos y comprimidos en: {zip_path}")

    convert_button.on_click(convertir_handler)

    # Mostrar interfaz
    display(widgets.HTML("<h2>Convertidor de archivos .lis / .xml a .xlsx</h2>"))
    display(widgets.HTML("1. Sube uno o más archivos del mismo tipo"))
    display(upload_button)
    display(widgets.HTML("2. Haz clic para convertir"))
    display(convert_button)
    display(output)
