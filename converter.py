import pandas as pd
import io
from googleapiclient.http import MediaIoBaseUpload

def xml_to_excel_bytes(xml_text):
    """
    Convierte texto XML a bytes de archivo Excel (.xlsx).
    """
    meta = pd.read_xml(io.StringIO(xml_text))
    df = pd.read_xml(io.StringIO(xml_text), xpath='.//Registro')
    meta = meta.iloc[[0]]
    meta = meta.loc[meta.index.repeat(len(df))].reset_index(drop=True)
    df = pd.concat([meta, df.reset_index(drop=True)], axis=1)

    output = io.BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return output

def convert_files_in_drive_folder(service, folder_id):
    """
    Descarga archivos .lis/.xml desde Drive, convierte a .xlsx,
    sube el resultado y elimina el archivo original.

    Args:
        service: Google Drive API service.
        folder_id: ID de la carpeta compartida.

    Returns:
        str: Resultado de la operación.
    """
    response = service.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        fields="files(id, name, mimeType)"
    ).execute()

    archivos = response.get('files', [])
    if not archivos:
        return "⚠️ No se encontraron archivos."

    total = 0
    for archivo in archivos:
        file_id = archivo['id']
        name = archivo['name']

        if not (name.endswith('.xml') or name.endswith('.lis')):
            continue

        file_content = service.files().get_media(fileId=file_id).execute()
        try:
            if name.endswith('.xml'):
                excel_bytes = xml_to_excel_bytes(file_content.decode('utf-8'))
            else:
                df = pd.read_csv(io.StringIO(file_content.decode('latin1')), sep='|', engine='python')
                try:
                    for i in df.columns:
                        if 'fecha' in i:
                            df[i]=pd.to_datetime(df[i],format='%b %d %Y %I:%M:%S:%f%p')
                except:pass
                excel_bytes = io.BytesIO()
                df.to_excel(excel_bytes, index=False)
                excel_bytes.seek(0)

            # Subir el Excel
            excel_name = name.rsplit('.', 1)[0] + '.xlsx'
            media = MediaIoBaseUpload(excel_bytes, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            service.files().create(
                body={'name': excel_name, 'parents': [folder_id]},
                media_body=media,
                fields='id'
            ).execute()

            # Borrar original
            service.files().delete(fileId=file_id).execute()
            total += 1

        except Exception as e:
            print(f"❌ Error con {name}: {e}")

    return f"✅ Se convirtieron {total} archivo(s) y se subieron como .xlsx"
