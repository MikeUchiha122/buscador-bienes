import pandas as pd
import os
from datetime import datetime

BASE_FILE = 'BASE_BIENES_UNIDAD.xlsx'
NUEVO_FILE = 'archivo_cruzar/ARCHIVO_NUEVO.xlsx'
OUTPUT_FILE = 'INFORME_CRUZE.xlsx'

def cruzar_por_cabm():
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
    print(f"  Base: {base_path}")
    print(f"  Nuevo: {nuevo_path}")
    
    df_base = pd.read_excel(base_path)
    df_nuevo = pd.read_excel(nuevo_path)
    
    df_base['CABM'] = df_base['CABM'].astype(str).str.strip()
    df_nuevo['CABM'] = df_nuevo['CABM'].astype(str).str.strip()
    
    cabm_base = set(df_base['CABM'].unique())
    cabm_nuevo = set(df_nuevo['CABM'].unique())
    
    existentes = df_nuevo[df_nuevo['CABM'].isin(cabm_base)]
    faltantes = df_nuevo[~df_nuevo['CABM'].isin(cabm_base)]
    
    print(f"\n--- RESULTADOS ---")
    print(f"Total registros BASE: {len(df_base)}")
    print(f"Total registros NUEVO: {len(df_nuevo)}")
    print(f"CABMs únicos BASE: {len(cabm_base)}")
    print(f"CABMs únicos NUEVO: {len(cabm_nuevo)}")
    print(f"Existentes (match): {len(existentes)}")
    print(f"Faltantes (no match): {len(faltantes)}")
    
    with pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl') as writer:
        existentes.to_excel(writer, sheet_name='Existentes', index=False)
        faltantes.to_excel(writer, sheet_name='Faltantes', index=False)
    
    print(f"\nInforme generado: {OUTPUT_FILE}")
    print(f"Hoja 1: Existentes ({len(existentes)} registros)")
    print(f"Hoja 2: Faltantes ({len(faltantes)} registros)")

if __name__ == '__main__':
    cruzar_por_cabm()