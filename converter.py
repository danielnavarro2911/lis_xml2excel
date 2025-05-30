import pandas as pd
import io

def xml_to_excel(file_content):
    """
    Convierte el contenido de un archivo XML a DataFrame combinando metadatos y registros.

    Args:
        file_content (str): Contenido del XML en texto.

    Returns:
        pd.DataFrame: DataFrame combinado.
    """
    decoded = file_content.decode('utf-8')
    meta = pd.read_xml(io.StringIO(decoded))
    df = pd.read_xml(io.StringIO(decoded), xpath='.//Registro')

    meta = meta.iloc[[0]]
    meta = meta.loc[meta.index.repeat(len(df))].reset_index(drop=True)
    df = pd.concat([meta, df.reset_index(drop=True)], axis=1)
    return df

def convert_files_in_drive_folder(drive, folder_id):
    """
    Convierte todos los archivos .lis y .xml de una carpeta de Google Drive a .xlsx.
    Los archivos convertidos se suben en la misma carpeta.
    Los originales se eliminan.

    Args:
        drive (GoogleDrive): Objeto autenticado con PyDrive2.
        folder_id (str): ID de la carpeta en Google Drive.

    Returns:
        str: Mensaje con la cantidad de archivos procesados o error.
    """
    file_list = drive.ListFile({
        'q': f"'{folder_id}' in parents and trashed=false"
    }).GetList()

    if not file_list:
        return "⚠️ No se encontraron archivos .lis o .xml en la carpeta."

    total = 0

    for file in file_list:
        filename = file['title']
        if not (filename.endswith('.xml') or filename.endswith('.lis')):
            continue  # saltar archivos no soportados

        try:
            content = file.GetContentString(encoding='utf-8')

            if filename.endswith('.lis'):
                df = pd.read_csv(io.StringIO(content), sep='|', engine='python', encoding='latin1')
                for i in df.columns:
                    try:
                        if 'fecha' in i:
                            df[i]=pd.to_datetime(df[i],format='%b %d %Y %I:%M:%S:%f%p')
                    except:pass
            else:  # XML
                df = xml_to_excel(content)

            # Convertir DataFrame a Excel en memoria
            output = io.BytesIO()
            df.to_excel(output, index=False, engine='openpyxl')
            output.seek(0)

            # Subir a Drive como .xlsx
            new_file = drive.CreateFile({
                'title': filename.rsplit('.', 1)[0] + '.xlsx',
                'parents': [{'id': folder_id}]
            })
            new_file.SetContentString(output.read().decode('ISO-8859-1'), encoding='ISO-8859-1')
            new_file.Upload()

            # Eliminar original
            file.Delete()

            total += 1

        except Exception as e:
            print(f"❌ Error procesando {filename}: {e}")

    return f"✅ Se convirtieron {total} archivo(s) .lis / .xml a .xlsx y se subieron al mismo folder."
