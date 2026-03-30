# 📖 Guía Completa - Asset Manager

> Guía de uso y documentación técnica

---

## 📋 Índice

1. [Introducción](#1-introducción)
2. [Características](#2-características)
3. [Requisitos del Sistema](#3-requisitos-del-sistema)
4. [Instalación](#4-instalación)
5. [Guía de Uso](#5-guía-de-uso)
6. [Estructura del Proyecto](#6-estructura-del-proyecto)
7. [Tecnologías Utilizadas](#7-tecnologías-utilizadas)
8. [Glosario](#8-glosario)
9. [Créditos](#9-créditos)

---

## 1. Introducción

**Asset Manager** es una aplicación de escritorio para la gestión integral de inventarios de activos empresariales.

### ¿Qué hace?

- ✅ Busca activos por código, descripción, ubicación o estado
- ✅ Filtra por estado: ACTIVOS, INACTIVOS, TODOS
- ✅ Ver detalle de cada activo
- ✅ Editar información
- ✅ Gestionar estados (dar de baja)
- ✅ Cruzar datos con otros archivos Excel

---

## 2. Características

| Función | Descripción |
|---------|-------------|
| 🔍 Búsqueda Avanzada | Filtra en tiempo real por múltiples campos |
| 📊 Filtros Dinámicos | Ver activos por estado |
| ✏️ Gestión Completa | Editar y actualizar información |
| 🌙 Interfaz Oscura | Diseño moderno y profesional |
| 📝 Logging | Registro de todas las operaciones |
| 📥 Importación | Cruzar datos con archivos Excel |

---

## 3. Requisitos del Sistema

### Versión Portable (Recomendada)
- Windows 7/8/10/11
- No requiere Python
- No requiere permisos de administrador

### Versión Código Fuente
- Python 3.8+
- Windows 7/8/10/11
- Dependencias: `pandas`, `openpyxl`

---

## 4. Instalación

### Versión Portable

1. Descarga `AssetManager-v1.0.zip` desde [Releases](https://github.com/MikeUchiha122/buscador-bienes/releases)
2. Extrae la carpeta
3. Ejecuta `AssetManager.exe`

### Versión Código Fuente

```bash
git clone https://github.com/MikeUchiha122/buscador-bienes.git
cd buscador-bienes
pip install pandas openpyxl
python buscador_bienes.py
```

---

## 5. Guía de Uso

### 5.1 Interfaz Principal

![Interfaz Principal](assets/screenshot-main.png)

La interfaz se divide en:

| Sección | Descripción |
|---------|-------------|
| **Header** | Título y subtítulo de la aplicación |
| **Barra de búsqueda** | Campo para buscar y botón de acción |
| **Filtros** | Selector de estado (ACTIVOS/INACTIVOS/TODOS) |
| **Tabla de resultados** | Lista de activos encontrados |
| **Botones de acción** | Editar, ver detalle, gestionar |

### 5.2 Buscar un Activo

1. Escribe en el campo de búsqueda
2. Selecciona el campo donde buscar:
   - Todos
   - Número de Inventario
   - Descripción
   - Ubicación
   - Estado
3. Selecciona el filtro de estado
4. Presiona ENTER o haz clic en "Buscar"

### 5.3 Ver Detalle

1. Haz **doble clic** en cualquier fila
2. Se abre una ventana con información completa
3. Puedes editar campos disponibles
4. Guarda los cambios o Cancela

### 5.4 Dar de Baja

1. Selecciona el activo en la tabla
2. Haz doble clic para abrir el detalle
3. Haz clic en "DAR DE BAJA"
4. Confirma la acción

> **Nota:** La baja es lógica (STATUS=0), los datos se conservan.

### 5.5 Cruzar Archivos

1. Coloca el archivo Excel en: `archivo_cruzar/ARCHIVO_NUEVO.xlsx`
2. Presiona uno de los botones:
   - **x Inventario** - Cruza solo por número
   - **x Inv+CABM** - Cruza por número + código CABM
3. Se genera un informe automático

---

## 6. Estructura del Proyecto

```
buscador-bienes/
├── 📁 docs/                  # Documentación
│   └── GUIA.md              # Esta guía
├── 📁 dist/                  # Versión portable
│   ├── AssetManager.exe
│   └── BASE_BIENES_UNIDAD.xlsx
├── 🔍 buscador_bienes.py     # Aplicación principal
├── 📊 BASE_BIENES_UNIDAD.xlsx
├── 📝 bienes.log            # Logs
└── 📖 README.md            # README principal
```

---

## 7. Tecnologías Utilizadas

| Tecnología | Propósito |
|------------|-----------|
| Python 3.8+ | Lenguaje de programación |
| Tkinter | Interfaz gráfica |
| Pandas | Manipulación de datos |
| Excel (.xlsx) | Almacenamiento de datos |
| PyInstaller | Compilación portable |

---

## 8. Glosario

| Término | Significado |
|---------|-------------|
| **DataFrame** | Tabla de datos en memoria |
| **Activo** | Bien que está en uso |
| **Inactivo** | Bien dado de baja |
| **STATUS** | Campo que indica estado (1=activo, 0=inactivo) |
| **Inventario** | Número único de identificación |
| **CABM** | Código adicional de identificación |
| **Cruce** | Comparar dos archivos |

---

## 9. Créditos

| Campo | Información |
|-------|-------------|
| **Desarrollador** | Ing. Miguel Ángel Ramírez Galicia |
| **Licencia** | MIT |
| **Versión** | 1.0.0 |

---

<div align="center">

⭐️ ¡Gracias por usar Asset Manager!

</div>
