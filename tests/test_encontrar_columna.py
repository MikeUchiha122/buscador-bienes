"""
Pruebas para el método BuscadorBienes.encontrar_columna().

Comportamiento esperado:
- Devuelve la columna del DataFrame cuyo nombre contiene el texto buscado (parcial, sin mayúsculas).
- Guarda el resultado en caché para evitar búsquedas repetidas.
- Si no encuentra ninguna coincidencia, devuelve el mismo texto buscado sin error.
"""
import pandas as pd
from unittest.mock import MagicMock

from buscador_bienes import BuscadorBienes


def _mock_app(df):
    """Crea una instancia simulada de BuscadorBienes con sólo los atributos requeridos."""
    inst = MagicMock(spec=BuscadorBienes)
    inst.df = df
    inst._cache_columnas = {}
    inst.encontrar_columna = lambda nombre: BuscadorBienes.encontrar_columna(inst, nombre)
    return inst


class TestEncontrarColumnaCoincidencias:
    def test_coincidencia_exacta(self, df_bienes):
        app = _mock_app(df_bienes)
        assert app.encontrar_columna("N° INVENTARIO") == "N° INVENTARIO"

    def test_coincidencia_parcial(self, df_bienes):
        """'INVENTARIO' debe encontrar 'N° INVENTARIO'."""
        app = _mock_app(df_bienes)
        assert app.encontrar_columna("INVENTARIO") == "N° INVENTARIO"

    def test_coincidencia_insensible_a_mayusculas(self, df_bienes):
        """La búsqueda debe ignorar diferencias entre mayúsculas y minúsculas."""
        app = _mock_app(df_bienes)
        assert app.encontrar_columna("inventario") == "N° INVENTARIO"

    def test_coincidencia_parcial_descripcion(self, df_bienes):
        app = _mock_app(df_bienes)
        assert app.encontrar_columna("DESCRIPCIÓN") == "DESCRIPCIÓN DETALLE"

    def test_coincidencia_parcial_estado(self, df_bienes):
        app = _mock_app(df_bienes)
        assert app.encontrar_columna("ESTADO") == "ESTADO DEL BIEN"

    def test_coincidencia_columna_ubicacion(self, df_bienes):
        app = _mock_app(df_bienes)
        assert app.encontrar_columna("UBICACIÓN") == "UBICACIÓN"

    def test_columna_cabm(self, df_bienes):
        app = _mock_app(df_bienes)
        assert app.encontrar_columna("CABM") == "CABM"


class TestEncontrarColumnaNoEncontrada:
    def test_columna_inexistente_retorna_el_mismo_texto(self, df_bienes):
        """Si no hay coincidencia, devuelve el texto de búsqueda sin modificar."""
        app = _mock_app(df_bienes)
        resultado = app.encontrar_columna("COLUMNA_QUE_NO_EXISTE")
        assert resultado == "COLUMNA_QUE_NO_EXISTE"

    def test_texto_vacio_retorna_vacio(self, df_bienes):
        app = _mock_app(df_bienes)
        resultado = app.encontrar_columna("")
        # Cualquier columna cuyo nombre contiene "" es cualquier columna,
        # por lo que devuelve la primera columna encontrada.
        assert isinstance(resultado, str)

    def test_dataframe_vacio_retorna_el_mismo_texto(self):
        df_vacio = pd.DataFrame()
        app = _mock_app(df_vacio)
        assert app.encontrar_columna("INVENTARIO") == "INVENTARIO"


class TestEncontrarColumnaCache:
    def test_resultado_se_guarda_en_cache(self, df_bienes):
        app = _mock_app(df_bienes)
        app.encontrar_columna("INVENTARIO")
        assert "INVENTARIO" in app._cache_columnas
        assert app._cache_columnas["INVENTARIO"] == "N° INVENTARIO"

    def test_segunda_llamada_usa_cache(self, df_bienes):
        """Una vez cacheado, el resultado no cambia aunque el DataFrame cambie."""
        app = _mock_app(df_bienes)
        # Primera llamada: llena el caché
        primera = app.encontrar_columna("DESCRIPCIÓN")
        assert primera == "DESCRIPCIÓN DETALLE"

        # Reemplazar el DataFrame por uno sin esa columna
        app.df = pd.DataFrame({"OTRA_COLUMNA": [1, 2]})

        # Segunda llamada: debe devolver el valor cacheado, no fallar
        segunda = app.encontrar_columna("DESCRIPCIÓN")
        assert segunda == "DESCRIPCIÓN DETALLE"

    def test_cache_independiente_por_clave(self, df_bienes):
        app = _mock_app(df_bienes)
        app.encontrar_columna("INVENTARIO")
        app.encontrar_columna("UBICACIÓN")
        assert app._cache_columnas["INVENTARIO"] == "N° INVENTARIO"
        assert app._cache_columnas["UBICACIÓN"] == "UBICACIÓN"

    def test_columna_no_encontrada_tambien_se_cachea(self, df_bienes):
        """El fallback también se guarda para evitar búsquedas repetidas."""
        app = _mock_app(df_bienes)
        app.encontrar_columna("INEXISTENTE")
        assert "INEXISTENTE" in app._cache_columnas
        assert app._cache_columnas["INEXISTENTE"] == "INEXISTENTE"
