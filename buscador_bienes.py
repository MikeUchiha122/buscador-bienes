import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
import sys
import logging

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_FILE = os.path.join(BASE_DIR, "bienes.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

EXCEL_FILES = [
    "BASE_BIENES_UNIDAD.xlsx",
]

def encontrar_excel():
    for f in EXCEL_FILES:
        path = os.path.join(BASE_DIR, f)
        if os.path.exists(path):
            return path
    return None

EXCEL_PATH = encontrar_excel()

LOG_COLORS = {
    "bg_main": "#1e1e2e",
    "bg_dark": "#313244",
    "bg_gray": "#45475a",
    "text_light": "#cdd6f4",
    "text_muted": "#a6adc8",
    "text_dim": "#6c7086",
    "accent_blue": "#89b4fa",
    "accent_yellow": "#f9e2af",
    "accent_green": "#94e2d5",
    "success": "#a6e3a1",
    "danger": "#f38ba8",
    "warning": "#fab387",
}

ESTADO_COLORES = {
    "BUENO": LOG_COLORS["success"],
    "MALO": LOG_COLORS["danger"],
    "REGULAR": LOG_COLORS["warning"],
}

FILTRO_STATUS = {
    "VIGENTES": 1,
    "BAJAS": 0,
    "TODOS": None,
}

def log_accion(accion, detalles=""):
    logger.info(f"[{accion}] {detalles}")

class BuscadorBienes:
    def __init__(self, root):
        self.root = root
        self.root.title("🔍 Buscador de Bienes - SICOBIM | Ing. Miguel Ángel Ramírez Galicia")
        self.root.geometry("1200x700")
        self.root.minsize(900, 500)
        self.root.configure(bg=LOG_COLORS["bg_main"])
        
        self.df = self.cargar_datos()
        self._cache_columnas = {}
        
        self.configurar_estilos()
        self.crear_interfaz()
        
        self.root.bind("<Configure>", self.on_resize)
    
    def cargar_datos(self):
        try:
            log_accion("INICIO", f"Cargando Excel: {EXCEL_PATH}")
            df = pd.read_excel(EXCEL_PATH, header=0, engine='openpyxl')
            df.columns = df.columns.str.strip()
            
            df = df.loc[:, ~df.columns.isna()]
            
            for col in df.columns:
                if col and isinstance(col, str) and 'INVENTARIO' in col.upper():
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype('int64')
                    break
            
            for col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = df[col].fillna('').astype(str).str.strip()
            
            if 'STATUS' not in df.columns:
                df['STATUS'] = 1
                df.to_excel(EXCEL_PATH, index=False, engine='openpyxl')
                log_accion("NUEVA_COLUMNA", "Se agregó columna STATUS al Excel")
            
            log_accion("CARGA_EXITO", f"Total bienes cargados: {len(df)}, Vigentes: {len(df[df['STATUS']==1])}, Bajas: {len(df[df['STATUS']==0])}")
            return df
        except Exception as e:
            log_accion("ERROR_CARGA", str(e))
            messagebox.showerror("Error", f"No se pudo cargar el Excel:\n{e}")
            return pd.DataFrame()
    
    def encontrar_columna(self, nombre_buscar):
        if nombre_buscar in self._cache_columnas:
            return self._cache_columnas[nombre_buscar]
        
        for col in self.df.columns:
            if nombre_buscar.upper() in col.upper():
                self._cache_columnas[nombre_buscar] = col
                return col
        
        self._cache_columnas[nombre_buscar] = nombre_buscar
        return nombre_buscar
    
    def _obtener_df_filtrado(self):
        filtro = self.filtro_status.get()
        status_value = FILTRO_STATUS.get(filtro)
        if status_value is None:
            return self.df.copy()
        return self.df[self.df['STATUS'] == status_value].copy()
    
    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("Treeview", 
                        background=LOG_COLORS["bg_dark"],
                        foreground=LOG_COLORS["text_light"],
                        fieldbackground=LOG_COLORS["bg_dark"],
                        rowheight=28)
        
        style.configure("Treeview.Heading",
                        background=LOG_COLORS["bg_gray"],
                        foreground=LOG_COLORS["text_light"],
                        font=("Segoe UI", 10, "bold"))
        
        style.map("Treeview", 
                  background=[("selected", LOG_COLORS["accent_blue"])])
    
    def crear_interfaz(self):
        header_frame = tk.Frame(self.root, bg=LOG_COLORS["bg_main"], height=80)
        header_frame.pack(fill="x", padx=20, pady=15)
        
        title = tk.Label(header_frame, 
                        text="🔐 Búsqueda de Bienes - SICOBIM",
                        font=("Segoe UI", 18, "bold"),
                        fg=LOG_COLORS["accent_blue"], bg=LOG_COLORS["bg_main"])
        title.pack(anchor="w")
        
        subtitle = tk.Label(header_frame,
                           text="Sistema de Control de Bienes Muebles - México",
                           font=("Segoe UI", 10),
                           fg=LOG_COLORS["text_muted"], bg=LOG_COLORS["bg_main"])
        subtitle.pack(anchor="w")
        
        btn_cruzar_frame = tk.Frame(header_frame, bg=LOG_COLORS["bg_main"])
        btn_cruzar_frame.pack(side="right", padx=10)
        
        btn_cruzar_inv = tk.Button(btn_cruzar_frame,
                              text="📊 x Inventario",
                              command=self.cruzar_inventario,
                              bg=LOG_COLORS["accent_yellow"],
                              fg=LOG_COLORS["bg_main"],
                              font=("Segoe UI", 9, "bold"),
                              relief="flat",
                              padx=15, pady=8)
        btn_cruzar_inv.pack(side="left", padx=5)
        
        btn_cruzar_inv_cabm = tk.Button(btn_cruzar_frame,
                              text="📊 x Inv+CABM",
                              command=self.cruzar_inv_cabm,
                              bg=LOG_COLORS["accent_green"],
                              fg=LOG_COLORS["bg_main"],
                              font=("Segoe UI", 9, "bold"),
                              relief="flat",
                              padx=15, pady=8)
        btn_cruzar_inv_cabm.pack(side="left", padx=5)
        
        search_frame = tk.Frame(self.root, bg=LOG_COLORS["bg_main"])
        search_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        tk.Label(search_frame, text="Buscar:", 
                fg=LOG_COLORS["text_light"], bg=LOG_COLORS["bg_main"],
                font=("Segoe UI", 11)).pack(side="left")
        
        self.buscar_var = tk.StringVar()
        self.entry_busqueda = tk.Entry(search_frame,
                                        textvariable=self.buscar_var,
                                        font=("Segoe UI", 11),
                                        bg=LOG_COLORS["bg_dark"],
                                        fg=LOG_COLORS["text_light"],
                                        insertbackground=LOG_COLORS["text_light"],
                                        width=40)
        self.entry_busqueda.pack(side="left", padx=10, fill="x", expand=True)
        
        btn_buscar = tk.Button(search_frame,
                              text="🔍 Buscar",
                              command=self.buscar,
                              bg=LOG_COLORS["accent_blue"],
                              fg=LOG_COLORS["bg_main"],
                              font=("Segoe UI", 10, "bold"),
                              relief="flat",
                              padx=15, pady=5)
        btn_buscar.pack(side="left")
        
        btn_limpiar = tk.Button(search_frame,
                               text="Limpiar",
                               command=self.limpiar_busqueda,
                               bg=LOG_COLORS["bg_gray"],
                               fg=LOG_COLORS["text_light"],
                               font=("Segoe UI", 10),
                               relief="flat",
                               padx=15, pady=5)
        btn_limpiar.pack(side="left", padx=(10, 0))
        
        combo_frame = tk.Frame(search_frame, bg=LOG_COLORS["bg_main"])
        combo_frame.pack(side="right")
        
        tk.Label(combo_frame, text=" Filtro:",
                fg=LOG_COLORS["text_light"], bg=LOG_COLORS["bg_main"]).pack(side="left")
        
        self.filtro_status = ttk.Combobox(combo_frame,
                                            values=["VIGENTES", "BAJAS", "TODOS"],
                                            state="readonly",
                                            width=12)
        self.filtro_status.set("VIGENTES")
        self.filtro_status.pack(side="left", padx=(5, 0))
        self.filtro_status.bind("<<ComboboxSelected>>", lambda e: self.buscar())
        
        tk.Label(combo_frame, text=" Buscar en:",
                fg=LOG_COLORS["text_light"], bg=LOG_COLORS["bg_main"]).pack(side="left")
        
        self.campo_busqueda = ttk.Combobox(combo_frame,
                                            values=["Todos", "DESCRIPCIÓN DETALLE", 
                                                   "UBICACIÓN", "ESTADO DEL BIEN",
                                                   "N° INVENTARIO", "CABM", 
                                                   "NOMBRE COMPLETO", "MARCA", "MODELO"],
                                            state="readonly",
                                            width=20)
        self.campo_busqueda.set("Todos")
        self.campo_busqueda.pack(side="left", padx=(5, 0))
        
        self.entry_busqueda.bind("<Return>", lambda e: self.buscar())
        
        columns = ("N° INVENTARIO", "DESCRIPCIÓN DETALLE", "UBICACIÓN", "ESTADO DEL BIEN", "IMPORTE")
        tree_frame = tk.Frame(self.root, bg=LOG_COLORS["bg_main"])
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        self.tree.column("DESCRIPCIÓN DETALLE", width=250)
        self.tree.column("IMPORTE", width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.tree.bind("<Double-1>", self.mostrar_detalle)
        
        self.llenar_tabla(self.df)
        
        total_frame = tk.Frame(self.root, bg=LOG_COLORS["bg_main"])
        total_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.lbl_total = tk.Label(total_frame,
                                  text=f"Total de registros: {len(self.df)}",
                                  fg=LOG_COLORS["text_muted"], bg=LOG_COLORS["bg_main"],
                                  font=("Segoe UI", 10))
        self.lbl_total.pack(side="left")
        
        info = tk.Label(total_frame,
                       text="💡 Doble clic en un registro para ver todos los detalles",
                       fg=LOG_COLORS["text_dim"], bg=LOG_COLORS["bg_main"],
                       font=("Segoe UI", 9))
        info.pack(side="right")
    
    def on_resize(self, event):
        width = self.root.winfo_width()
        
        if hasattr(self, 'tree'):
            tree_width = max(800, width - 60)
            self.tree.column("N° INVENTARIO", width=int(tree_width * 0.12))
            self.tree.column("DESCRIPCIÓN DETALLE", width=int(tree_width * 0.35))
            self.tree.column("UBICACIÓN", width=int(tree_width * 0.25))
            self.tree.column("ESTADO DEL BIEN", width=int(tree_width * 0.13))
            self.tree.column("IMPORTE", width=int(tree_width * 0.15))
    
    def buscar(self):
        try:
            criterio = self.buscar_var.get().strip().upper().replace(" ", "")
            campo = self.campo_busqueda.get()
            
            df_filtrado = self._obtener_df_filtrado()
            
            if not criterio:
                self.llenar_tabla(df_filtrado)
                self.lbl_total.config(text=f"Total de registros: {len(df_filtrado)}")
                return
            
            log_accion("BUSQUEDA", f"Buscar: '{criterio}' en campo: {campo}, filtro: {self.filtro_status.get()}")
            
            if campo == "Todos":
                mask = df_filtrado.apply(lambda row: criterio in row.astype(str).values, axis=1)
            else:
                campo_en_df = self.encontrar_columna(campo)
                mask = df_filtrado[campo_en_df].astype(str).str.contains(criterio, na=False, regex=False)
            
            resultados = df_filtrado[mask]
            
            if resultados.empty:
                log_accion("BUSQUEDA_SIN_RESULTADOS", f"Sin resultados para: '{criterio}'")
                messagebox.showinfo("Sin resultados", f"No se encontraron bienes con: '{criterio}'")
                self.llenar_tabla(df_filtrado)
                self.lbl_total.config(text=f"Total de registros: {len(df_filtrado)}")
            else:
                log_accion("BUSQUEDA_EXITOSA", f"Resultados: {len(resultados)} para: '{criterio}'")
                self.llenar_tabla(resultados)
                self.lbl_total.config(text=f"Resultados: {len(resultados)} de {len(df_filtrado)}")
        except Exception as e:
            log_accion("ERROR_BUSQUEDA", str(e))
            import traceback
            print(f"Error en búsqueda: {e}")
            traceback.print_exc()
            messagebox.showerror("Error", f"Error en búsqueda:\n{e}")
    
    def limpiar_busqueda(self):
        self.buscar_var.set("")
        df_filtrado = self._obtener_df_filtrado()
        self.llenar_tabla(df_filtrado)
        self.lbl_total.config(text=f"Total de registros: {len(df_filtrado)}")
    
    def llenar_tabla(self, df):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        col_inv = self.encontrar_columna("N° INVENTARIO")
        col_desc = self.encontrar_columna("DESCRIPCIÓN DETALLE")
        col_ubic = self.encontrar_columna("UBICACIÓN")
        col_estado = self.encontrar_columna("ESTADO DEL BIEN")
        col_importe = self.encontrar_columna("IMPORTE")
        
        valores = df[[col_inv, col_desc, col_ubic, col_estado, col_importe]].values
        
        for idx, row in enumerate(valores):
            try:
                inventario = str(int(float(row[0])))
            except:
                inventario = str(row[0])
            desc = str(row[1])[:40]
            ubicacion = str(row[2])
            estado = str(row[3])
            importe = str(row[4])
            
            self.tree.insert("", "end", 
                           values=(inventario, desc, ubicacion, estado, importe),
                           tags=(str(idx),))
    
    def mostrar_detalle(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        idx = int(item["tags"][0])
        
        registro = self.df.iloc[idx]
        
        detalle_window = tk.Toplevel(self.root)
        try:
            col_inv = self.encontrar_columna("N° INVENTARIO")
            num_inv = str(int(float(registro[col_inv])))
        except:
            col_inv = self.encontrar_columna("N° INVENTARIO")
            num_inv = str(registro[col_inv])
        detalle_window.title(f"📋 Detalle del Bien - Inventario: {num_inv}")
        detalle_window.geometry("700x680")
        detalle_window.configure(bg=LOG_COLORS["bg_main"])
        
        header = tk.Label(detalle_window,
                         text="📋 DETALLE COMPLETO DEL BIEN",
                         font=("Segoe UI", 14, "bold"),
                         fg=LOG_COLORS["accent_blue"], bg=LOG_COLORS["bg_main"])
        header.pack(pady=15)
        
        canvas = tk.Canvas(detalle_window, bg=LOG_COLORS["bg_main"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(detalle_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=LOG_COLORS["bg_main"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=(0, 10))
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=(0, 10))
        
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        campos_info = [
            ("N° INVENTARIO", "N° INVENTARIO", False),
            ("CABM", "CABM", False),
            ("DESCRIPCIÓN CABM", "DESCRIPCIÓN CABM", False),
            ("DESCRIPCIÓN DETALLE", "DESCRIPCIÓN DETALLE", False),
            ("UBICACIÓN", "UBICACIÓN", True),
            ("ESTADO DEL BIEN", "ESTADO DEL BIEN", True),
            ("MARCA", "MARCA", True),
            ("MODELO", "MODELO", True),
            ("SERIE", "SERIE", True),
            ("PROVEEDOR", "PROVEEDOR", True),
            ("N° CONTRATO", "N° CONTRATO", True),
            ("N° FACTURA", "N° FACTURA", True),
            ("FECHA DE ALTA", "FECHA DE ALTA", False),
            ("FECHA DOCUMENTO", "FECHA DOCUMENTO", False),
            ("PARTIDA CONTABLE", "PARTIDA CONTABLE", False),
            ("TIPO BIEN", "TIPO BIEN", False),
            ("NOMBRE COMPLETO", "NOMBRE COMPLETO", True),
            ("RFC", "RFC", False),
            ("UR", "UR", False),
            ("CT", "CT", False),
            ("PF", "PF", False),
            ("PP", "PP", False),
            ("IMPORTE", "IMPORTE", False),
            ("VALOR DEPRECIADO", "VALOR DEPRECIADO", False),
        ]
        
        entradas = {}
        
        def get_valor_df(registro, nombre_buscar):
            for col in registro.index:
                if nombre_buscar.upper() in col.upper():
                    return registro[col]
            return ""
        
        def get_nombre_columna(registro, nombre_buscar):
            for col in registro.index:
                if nombre_buscar.upper() in col.upper():
                    return col
            return nombre_buscar
        
        for campo, label, editable in campos_info:
            frame = tk.Frame(scrollable_frame, bg=LOG_COLORS["bg_dark"], pady=5, padx=10)
            frame.pack(fill="x", pady=2)
            
            tk.Label(frame,
                    text=f"{label}:",
                    font=("Segoe UI", 10, "bold"),
                    fg=LOG_COLORS["accent_blue"],
                    bg=LOG_COLORS["bg_dark"],
                    width=20,
                    anchor="w").pack(side="left")
            
            valor = str(get_valor_df(registro, campo))
            
            if editable:
                entrada = tk.Entry(frame,
                                  font=("Segoe UI", 10),
                                  bg=LOG_COLORS["bg_gray"],
                                  fg=LOG_COLORS["text_light"],
                                  insertbackground=LOG_COLORS["text_light"])
                entrada.insert(0, valor if valor != "nan" else "")
                entrada.pack(side="left", fill="x", expand=True)
                nombre_col = get_nombre_columna(registro, campo)
                entradas[nombre_col] = entrada
            else:
                color_valor = LOG_COLORS["text_light"]
                if label == "ESTADO DEL BIEN":
                    color_valor = ESTADO_COLORES.get(valor, LOG_COLORS["text_light"])
                
                tk.Label(frame,
                        text=valor if valor != "nan" else "N/A",
                        font=("Segoe UI", 10),
                        fg=color_valor,
                        bg=LOG_COLORS["bg_dark"],
                        anchor="w").pack(side="left", fill="x", expand=True)
        
        def guardar_cambios():
            try:
                cambios = []
                for nombre_col, entrada in entradas.items():
                    nuevo_valor = entrada.get().strip()
                    valor_anterior = str(self.df.at[idx, nombre_col])
                    self.df.at[idx, nombre_col] = nuevo_valor if nuevo_valor else None
                    cambios.append(f"{nombre_col}: {valor_anterior} -> {nuevo_valor}")
                
                self.df.to_excel(EXCEL_PATH, index=False, engine='openpyxl')
                
                log_accion("ACTUALIZACION", f"Inventario: {idx} | Cambios: {'; '.join(cambios)}")
                
                canvas.unbind_all("<MouseWheel>")
                messagebox.showinfo("Éxito", "Cambios guardados correctamente en el Excel")
                detalle_window.destroy()
                self.llenar_tabla(self.df)
            except Exception as e:
                log_accion("ERROR_ACTUALIZACION", str(e))
                messagebox.showerror("Error", f"No se pudieron guardar los cambios:\n{e}")
        
        def dar_de_baja():
            respuesta = messagebox.askyesno("Confirmar Baja", "¿Está seguro de dar de BAJA este bien?")
            if respuesta:
                try:
                    col_inv = self.encontrar_columna("N° INVENTARIO")
                    num_inv = self.df.at[idx, col_inv]
                    self.df.at[idx, 'STATUS'] = 0
                    self.df.to_excel(EXCEL_PATH, index=False, engine='openpyxl')
                    log_accion("BAJA", f"Inventario: {num_inv}")
                    canvas.unbind_all("<MouseWheel>")
                    messagebox.showinfo("Éxito", "Bien dado de BAJA correctamente")
                    detalle_window.destroy()
                    self.buscar()
                except Exception as e:
                    log_accion("ERROR_BAJA", str(e))
                    messagebox.showerror("Error", f"No se pudo dar de baja:\n{e}")
        
        btn_frame = tk.Frame(detalle_window, bg=LOG_COLORS["bg_main"])
        btn_frame.pack(pady=20)
        
        btn_guardar = tk.Button(btn_frame,
                              text="💾 GUARDAR CAMBIOS",
                              command=guardar_cambios,
                              bg=LOG_COLORS["success"],
                              fg=LOG_COLORS["bg_main"],
                              font=("Segoe UI", 11, "bold"),
                              relief="flat",
                              padx=30, pady=12,
                              width=25)
        btn_guardar.pack(pady=5)
        
        btn_baja = tk.Button(btn_frame,
                            text="🗑️ DAR DE BAJA",
                            command=dar_de_baja,
                            bg=LOG_COLORS["accent_yellow"],
                            fg=LOG_COLORS["bg_main"],
                            font=("Segoe UI", 11, "bold"),
                            relief="flat",
                            padx=30, pady=12,
                            width=25)
        btn_baja.pack(pady=5)
        
        def cerrar_ventana():
            canvas.unbind_all("<MouseWheel>")
            detalle_window.destroy()
        
        btn_cancelar = tk.Button(btn_frame,
                               text="CANCELAR",
                               command=cerrar_ventana,
                               bg=LOG_COLORS["danger"],
                               fg=LOG_COLORS["bg_main"],
                               font=("Segoe UI", 11, "bold"),
                               relief="flat",
                               padx=30, pady=12,
                               width=25)
        btn_cancelar.pack(pady=5)

    def cruzar_inventario(self):
        try:
            nuevo_path = os.path.join(BASE_DIR, "archivo_cruzar", "ARCHIVO_NUEVO.xlsx")
            
            if not os.path.exists(nuevo_path):
                messagebox.showerror("Error", f"No se encuentra el archivo:\n{nuevo_path}\n\nColoca el archivo a cruzar en esa ubicación.")
                return
            
            log_accion("CRUZE_INVENTARIO_INICIO", "Iniciando cruze por N° INVENTARIO")
            
            df_base = self.df.copy()
            df_nuevo = pd.read_excel(nuevo_path)
            
            col_inv = self.encontrar_columna("N° INVENTARIO")
            df_base[col_inv] = df_base[col_inv].astype(str).str.strip()
            df_nuevo[col_inv] = df_nuevo[col_inv].astype(str).str.strip()
            
            inv_base = set(df_base[col_inv].unique())
            
            existentes = df_nuevo[df_nuevo[col_inv].isin(inv_base)]
            faltantes = df_nuevo[~df_nuevo[col_inv].isin(inv_base)]
            
            output_file = os.path.join(BASE_DIR, "INFORME_CRUZE_INVENTARIO.xlsx")
            
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                existentes.to_excel(writer, sheet_name='Existentes', index=False)
                faltantes.to_excel(writer, sheet_name='Faltantes', index=False)
            
            log_accion("CRUZE_INVENTARIO_FIN", f"Existentes: {len(existentes)}, Faltantes: {len(faltantes)}")
            
            messagebox.showinfo("Cruze por Inventario", 
                f"Cruce realizado solo por N° INVENTARIO\n\n"
                f"Resultados:\n"
                f"• Existentes (match): {len(existentes)}\n"
                f"• Faltantes: {len(faltantes)}\n\n"
                f"Informe: {output_file}")
            
            os.startfile(output_file)
            
        except Exception as e:
            log_accion("ERROR_CRUXE_INVENTARIO", str(e))
            messagebox.showerror("Error", f"Error al realizar el cruze:\n{e}")
    
    def cruzar_inv_cabm(self):
        try:
            nuevo_path = os.path.join(BASE_DIR, "archivo_cruzar", "ARCHIVO_NUEVO.xlsx")
            
            if not os.path.exists(nuevo_path):
                messagebox.showerror("Error", f"No se encuentra el archivo:\n{nuevo_path}\n\nColoca el archivo a cruzar en esa ubicación.")
                return
            
            log_accion("CRUZE_INV_CABM_INICIO", "Iniciando cruze por N° INVENTARIO + CABM")
            
            df_base = self.df.copy()
            df_nuevo = pd.read_excel(nuevo_path)
            
            col_inv = self.encontrar_columna("N° INVENTARIO")
            col_cabm = self.encontrar_columna("CABM")
            
            df_base[col_inv] = df_base[col_inv].astype(str).str.strip()
            df_nuevo[col_inv] = df_nuevo[col_inv].astype(str).str.strip()
            df_base[col_cabm] = df_base[col_cabm].astype(str).str.strip()
            df_nuevo[col_cabm] = df_nuevo[col_cabm].astype(str).str.strip()
            
            df_base['CLAVE_CRUEZE'] = df_base[col_inv] + '|' + df_base[col_cabm]
            df_nuevo['CLAVE_CRUEZE'] = df_nuevo[col_inv] + '|' + df_nuevo[col_cabm]
            
            claves_base = set(df_base['CLAVE_CRUEZE'].unique())
            
            existentes = df_nuevo[df_nuevo['CLAVE_CRUEZE'].isin(claves_base)]
            faltantes = df_nuevo[~df_nuevo['CLAVE_CRUEZE'].isin(claves_base)]
            
            output_file = os.path.join(BASE_DIR, "INFORME_CRUZE_INV_CABM.xlsx")
            
            df_existentes = existentes.drop(columns=['CLAVE_CRUEZE'])
            df_faltantes = faltantes.drop(columns=['CLAVE_CRUEZE'])
            
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                df_existentes.to_excel(writer, sheet_name='Existentes', index=False)
                df_faltantes.to_excel(writer, sheet_name='Faltantes', index=False)
            
            log_accion("CRUZE_INV_CABM_FIN", f"Existentes: {len(existentes)}, Faltantes: {len(faltantes)}")
            
            messagebox.showinfo("Cruze por Inventario + CABM", 
                f"Cruce realizado por N° INVENTARIO + CABM\n\n"
                f"Resultados:\n"
                f"• Existentes (match): {len(existentes)}\n"
                f"• Faltantes: {len(faltantes)}\n\n"
                f"Informe: {output_file}")
            
            os.startfile(output_file)
            
        except Exception as e:
            log_accion("ERROR_CRUXE_INV_CABM", str(e))
            messagebox.showerror("Error", f"Error al realizar el cruze:\n{e}")

def main():
    root = tk.Tk()
    app = BuscadorBienes(root)
    root.mainloop()

if __name__ == "__main__":
    main()
