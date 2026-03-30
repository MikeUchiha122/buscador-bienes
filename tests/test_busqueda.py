"""
Pruebas para la lógica de búsqueda en BuscadorBienes.buscar().

Comportamiento esperado:
- Criterio vacío → devuelve todos los registros del filtro de status activo.
- Búsqueda en "Todos" → coincidencia exacta de elemento en alguna columna.
- Búsqueda en campo específico → subcadena (str.contains, regex=False).
- El criterio se normaliza: strip + upper + eliminar espacios antes de buscar.
- Si no hay resultados, llenar_tabla recibe el DataFrame completo filtrado (no vacío).

Nota sobre "Buscar en Todos":
  El código usa: criterio in row.astype(str).values
  Esto comprueba si el criterio es exactamente igual a algún elemento de la fila.
  Por tanto, "LAPTOP" NO coincide con "LAPTOP HP PROBOOK", pero SÍ con "BUENO",
  "5010", "1001", etc.  Para buscar subcadenas en un campo concreto se usa
  str.contains, que SÍ hace coincidencia parcial.
"""
import pandas as pd
import pytest
from unittest.mock import MagicMock

from buscador_bienes import BuscadorBienes


def _mock_app_busqueda(df, criterio="", campo="Todos", filtro="TODOS"):
    """Instancia simulada con toda la infraestructura de buscar() conectada."""
    inst = MagicMock(spec=BuscadorBienes)
    inst.df = df.copy()
    inst._cache_columnas = {}

    inst.buscar_var = MagicMock()
    inst.buscar_var.get.return_value = criterio

    inst.campo_busqueda = MagicMock()
    inst.campo_busqueda.get.return_value = campo

    inst.filtro_status = MagicMock()
    inst.filtro_status.get.return_value = filtro

    # Conectar los métodos reales de negocio
    inst.encontrar_columna = lambda n: BuscadorBienes.encontrar_columna(inst, n)
    inst._obtener_df_filtrado = lambda: BuscadorBienes._obtener_df_filtrado(inst)

    return inst


def _df_resultado(app):
    """Extrae el DataFrame que se pasó a llenar_tabla en la última llamada."""
    return app.llenar_tabla.call_args[0][0]


# ---------------------------------------------------------------------------
# Criterio vacío
# ---------------------------------------------------------------------------

class TestBusquedaCriterioVacio:
    def test_criterio_vacio_muestra_todos_vigentes(self, df_bienes):
        app = _mock_app_busqueda(df_bienes, criterio="", filtro="VIGENTES")
        BuscadorBienes.buscar(app)
        resultado = _df_resultado(app)
        assert all(resultado["STATUS"] == 1)

    def test_criterio_vacio_con_filtro_todos_muestra_todo(self, df_bienes):
        app = _mock_app_busqueda(df_bienes, criterio="", filtro="TODOS")
        BuscadorBienes.buscar(app)
        resultado = _df_resultado(app)
        assert len(resultado) == len(df_bienes)

    def test_criterio_solo_espacios_equivale_a_vacio(self, df_bienes):
        app = _mock_app_busqueda(df_bienes, criterio="   ", filtro="TODOS")
        BuscadorBienes.buscar(app)
        resultado = _df_resultado(app)
        assert len(resultado) == len(df_bienes)


# ---------------------------------------------------------------------------
# Búsqueda en campo específico (subcadena)
# ---------------------------------------------------------------------------

class TestBusquedaEnCampoEspecifico:
    def test_subcadena_en_descripcion(self, df_bienes):
        app = _mock_app_busqueda(
            df_bienes, criterio="LAPTOP", campo="DESCRIPCIÓN DETALLE", filtro="TODOS"
        )
        BuscadorBienes.buscar(app)
        resultado = _df_resultado(app)
        assert len(resultado) == 1
        assert "LAPTOP" in resultado["DESCRIPCIÓN DETALLE"].values[0]

    def test_subcadena_en_ubicacion(self, df_bienes):
        app = _mock_app_busqueda(
            df_bienes, criterio="OFICINA", campo="UBICACIÓN", filtro="TODOS"
        )
        BuscadorBienes.buscar(app)
        resultado = _df_resultado(app)
        assert all("OFICINA" in v for v in resultado["UBICACIÓN"].values)

    def test_busqueda_por_estado_exacto(self, df_bienes):
        app = _mock_app_busqueda(
            df_bienes, criterio="BUENO", campo="ESTADO DEL BIEN", filtro="TODOS"
        )
        BuscadorBienes.buscar(app)
        resultado = _df_resultado(app)
        assert all(v == "BUENO" for v in resultado["ESTADO DEL BIEN"].values)

    def test_busqueda_por_cabm(self, df_bienes):
        app = _mock_app_busqueda(
            df_bienes, criterio="5010", campo="CABM", filtro="TODOS"
        )
        BuscadorBienes.buscar(app)
        resultado = _df_resultado(app)
        assert all(v == "5010" for v in resultado["CABM"].values)
        assert len(resultado) == 2  # hay dos bienes con CABM 5010

    def test_campo_especifico_con_filtro_vigentes(self, df_bienes):
        """La búsqueda por campo respeta el filtro de status."""
        app = _mock_app_busqueda(
            df_bienes, criterio="OFICINA", campo="UBICACIÓN", filtro="VIGENTES"
        )
        BuscadorBienes.buscar(app)
        resultado = _df_resultado(app)
        assert all(resultado["STATUS"] == 1)
        assert all("OFICINA" in v for v in resultado["UBICACIÓN"].values)


# ---------------------------------------------------------------------------
# Búsqueda en "Todos" los campos (coincidencia exacta por elemento)
# ---------------------------------------------------------------------------

class TestBusquedaEnTodos:
    def test_buscar_cabm_exacto_en_todos(self, df_bienes):
        """'5010' coincide exactamente con el valor de la columna CABM."""
        app = _mock_app_busqueda(df_bienes, criterio="5010", campo="Todos", filtro="TODOS")
        BuscadorBienes.buscar(app)
        resultado = _df_resultado(app)
        assert len(resultado) == 2

    def test_buscar_estado_exacto_en_todos(self, df_bienes):
        """'MALO' coincide exactamente con el valor de la columna ESTADO DEL BIEN."""
        app = _mock_app_busqueda(df_bienes, criterio="MALO", campo="Todos", filtro="TODOS")
        BuscadorBienes.buscar(app)
        resultado = _df_resultado(app)
        assert len(resultado) == 1
        assert resultado["ESTADO DEL BIEN"].values[0] == "MALO"

    def test_buscar_numero_inventario_en_todos(self, df_bienes):
        """El número de inventario '1001' coincide exactamente."""
        app = _mock_app_busqueda(df_bienes, criterio="1001", campo="Todos", filtro="TODOS")
        BuscadorBienes.buscar(app)
        resultado = _df_resultado(app)
        assert len(resultado) == 1


# ---------------------------------------------------------------------------
# Normalización del criterio
# ---------------------------------------------------------------------------

class TestNormalizacionCriterio:
    def test_criterio_en_minusculas_se_normaliza(self, df_bienes):
        """'bueno' se convierte a 'BUENO' antes de buscar."""
        app = _mock_app_busqueda(
            df_bienes, criterio="bueno", campo="ESTADO DEL BIEN", filtro="TODOS"
        )
        BuscadorBienes.buscar(app)
        resultado = _df_resultado(app)
        assert len(resultado) > 0
        assert all(v == "BUENO" for v in resultado["ESTADO DEL BIEN"].values)

    def test_criterio_con_espacios_intermedios_se_elimina(self, df_bienes):
        """'LAP TOP' → 'LAPTOP' después de eliminar espacios."""
        app = _mock_app_busqueda(
            df_bienes, criterio="LAP TOP", campo="DESCRIPCIÓN DETALLE", filtro="TODOS"
        )
        BuscadorBienes.buscar(app)
        resultado = _df_resultado(app)
        assert len(resultado) == 1

    def test_criterio_con_espacios_al_inicio_y_fin(self, df_bienes):
        app = _mock_app_busqueda(
            df_bienes, criterio="  LAPTOP  ", campo="DESCRIPCIÓN DETALLE", filtro="TODOS"
        )
        BuscadorBienes.buscar(app)
        resultado = _df_resultado(app)
        assert len(resultado) == 1


# ---------------------------------------------------------------------------
# Sin resultados
# ---------------------------------------------------------------------------

class TestBusquedaSinResultados:
    def test_sin_resultados_llena_tabla_con_df_filtrado(self, df_bienes):
        """Si no hay coincidencias, llenar_tabla recibe el df completo, no uno vacío."""
        app = _mock_app_busqueda(
            df_bienes, criterio="TEXTO_INEXISTENTE_XYZ", filtro="TODOS"
        )
        BuscadorBienes.buscar(app)
        resultado = _df_resultado(app)
        assert len(resultado) == len(df_bienes)

    def test_sin_resultados_con_filtro_vigentes(self, df_bienes):
        app = _mock_app_busqueda(
            df_bienes, criterio="TEXTO_INEXISTENTE_XYZ", filtro="VIGENTES"
        )
        BuscadorBienes.buscar(app)
        resultado = _df_resultado(app)
        # Debe devolver los vigentes, no un DataFrame vacío
        assert len(resultado) == len(df_bienes[df_bienes["STATUS"] == 1])

    def test_sin_resultados_no_levanta_excepcion(self, df_bienes):
        app = _mock_app_busqueda(
            df_bienes, criterio="ZZZNADA", campo="DESCRIPCIÓN DETALLE", filtro="TODOS"
        )
        # No debe lanzar ninguna excepción
        BuscadorBienes.buscar(app)
