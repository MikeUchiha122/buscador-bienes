# Buscador de Bienes SICOBIM

Aplicación de escritorio desarrollada en Python para la gestión integral del inventario de bienes muebles del ISSSTE México.

## Descripción

Sistema de gestión de inventario que permite administrar bienes muebles mediante una interfaz gráfica intuitiva, con capacidades de búsqueda avanzada, filtrado por estado y registro de operaciones.

## Características

| Característica | Descripción |
|----------------|-------------|
| **Búsqueda multidimensional** | Busca por número de inventario, descripción, ubicación o estado |
| **Filtros dinámicos** | Filtra por VIGENTES, BAJAS o TODOS los bienes |
| **Gestión de bienes** | Visualización de detalle, edición de campos y bajas lógicas |
| **Interfaz moderna** | Diseño oscuro con temática de ciberseguridad |
| **Logging completo** | Registro de todas las operaciones en archivo.log |

## Requisitos del Sistema

- Python 3.8 o superior
- Windows 7/8/10/11
- Dependencias: `pandas`, `openpyxl`

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/MikeUchiha122/buscador-bienes.git

# Navegar al directorio
cd buscador-bienes

# Instalar dependencias
pip install pandas openpyxl
```

## Uso

```bash
python buscador_bienes.py
```

### Guía de操作es

- **Búsqueda**: Escribe en el campo de texto para filtrar resultados en tiempo real
- **Filtros**: Usa los botones para mostrar bienes VIGENTES, BAJAS o TODOS
- **Detalle**: Doble clic en cualquier fila para ver información completa
- **Edición**: Selecciona una fila y modifica los campos deseados
- **Baja**: Selecciona un bien y haz clic en "DAR DE BAJA" para desactivar (STATUS=0)

## Estructura del Proyecto

```
buscador-bienes/
├── buscador_bienes.py      # Aplicación principal (GUI Tkinter)
├── crear_word.py           # Generador de documentos Word
├── crear_word2.py          # Generador de documentos (v2)
├── cruzar_bienes.py        # Utilidad de cruces de inventario
├── cruzar_inventario.py    # Utilidad de cruces
├── cruzar_por_inventario.py
├── BASE_BIENES_UNIDAD.xlsx # Base de datos de bienes
├── bienes.log              # Archivo de logs
└── README.md              # Este archivo
```

## Tecnologías Utilizadas

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-FF5722?style=flat&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data-150458?style=flat&logo=pandas)
![Excel](https://img.shields.io/badge/Excel-Storage-217346?style=flat&logo=microsoft-excel)

</div>

## Capturas de Pantalla

La aplicación cuenta con:
- Interfaz oscura con colores profesional
- Tabla de resultados con scroll
- Panel de búsqueda y filtros
- Botones de acción para gestión de bienes

## Licencia

MIT License - Ver archivo LICENSE para más detalles.

---

**Desarrollado por**: Ing. Miguel Ángel Ramírez Galicia  
**Organización**: ISSSTE México  
**Versión**: 1.0.0

¿Dudas o sugerencias? Abre un issue en el repositorio.
