------------
![](https://github.com/elMauro2003/imagenes/blob/main/SRCM-image.jpg)

# Gestor de Tareas ToDoList

Este proyecto es un gestor de tareas moderno desarrollado en Python con una interfaz gráfica basada en `customtkinter`. Permite crear, editar, eliminar y gestionar tareas con recordatorios y filtros.

---

## Requisitos Previos

- **Python**: Versión 3.7 o superior instalada en tu sistema.
- **Pip**: Administrador de paquetes de Python (incluido con Python).
- **Conexión a Internet**: Para instalar las dependencias necesarias.

---

## Configuración del Entorno

### 1. Crear un Entorno Virtual
1. Abre una terminal o línea de comandos.
2. Navega al directorio donde se encuentra el archivo `appVisual.py`.
3. Ejecuta el siguiente comando para crear un entorno virtual:
```
python -m venv env
```

### 2. Ejecutar el Entorno Virtual
Linux Run env
```
source env/bin/activate
```

Windows Run env
```
env\Scripts\activate
```

## 3. Instalar los requirements del proyecto

>Run next comand 
```
pip install -r requirements.txt
```

## Uso del Software

### 1. Ejecutar la Aplicación
1. Asegúrate de que el entorno virtual esté activado.
2. Ejecuta el archivo principal:
```
python appVisual.py
```

### 2. Funcionalidades Principales

- **Crear Tarea:**
    Haz clic en el botón Crear Tarea.
    Completa los campos requeridos: título, descripción, categoría, carpeta, fecha de vencimiento y recordatorio.
    Haz clic en Guardar para añadir la tarea.

- **Editar Tarea:**
    Haz clic en el botón Editar junto a la tarea que deseas modificar.
    Cambia los datos en los campos y haz clic en Guardar Cambios.

- **Eliminar Tarea:**
    Haz clic en el botón Eliminar junto a la tarea que deseas borrar.

- **Filtrar Tareas:**
    Usa los botones de filtro en el panel derecho para mostrar tareas completadas, pendientes o vencidas.

- **Guardar Tareas:**
    Haz clic en el botón Guardar Tareas para guardar todas las tareas en el archivo tareas.json.
- **Salir:**
    Haz clic en el botón Salir para cerrar la aplicación.

