# Buscador de Bienes SICOBIM

Aplicacion de escritorio para gestionar el inventario de bienes muebles del ISSSTE Mexico.

## Caracteristicas

- Busqueda avanzada por inventario, descripcion, ubicacion o estado
- Filtros dinamicos: VIGENTES, BAJAS, TODOS
- Gestion completa: ver detalle, editar campos y dar de baja bienes
- Interfaz oscura con tema moderno
- Logging de operaciones
- No requiere permisos de administrador

## Descarga

### Version Portable (Recomendada)

1. Ve a Releases: https://github.com/MikeUchiha122/buscador-bienes/releases
2. Descarga BuscadorBienes-SICOBIM.zip
3. Extrae y ejecuta BuscadorBienes.exe

### Version Codigo Fuente

git clone https://github.com/MikeUchiha122/buscador-bienes.git
cd buscador-bienes
pip install pandas openpyxl
python buscador_bienes.py

## Uso

Simplemente ejecuta BuscadorBienes.exe. No necesita:
- Python instalado
- Permisos de administrador
- Instalacion

## Estructura Portable

BuscadorBienes-SICOBIM/
- BuscadorBienes.exe
- BASE_BIENES_UNIDAD.xlsx
- bienes.log (se crea al usar)

## Tecnologias

- Python + Tkinter + Pandas + Excel + PyInstaller

## Licencia

MIT

---

Desarrollado por Miguel Angel Ramirez Galicia