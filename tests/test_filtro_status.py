"""
Pruebas para el filtro de STATUS en BuscadorBienes._obtener_df_filtrado().

Comportamiento esperado:
- "VIGENTES" → sólo filas con STATUS == 1.
- "BAJAS"    → sólo filas con STATUS == 0.
- "TODOS"    → todas las filas sin importar STATUS.
- El resultado es siempre una copia del DataFrame, no una referencia.
"""
import pandas as pd
import pytest
from unittest.mock import MagicMock

from buscador_bienes import BuscadorBienes, FILTRO_STATUS


def _mock_app_con_filtro(df, filtro_valor):
    """Instancia simulada con el filtro de status configurado."""
    inst = MagicMock(spec=BuscadorBienes)
    inst.df = df
    inst.filtro_status = MagicMock()
    inst.filtro_status.get.return_value = filtro_valor
    inst._obtener_df_filtrado = lambda: BuscadorBienes._obtener_df_filtrado(inst)
    return inst


class TestConstantesFiltroStatus:
    def test_vigentes_equivale_a_status_uno(self):
        assert FILTRO_STATUS["VIGENTES"] == 1

    def test_bajas_equivale_a_status_cero(self):
        assert FILTRO_STATUS["BAJAS"] == 0

    def test_todos_equivale_a_none(self):
        assert FILTRO_STATUS["TODOS"] is None

    def test_claves_existentes(self):
        assert set(FILTRO_STATUS.keys()) == {"VIGENTES", "BAJAS", "TODOS"}


class TestFiltroVigentes:
    def test_solo_retorna_filas_con_status_uno(self, df_bienes):
        app = _mock_app_con_filtro(df_bienes, "VIGENTES")
        resultado = app._obtener_df_filtrado()
        assert all(resultado["STATUS"] == 1)

    def test_conteo_correcto(self, df_bienes):
        app = _mock_app_con_filtro(df_bienes, "VIGENTES")
        resultado = app._obtener_df_filtrado()
        esperado = len(df_bienes[df_bienes["STATUS"] == 1])
        assert len(resultado) == esperado

    def test_no_incluye_bajas(self, df_bienes):
        app = _mock_app_con_filtro(df_bienes, "VIGENTES")
        resultado = app._obtener_df_filtrado()
        assert 0 not in resultado["STATUS"].values


class TestFiltroBajas:
    def test_solo_retorna_filas_con_status_cero(self, df_bienes):
        app = _mock_app_con_filtro(df_bienes, "BAJAS")
        resultado = app._obtener_df_filtrado()
        assert all(resultado["STATUS"] == 0)

    def test_conteo_correcto(self, df_bienes):
        app = _mock_app_con_filtro(df_bienes, "BAJAS")
        resultado = app._obtener_df_filtrado()
        esperado = len(df_bienes[df_bienes["STATUS"] == 0])
        assert len(resultado) == esperado

    def test_no_incluye_vigentes(self, df_bienes):
        app = _mock_app_con_filtro(df_bienes, "BAJAS")
        resultado = app._obtener_df_filtrado()
        assert 1 not in resultado["STATUS"].values


class TestFiltroTodos:
    def test_retorna_todos_los_registros(self, df_bienes):
        app = _mock_app_con_filtro(df_bienes, "TODOS")
        resultado = app._obtener_df_filtrado()
        assert len(resultado) == len(df_bienes)

    def test_incluye_vigentes_y_bajas(self, df_bienes):
        app = _mock_app_con_filtro(df_bienes, "TODOS")
        resultado = app._obtener_df_filtrado()
        assert set(resultado["STATUS"].unique()) == {0, 1}


class TestFiltroEsCopia:
    def test_resultado_no_es_la_misma_referencia(self, df_bienes):
        """El filtro debe devolver una copia para evitar mutaciones inesperadas."""
        app = _mock_app_con_filtro(df_bienes, "TODOS")
        resultado = app._obtener_df_filtrado()
        assert resultado is not app.df

    def test_modificar_resultado_no_altera_df_original(self, df_bienes):
        app = _mock_app_con_filtro(df_bienes, "TODOS")
        resultado = app._obtener_df_filtrado()
        original_len = len(app.df)
        resultado.drop(resultado.index[0], inplace=True)
        assert len(app.df) == original_len


class TestFiltroDfVacio:
    def test_vigentes_con_df_vacio_retorna_vacio(self):
        df_vacio = pd.DataFrame({"STATUS": pd.Series([], dtype=int)})
        app = _mock_app_con_filtro(df_vacio, "VIGENTES")
        resultado = app._obtener_df_filtrado()
        assert len(resultado) == 0

    def test_todos_con_df_vacio_retorna_vacio(self):
        df_vacio = pd.DataFrame({"STATUS": pd.Series([], dtype=int)})
        app = _mock_app_con_filtro(df_vacio, "TODOS")
        resultado = app._obtener_df_filtrado()
        assert len(resultado) == 0
