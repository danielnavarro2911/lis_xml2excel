import pandas as pd
import os

def xml_to_excel(file):
    """
    Convierte un archivo XML que tiene metadatos y registros.
    """
    with open(file, 'r', encoding='utf-8') as f:
        meta = pd.read_xml(f)
    with open(file, 'r', encoding='utf-8') as f:
        df = pd.read_xml(f, xpath='.//Registro')

    meta = meta.iloc[[0]]
    meta = meta.loc[meta.index.repeat(len(df))].reset_index(drop=True)
    df = pd.concat([meta, df.reset_index(drop=True)], axis=1)
    return df

def convert_drive_folder(folder_path):
    """
    Convierte todos los archivos .lis y .xml en una carpeta a .xlsx,
    los guarda en la misma carpeta y elimina los originales.
    """
    files = [f for f in os.listdir(folder_path) if f.endswith('.lis') or f.endswith('.xml')]
    if not files:
        return "No se encontraron archivos .lis ni .xml."

    try:
        for file in files:
            full_path = os.path.join(folder_path, file)

            if file.endswith('.lis'):
                df = pd.read_csv(full_path, sep='|', engine='python', encoding='latin1')
                for i in df.columns:
                    try:
                        if 'fecha' in i:
                            df[i]=pd.to_datetime(df[i],format='%b %d %Y %I:%M:%S:%f%p')
                    except:pass
            elif file.endswith('.xml'):
                df = xml_to_excel(full_path)
            else:
                continue  # se ignora

            output_name = os.path.join(folder_path, file.rsplit('.', 1)[0] + '.xlsx')
            df.to_excel(output_name, index=False)

            os.remove(full_path)  # borra el original

        return f"✅ {len(files)} archivo(s) convertidos y guardados en la carpeta."

    except Exception as e:
        return f"❌ Error durante la conversión: {e}"
