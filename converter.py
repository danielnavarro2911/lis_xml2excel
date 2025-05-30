import pandas as pd
import os
import zipfile

def save_uploaded_files(uploaded_files):
    """
    Guarda todos los archivos subidos.

    Args:
        uploaded_files (dict): Diccionario con los archivos cargados.

    Returns:
        List[str]: Lista de nombres de archivos guardados.
    """
    saved_files = []
    for file_info in uploaded_files.values():
        filename = file_info['metadata']['name']
        content = file_info['content']
        with open(filename, 'wb') as f:
            f.write(content)
        saved_files.append(filename)
    return saved_files

def xml_to_excel(file):
    """
    Convierte un XML según el formato especial del usuario.

    Args:
        file (str): Ruta del archivo XML.

    Returns:
        pd.DataFrame: DataFrame combinado con metadata.
    """
    with open(file, 'r', encoding='utf-8') as f:
        meta = pd.read_xml(f)
    with open(file, 'r', encoding='utf-8') as f:
        df = pd.read_xml(f, xpath='.//Registro')

    meta = meta.iloc[[0]]
    meta = meta.loc[meta.index.repeat(len(df))].reset_index(drop=True)
    df = pd.concat([meta, df.reset_index(drop=True)], axis=1)
    return df

def convert_files_to_excel(file_list):
    """
    Convierte múltiples archivos a Excel.

    Args:
        file_list (List[str]): Archivos a convertir.

    Returns:
        List[str]: Archivos .xlsx generados.
        str or None: Mensaje de error si ocurre alguno.
    """
    excel_files = []
    try:
        for file in file_list:
            if file.endswith('.lis'):
                df = pd.read_csv(file, sep='|', engine='python', encoding='latin1')
                for i in df.columns:
                    if 'fecha' in i:
                        try:
                            df[i]=pd.to_datetime(df[i],format='%b %d %Y %I:%M:%S:%f%p')
                        except:
                            pass
            elif file.endswith('.xml'):
                df = xml_to_excel(file)
            else:
                return [], f"Tipo de archivo no soportado: {file}"

            output_name = file.rsplit('.', 1)[0] + '.xlsx'
            df.to_excel(output_name, index=False)
            excel_files.append(output_name)

        return excel_files, None

    except Exception as e:
        return [], str(e)

def zip_files(file_list, zip_name='archivos_convertidos.zip'):
    """
    Crea un ZIP con los archivos dados.

    Args:
        file_list (List[str]): Archivos a comprimir.
        zip_name (str): Nombre del archivo ZIP.

    Returns:
        str: Nombre del archivo ZIP creado.
    """
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for file in file_list:
            zipf.write(file)
    return zip_name
