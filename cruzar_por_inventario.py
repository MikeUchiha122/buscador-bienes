import pandas as pd
import os

BASE_FILE = 'BASE_BIENES_UNIDAD.xlsx'
NUEVO_FILE = 'archivo_cruzar/ARCHIVO_NUEVO.xlsx'
OUTPUT_FILE = 'INFORME_CRUZE_INVENTARIO.xlsx'

def cruzar_por_inventario():
    base_path = BASE_FILE
    nuevo_path = NUEVO_FILE
    
    if not os.path.exists(base_path):
        print(f"Error: No se encuentra {base_path}")
        return
    
    if not os.path.exists(nuevo_path):
        print(f"Error: No se encuentra {nuevo_path}")
        print("Coloca el archivo actualizado en archivo_cruzar/ARCHIVO_NUEVO.xlsx")
        return
    
    print(f"Leyendo archivos...")
    df_base = pd.read_excel(base_path)
    df_nuevo = pd.read_excel(nuevo_path)
    
    df_base['N° INVENTARIO'] = df_base['N° INVENTARIO'].astype(str).str.strip()
    df_nuevo['N° INVENTARIO'] = df_nuevo['N° INVENTARIO'].astype(str).str.strip()
    
    inv_base = set(df_base['N° INVENTARIO'].unique())
    inv_nuevo = set(df_nuevo['N° INVENTARIO'].unique())
    
    existentes = df_nuevo[df_nuevo['N° INVENTARIO'].isin(inv_base)]
    faltantes = df_nuevo[~df_nuevo['N° INVENTARIO'].isin(inv_base)]
    
    print(f"\n--- RESULTADOS ---")
    print(f"Registros BASE: {len(df_base)}")
    print(f"Registros NUEVO: {len(df_nuevo)}")
    print(f"Existentes (match): {len(existentes)}")
    print(f"Faltantes (no match): {len(faltantes)}")
    
    with pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl') as writer:
        existentes.to_excel(writer, sheet_name='Existentes', index=False)
        faltantes.to_excel(writer, sheet_name='Faltantes', index=False)
    
    print(f"\nInforme generado: {OUTPUT_FILE}")

if __name__ == '__main__':
    cruzar_por_inventario()