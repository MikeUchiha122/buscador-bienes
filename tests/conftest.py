"""
Configuración compartida para todas las pruebas.

Importante: tkinter se debe suprimir ANTES de importar buscador_bienes,
ya que el módulo ejecuta código de GUI al importarse.
"""
import sys
from unittest.mock import MagicMock

# Suprimir tkinter para que el módulo pueda importarse sin display gráfico
for _mod in ["tkinter", "tkinter.ttk", "tkinter.messagebox"]:
    sys.modules[_mod] = MagicMock()

import pandas as pd
import pytest


@pytest.fixture
def df_bienes():
    """DataFrame típico con la estructura completa de la aplicación."""
    return pd.DataFrame(
        {
            "N° INVENTARIO": [1001, 1002, 1003, 1004, 1005],
            "DESCRIPCIÓN DETALLE": [
                "LAPTOP HP PROBOOK",
                "SILLA ERGONÓMICA NEGRA",
                'MONITOR DELL 24"',
                "ESCRITORIO DE MADERA",
                "IMPRESORA LASER CANON",
            ],
            "UBICACIÓN": [
                "OFICINA A",
                "SALA JUNTAS",
                "OFICINA A",
                "BODEGA",
                "OFICINA B",
            ],
            "ESTADO DEL BIEN": ["BUENO", "REGULAR", "MALO", "BUENO", "REGULAR"],
            "CABM": ["5010", "5020", "5010", "5030", "5040"],
            "IMPORTE": [15000.0, 3000.0, 8000.0, 5000.0, 12000.0],
            "STATUS": [1, 1, 0, 1, 0],
        }
    )


@pytest.fixture
def df_bienes_sin_status():
    """DataFrame sin columna STATUS para probar la creación automática."""
    return pd.DataFrame(
        {
            "N° INVENTARIO": [2001, 2002],
            "DESCRIPCIÓN DETALLE": ["ESCÁNER CANON", "PROYECTOR EPSON"],
            "UBICACIÓN": ["RECEPCIÓN", "SALA DE CAPACITACIÓN"],
            "ESTADO DEL BIEN": ["BUENO", "BUENO"],
            "CABM": ["6010", "6020"],
            "IMPORTE": [4500.0, 22000.0],
        }
    )


@pytest.fixture
def df_bienes_con_nan():
    """DataFrame con valores NaN para probar el manejo de datos nulos."""
    return pd.DataFrame(
        {
            "N° INVENTARIO": [3001, None, 3003],
            "DESCRIPCIÓN DETALLE": ["TECLADO", None, "MOUSE"],
            "UBICACIÓN": [None, "ALMACÉN", "ALMACÉN"],
            "ESTADO DEL BIEN": ["BUENO", None, "MALO"],
            "CABM": ["7010", "7020", None],
            "IMPORTE": [500.0, None, 250.0],
            "STATUS": [1, 1, 1],
        }
    )
