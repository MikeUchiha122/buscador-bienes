"""
Pruebas de integración para las funciones de cruce de inventarios.

Cubre:
1. cruzar_bienes.cruzar_por_cabm()        — cruce por código CABM
2. cruzar_inventario.cruzar_por_inventario() — cruce por N° INVENTARIO
3. BuscadorBienes.cruzar_inventario()     — cruce por N° INVENTARIO desde la GUI
4. BuscadorBienes.cruzar_inv_cabm()       — cruce por N° INVENTARIO + CABM desde la GUI

Las pruebas de los scripts standalone usan archivos Excel temporales reales
(tmp_path + monkeypatch.chdir) para verificar la lógica de cruce de extremo a extremo.
Las pruebas de los métodos de BuscadorBienes usan mocks + archivos temporales.
"""
import os
import pandas as pd
import pytest
from unittest.mock import MagicMock, patch

from cruzar_bienes import cruzar_por_cabm
from cruzar_inventario import cruzar_por_inventario
from buscador_bienes import BuscadorBienes


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _crear_excel(path, df):
    """Escribe un DataFrame en un archivo Excel."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(path, index=False)


def _leer_hoja(path, sheet):
    return pd.read_excel(path, sheet_name=sheet)


# ---------------------------------------------------------------------------
# cruzar_por_cabm (script standalone)
# ---------------------------------------------------------------------------

class TestCruzarPorCABM:
    def test_coincidencia_total(self, tmp_path, monkeypatch):
        df_base = pd.DataFrame({"CABM": ["A", "B", "C"]})
        df_nuevo = pd.DataFrame({"CABM": ["A", "B", "C"]})
        _crear_excel(tmp_path / "BASE_BIENES_UNIDAD.xlsx", df_base)
        _crear_excel(tmp_path / "archivo_cruzar" / "ARCHIVO_NUEVO.xlsx", df_nuevo)
        monkeypatch.chdir(tmp_path)

        cruzar_por_cabm()

        existentes = _leer_hoja(tmp_path / "INFORME_CRUZE.xlsx", "Existentes")
        faltantes = _leer_hoja(tmp_path / "INFORME_CRUZE.xlsx", "Faltantes")
        assert len(existentes) == 3
        assert len(faltantes) == 0

    def test_sin_coincidencias(self, tmp_path, monkeypatch):
        df_base = pd.DataFrame({"CABM": ["A", "B"]})
        df_nuevo = pd.DataFrame({"CABM": ["X", "Y", "Z"]})
        _crear_excel(tmp_path / "BASE_BIENES_UNIDAD.xlsx", df_base)
        _crear_excel(tmp_path / "archivo_cruzar" / "ARCHIVO_NUEVO.xlsx", df_nuevo)
        monkeypatch.chdir(tmp_path)

        cruzar_por_cabm()

        existentes = _leer_hoja(tmp_path / "INFORME_CRUZE.xlsx", "Existentes")
        faltantes = _leer_hoja(tmp_path / "INFORME_CRUZE.xlsx", "Faltantes")
        assert len(existentes) == 0
        assert len(faltantes) == 3

    def test_coincidencia_parcial(self, tmp_path, monkeypatch):
        df_base = pd.DataFrame({"CABM": ["A", "B", "C"]})
        df_nuevo = pd.DataFrame({"CABM": ["B", "C", "D", "E"]})
        _crear_excel(tmp_path / "BASE_BIENES_UNIDAD.xlsx", df_base)
        _crear_excel(tmp_path / "archivo_cruzar" / "ARCHIVO_NUEVO.xlsx", df_nuevo)
        monkeypatch.chdir(tmp_path)

        cruzar_por_cabm()

        existentes = _leer_hoja(tmp_path / "INFORME_CRUZE.xlsx", "Existentes")
        faltantes = _leer_hoja(tmp_path / "INFORME_CRUZE.xlsx", "Faltantes")
        assert len(existentes) == 2  # B y C
        assert len(faltantes) == 2   # D y E

    def test_elimina_espacios_en_cabm(self, tmp_path, monkeypatch):
        """Los valores con espacios deben normalizarse antes de comparar."""
        df_base = pd.DataFrame({"CABM": ["  5010  ", "5020"]})
        df_nuevo = pd.DataFrame({"CABM": ["5010", "5020", "5030"]})
        _crear_excel(tmp_path / "BASE_BIENES_UNIDAD.xlsx", df_base)
        _crear_excel(tmp_path / "archivo_cruzar" / "ARCHIVO_NUEVO.xlsx", df_nuevo)
        monkeypatch.chdir(tmp_path)

        cruzar_por_cabm()

        existentes = _leer_hoja(tmp_path / "INFORME_CRUZE.xlsx", "Existentes")
        assert len(existentes) == 2  # 5010 y 5020 coinciden

    def test_cabm_con_duplicados_en_nuevo(self, tmp_path, monkeypatch):
        """Duplicados en el archivo nuevo no deben colapsarse."""
        df_base = pd.DataFrame({"CABM": ["A"]})
        df_nuevo = pd.DataFrame({"CABM": ["A", "A", "B"]})
        _crear_excel(tmp_path / "BASE_BIENES_UNIDAD.xlsx", df_base)
        _crear_excel(tmp_path / "archivo_cruzar" / "ARCHIVO_NUEVO.xlsx", df_nuevo)
        monkeypatch.chdir(tmp_path)

        cruzar_por_cabm()

        existentes = _leer_hoja(tmp_path / "INFORME_CRUZE.xlsx", "Existentes")
        faltantes = _leer_hoja(tmp_path / "INFORME_CRUZE.xlsx", "Faltantes")
        assert len(existentes) == 2  # las dos filas con "A"
        assert len(faltantes) == 1   # "B"

    def test_genera_archivo_de_salida(self, tmp_path, monkeypatch):
        df_base = pd.DataFrame({"CABM": ["A"]})
        df_nuevo = pd.DataFrame({"CABM": ["A"]})
        _crear_excel(tmp_path / "BASE_BIENES_UNIDAD.xlsx", df_base)
        _crear_excel(tmp_path / "archivo_cruzar" / "ARCHIVO_NUEVO.xlsx", df_nuevo)
        monkeypatch.chdir(tmp_path)

        cruzar_por_cabm()

        assert (tmp_path / "INFORME_CRUZE.xlsx").exists()

    def test_archivo_base_no_existe(self, tmp_path, monkeypatch, capsys):
        """Si no existe la base, la función termina silenciosamente."""
        monkeypatch.chdir(tmp_path)
        cruzar_por_cabm()
        capturado = capsys.readouterr()
        assert "Error" in capturado.out


# ---------------------------------------------------------------------------
# cruzar_por_inventario (script standalone)
# ---------------------------------------------------------------------------

class TestCruzarPorInventario:
    def test_coincidencia_total(self, tmp_path, monkeypatch):
        df_base = pd.DataFrame({"N° INVENTARIO": [1001, 1002, 1003]})
        df_nuevo = pd.DataFrame({"N° INVENTARIO": [1001, 1002, 1003]})
        _crear_excel(tmp_path / "BASE_BIENES_UNIDAD.xlsx", df_base)
        _crear_excel(tmp_path / "archivo_cruzar" / "ARCHIVO_NUEVO.xlsx", df_nuevo)
        monkeypatch.chdir(tmp_path)

        cruzar_por_inventario()

        existentes = _leer_hoja(tmp_path / "INFORME_CRUZE_INVENTARIO.xlsx", "Existentes")
        faltantes = _leer_hoja(tmp_path / "INFORME_CRUZE_INVENTARIO.xlsx", "Faltantes")
        assert len(existentes) == 3
        assert len(faltantes) == 0

    def test_sin_coincidencias(self, tmp_path, monkeypatch):
        df_base = pd.DataFrame({"N° INVENTARIO": [1001, 1002]})
        df_nuevo = pd.DataFrame({"N° INVENTARIO": [9001, 9002, 9003]})
        _crear_excel(tmp_path / "BASE_BIENES_UNIDAD.xlsx", df_base)
        _crear_excel(tmp_path / "archivo_cruzar" / "ARCHIVO_NUEVO.xlsx", df_nuevo)
        monkeypatch.chdir(tmp_path)

        cruzar_por_inventario()

        existentes = _leer_hoja(tmp_path / "INFORME_CRUZE_INVENTARIO.xlsx", "Existentes")
        faltantes = _leer_hoja(tmp_path / "INFORME_CRUZE_INVENTARIO.xlsx", "Faltantes")
        assert len(existentes) == 0
        assert len(faltantes) == 3

    def test_coincidencia_parcial(self, tmp_path, monkeypatch):
        df_base = pd.DataFrame({"N° INVENTARIO": [1001, 1002, 1003]})
        df_nuevo = pd.DataFrame({"N° INVENTARIO": [1002, 1003, 1004, 1005]})
        _crear_excel(tmp_path / "BASE_BIENES_UNIDAD.xlsx", df_base)
        _crear_excel(tmp_path / "archivo_cruzar" / "ARCHIVO_NUEVO.xlsx", df_nuevo)
        monkeypatch.chdir(tmp_path)

        cruzar_por_inventario()

        existentes = _leer_hoja(tmp_path / "INFORME_CRUZE_INVENTARIO.xlsx", "Existentes")
        faltantes = _leer_hoja(tmp_path / "INFORME_CRUZE_INVENTARIO.xlsx", "Faltantes")
        assert len(existentes) == 2   # 1002 y 1003
        assert len(faltantes) == 2    # 1004 y 1005

    def test_elimina_espacios_en_inventario(self, tmp_path, monkeypatch):
        df_base = pd.DataFrame({"N° INVENTARIO": ["  1001  ", "1002"]})
        df_nuevo = pd.DataFrame({"N° INVENTARIO": ["1001", "1003"]})
        _crear_excel(tmp_path / "BASE_BIENES_UNIDAD.xlsx", df_base)
        _crear_excel(tmp_path / "archivo_cruzar" / "ARCHIVO_NUEVO.xlsx", df_nuevo)
        monkeypatch.chdir(tmp_path)

        cruzar_por_inventario()

        existentes = _leer_hoja(tmp_path / "INFORME_CRUZE_INVENTARIO.xlsx", "Existentes")
        assert len(existentes) == 1  # sólo 1001

    def test_genera_archivo_de_salida(self, tmp_path, monkeypatch):
        df_base = pd.DataFrame({"N° INVENTARIO": [1001]})
        df_nuevo = pd.DataFrame({"N° INVENTARIO": [1001]})
        _crear_excel(tmp_path / "BASE_BIENES_UNIDAD.xlsx", df_base)
        _crear_excel(tmp_path / "archivo_cruzar" / "ARCHIVO_NUEVO.xlsx", df_nuevo)
        monkeypatch.chdir(tmp_path)

        cruzar_por_inventario()

        assert (tmp_path / "INFORME_CRUZE_INVENTARIO.xlsx").exists()

    def test_archivo_base_no_existe(self, tmp_path, monkeypatch, capsys):
        monkeypatch.chdir(tmp_path)
        cruzar_por_inventario()
        capturado = capsys.readouterr()
        assert "Error" in capturado.out


# ---------------------------------------------------------------------------
# BuscadorBienes.cruzar_inventario() — método de la clase GUI
# ---------------------------------------------------------------------------

def _mock_app_cruzar(df_base, tmp_path):
    """Instancia simulada con df cargado y base en directorio temporal."""
    inst = MagicMock(spec=BuscadorBienes)
    inst.df = df_base.copy()
    inst._cache_columnas = {}
    inst.encontrar_columna = lambda n: BuscadorBienes.encontrar_columna(inst, n)
    return inst


class TestBuscadorCruzarInventario:
    def test_coincidencia_total_genera_informe(self, tmp_path):
        df_base = pd.DataFrame({
            "N° INVENTARIO": [1001, 1002, 1003],
            "DESCRIPCIÓN DETALLE": ["A", "B", "C"],
            "STATUS": [1, 1, 1],
        })
        df_nuevo = pd.DataFrame({"N° INVENTARIO": [1001, 1002, 1003]})
        nuevo_path = tmp_path / "archivo_cruzar" / "ARCHIVO_NUEVO.xlsx"
        _crear_excel(nuevo_path, df_nuevo)

        inst = _mock_app_cruzar(df_base, tmp_path)

        with (
            patch("buscador_bienes.BASE_DIR", str(tmp_path)),
            patch("buscador_bienes.os.startfile", create=True),
        ):
            BuscadorBienes.cruzar_inventario(inst)

        informe = tmp_path / "INFORME_CRUZE_INVENTARIO.xlsx"
        assert informe.exists()
        existentes = _leer_hoja(informe, "Existentes")
        faltantes = _leer_hoja(informe, "Faltantes")
        assert len(existentes) == 3
        assert len(faltantes) == 0

    def test_faltantes_detectados_correctamente(self, tmp_path):
        df_base = pd.DataFrame({
            "N° INVENTARIO": [1001, 1002],
            "STATUS": [1, 1],
        })
        df_nuevo = pd.DataFrame({"N° INVENTARIO": [1001, 9999]})
        nuevo_path = tmp_path / "archivo_cruzar" / "ARCHIVO_NUEVO.xlsx"
        _crear_excel(nuevo_path, df_nuevo)

        inst = _mock_app_cruzar(df_base, tmp_path)

        with (
            patch("buscador_bienes.BASE_DIR", str(tmp_path)),
            patch("buscador_bienes.os.startfile", create=True),
        ):
            BuscadorBienes.cruzar_inventario(inst)

        informe = tmp_path / "INFORME_CRUZE_INVENTARIO.xlsx"
        faltantes = _leer_hoja(informe, "Faltantes")
        assert len(faltantes) == 1
        assert str(faltantes["N° INVENTARIO"].iloc[0]) == "9999"

    def test_archivo_nuevo_no_encontrado(self, tmp_path):
        df_base = pd.DataFrame({"N° INVENTARIO": [1001], "STATUS": [1]})
        inst = _mock_app_cruzar(df_base, tmp_path)

        with patch("buscador_bienes.BASE_DIR", str(tmp_path)):
            BuscadorBienes.cruzar_inventario(inst)

        # Debe haber mostrado error sin generar informe
        inst.encontrar_columna  # no lanza excepción
        assert not (tmp_path / "INFORME_CRUZE_INVENTARIO.xlsx").exists()


# ---------------------------------------------------------------------------
# BuscadorBienes.cruzar_inv_cabm() — método de la clase GUI
# ---------------------------------------------------------------------------

class TestBuscadorCruzarInvCABM:
    def test_requiere_coincidencia_de_inventario_y_cabm(self, tmp_path):
        """Un registro que coincide en inventario pero no en CABM debe ir a Faltantes."""
        df_base = pd.DataFrame({
            "N° INVENTARIO": [1001, 1002],
            "CABM": ["5010", "5020"],
            "STATUS": [1, 1],
        })
        # 1001 tiene CABM diferente → faltante
        # 1002 coincide en ambos → existente
        df_nuevo = pd.DataFrame({
            "N° INVENTARIO": [1001, 1002],
            "CABM": ["9999", "5020"],
        })
        nuevo_path = tmp_path / "archivo_cruzar" / "ARCHIVO_NUEVO.xlsx"
        _crear_excel(nuevo_path, df_nuevo)

        inst = _mock_app_cruzar(df_base, tmp_path)

        with (
            patch("buscador_bienes.BASE_DIR", str(tmp_path)),
            patch("buscador_bienes.os.startfile", create=True),
        ):
            BuscadorBienes.cruzar_inv_cabm(inst)

        informe = tmp_path / "INFORME_CRUZE_INV_CABM.xlsx"
        assert informe.exists()
        existentes = _leer_hoja(informe, "Existentes")
        faltantes = _leer_hoja(informe, "Faltantes")
        assert len(existentes) == 1
        assert len(faltantes) == 1

    def test_coincidencia_total_inv_cabm(self, tmp_path):
        df_base = pd.DataFrame({
            "N° INVENTARIO": [1001, 1002],
            "CABM": ["5010", "5020"],
            "STATUS": [1, 1],
        })
        df_nuevo = pd.DataFrame({
            "N° INVENTARIO": [1001, 1002],
            "CABM": ["5010", "5020"],
        })
        nuevo_path = tmp_path / "archivo_cruzar" / "ARCHIVO_NUEVO.xlsx"
        _crear_excel(nuevo_path, df_nuevo)

        inst = _mock_app_cruzar(df_base, tmp_path)

        with (
            patch("buscador_bienes.BASE_DIR", str(tmp_path)),
            patch("buscador_bienes.os.startfile", create=True),
        ):
            BuscadorBienes.cruzar_inv_cabm(inst)

        informe = tmp_path / "INFORME_CRUZE_INV_CABM.xlsx"
        existentes = _leer_hoja(informe, "Existentes")
        faltantes = _leer_hoja(informe, "Faltantes")
        assert len(existentes) == 2
        assert len(faltantes) == 0

    def test_columna_clave_cruce_no_aparece_en_salida(self, tmp_path):
        """La columna auxiliar CLAVE_CRUEZE no debe aparecer en el informe final."""
        df_base = pd.DataFrame({
            "N° INVENTARIO": [1001],
            "CABM": ["5010"],
            "STATUS": [1],
        })
        df_nuevo = pd.DataFrame({
            "N° INVENTARIO": [1001],
            "CABM": ["5010"],
        })
        nuevo_path = tmp_path / "archivo_cruzar" / "ARCHIVO_NUEVO.xlsx"
        _crear_excel(nuevo_path, df_nuevo)

        inst = _mock_app_cruzar(df_base, tmp_path)

        with (
            patch("buscador_bienes.BASE_DIR", str(tmp_path)),
            patch("buscador_bienes.os.startfile", create=True),
        ):
            BuscadorBienes.cruzar_inv_cabm(inst)

        informe = tmp_path / "INFORME_CRUZE_INV_CABM.xlsx"
        existentes = _leer_hoja(informe, "Existentes")
        assert "CLAVE_CRUEZE" not in existentes.columns
