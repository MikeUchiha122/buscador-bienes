# 🗂️ Asset Manager

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/Platform-Windows-blue?style=for-the-badge">
</p>

> Aplicación de escritorio para la gestión integral de inventarios de activos empresariales.

## 📋 Descripción

**Asset Manager** es una solución de escritorio desarrollada en Python que permite administrar inventarios de activos mediante una interfaz gráfica moderna e intuitiva.

## ✨ Características

| Función | Descripción |
|---------|-------------|
| 🔍 **Búsqueda Avanzada** | Filtra por código, descripción, ubicación o estado |
| 📊 **Filtros Dinámicos** | Visualiza activos por estado: ACTIVOS, INACTIVOS, TODOS |
| ✏️ **Gestión Completa** | Ver detalle, editar campos y gestionar estados |
| 🌙 **Interfaz Oscura** | Diseño moderno con tema oscuro profesional |
| 📝 **Logging** | Registro completo de operaciones del sistema |

## 🛠️ Requisitos

- **Python**: 3.8 o superior
- **SO**: Windows 7/8/10/11
- **Dependencias**: `pandas`, `openpyxl`

## 🚀 Instalación

```bash
# Clonar repositorio
git clone https://github.com/MikeUchiha122/buscador-bienes.git

# Entrar al directorio
cd buscador-bienes

# Instalar dependencias
pip install pandas openpyxl
```

## 💻 Uso

```bash
python buscador_bienes.py
```

### Controles

| Acción | Descripción |
|--------|-------------|
| **Búsqueda** | Escribe para filtrar en tiempo real |
| **Filtros** | Botones para estados: ACTIVOS / INACTIVOS / TODOS |
| **Detalle** | Doble clic en fila para ver información completa |
| **Editar** | Selecciona fila y modifica campos |
| **Gestionar** | Botón para cambiar estado del activo |

## 📁 Estructura

```
buscador-bienes/
├── buscador_bienes.py         # Aplicación principal
├── crear_word.py              # Generador de documentos
├── crear_word2.py              # Generador de documentos v2
├── cruzar_bienes.py           # Utilidad de cruces
├── cruzar_inventario.py       # Utilidad de cruces
├── cruzar_por_inventario.py
├── BASE_BIENES_UNIDAD.xlsx    # Base de datos
├── bienes.log                 # Logs del sistema
└── README.md                  # Este archivo
```

## 🖥️ Vista Previa

```
┌─────────────────────────────────────────────────┐
│  🗂️ Asset Manager                    [─][□][×] │
├─────────────────────────────────────────────────┤
│  🔍 Buscar...                        [BUSCAR]  │
├─────────────────────────────────────────────────┤
│  [ACTIVOS] [INACTIVOS] [TODOS]                  │
├─────────────────────────────────────────────────┤
│  #  │ Código   │ Descripción    │ Ubicación   │
│─────┼──────────┼────────────────┼──────────────│
│  1  │ INV-001  │ Laptop Dell    │ Oficina A    │
│  2  │ INV-002  │ Escritorio    │ Oficina B    │
│  3  │ INV-003  │ Silla Ergonom. │ Bodega       │
├─────────────────────────────────────────────────┤
│  [EDITAR]  [VER DETALLE]  [GESTIONAR]           │
└─────────────────────────────────────────────────┘
```

## 🔧 Tecnologías

<div align="center">

| Tecnología | Propósito |
|------------|-----------|
| Python 3.8+ | Lenguaje principal |
| Tkinter | Interfaz gráfica |
| Pandas | Manipulación de datos |
| Excel | Almacenamiento |

</div>

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**. Consulta el archivo `LICENSE` para más información.

---

<div align="center">

**Desarrollado por** Miguel Ángel Ramírez Galicia

⭐️ ¡Dale una estrella si te fue útil!

</div>
