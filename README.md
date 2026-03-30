# 🗂️ Asset Manager

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/Platform-Windows-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Portable-Yes-green?style=for-the-badge">
</p>

> Aplicación de escritorio para la gestión integral de inventarios de activos empresariales.

## ✨ Características

| Función | Descripción |
|---------|-------------|
| 🔍 **Búsqueda Avanzada** | Filtra por código, descripción, ubicación o estado |
| 📊 **Filtros Dinámicos** | Visualiza activos por estado: ACTIVOS, INACTIVOS, TODOS |
| ✏️ **Gestión Completa** | Ver detalle, editar campos y gestionar estados |
| 🌙 **Interfaz Oscura** | Diseño moderno con tema oscuro profesional |
| 📝 **Logging** | Registro completo de operaciones del sistema |
| 🔐 **Sin Admin** | No requiere permisos de administrador |

## ⬇️ Descarga

### 🎯 Versión Portable (Recomendada)

**No requiere Python ni instalación.**

1. Ve a [Releases](https://github.com/MikeUchiha122/buscador-bienes/releases)
2. Descarga `AssetManager.zip`
3. Extrae y ejecuta `AssetManager.exe`

### 💻 Versión Código Fuente

```bash
# Clonar repositorio
git clone https://github.com/MikeUchiha122/buscador-bienes.git

# Entrar al directorio
cd buscador-bienes

# Instalar dependencias
pip install pandas openpyxl

# Ejecutar
python buscador_bienes.py
```

## 🚀 Uso

Simplemente ejecuta `AssetManager.exe`. No necesita:
- Python instalado
- Permisos de administrador
- Instalación

Todo se ejecuta en la carpeta donde copies la aplicación.

### Controles

| Acción | Descripción |
|--------|-------------|
| **Búsqueda** | Escribe para filtrar en tiempo real |
| **Filtros** | Botones para estados: ACTIVOS / INACTIVOS / TODOS |
| **Detalle** | Doble clic en fila para ver información completa |
| **Editar** | Selecciona fila y modifica campos |
| **Gestionar** | Botón para cambiar estado del activo |

## 📁 Estructura Portable

```
AssetManager/
├── AssetManager.exe           # Ejecutable principal
├── BASE_BIENES_UNIDAD.xlsx   # Base de datos
└── bienes.log               # Logs (se crea al usar)
```

## 🖥️ Vista Previa

```
┌─────────────────────────────────────────────────┐
│  🗂️ Asset Manager                    [─][□][×] │
├─────────────────────────────────────────────────┤
│  🔍 Buscar...                        [BUSCAR]   │
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
| Python | Lenguaje principal |
| Tkinter | Interfaz gráfica |
| Pandas | Manipulación de datos |
| Excel | Almacenamiento |
| PyInstaller | Compilación portable |

</div>

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**.

---

<div align="center">

**Desarrollado por** Miguel Ángel Ramírez Galicia

⭐️ ¡Dale una estrella si te fue útil!

</div>
