"""
Autor: Mauricio J. Avalo Tamayo
Carrera: 3ro de Ciencias de la Computacón
Info: Gestor de tareas ToDoList
"""
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import json
import asyncio
import threading

ARCHIVO_TAREAS = "tareas.json"

def crear_tarea(titulo, descripcion, categoria, carpeta, fecha_vencimiento, recordatorio):
    return {
        "id": datetime.now().timestamp(),
        "titulo": titulo,
        "descripcion": descripcion,
        "categoria": categoria,
        "carpeta": carpeta,
        "fecha_creacion": datetime.now().isoformat(),
        "fecha_vencimiento": fecha_vencimiento,
        "completada": False,
        "recordatorio": recordatorio,
    }

def guardar_tareas(tareas):
    with open(ARCHIVO_TAREAS, "w") as archivo:
        json.dump(tareas, archivo, indent=4)

def cargar_tareas():
    try:
        with open(ARCHIVO_TAREAS, "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []

class ToDoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Tareas Moderno")
        self.geometry("800x500")
        self.centrar_ventana(800, 500)
        self.tareas = cargar_tareas()
        self.tareas_filtradas = self.tareas

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.frame_izquierdo = ctk.CTkFrame(self, width=400)
        self.frame_izquierdo.pack(side="left", fill="both", expand=True)

        self.frame_derecho = ctk.CTkFrame(self, width=400)
        self.frame_derecho.pack(side="right", fill="both", expand=True)

        self.scrollable_frame = ctk.CTkScrollableFrame(self.frame_izquierdo, width=400, height=400)
        self.scrollable_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.btn_crear = ctk.CTkButton(self.frame_derecho, text="Crear Tarea", command=self.crear_tarea)
        self.btn_crear.pack(pady=10, padx=20)

        self.btn_guardar = ctk.CTkButton(self.frame_derecho, text="Guardar Tareas", command=self.guardar_tareas)
        self.btn_guardar.pack(pady=10, padx=20)

        self.btn_filtro_completadas = ctk.CTkButton(
            self.frame_derecho, text="Filtrar Completadas", command=lambda: self.filtrar_tareas(lambda t: t["completada"])
        )
        self.btn_filtro_completadas.pack(pady=10, padx=20)

        self.btn_filtro_pendientes = ctk.CTkButton(
            self.frame_derecho, text="Filtrar Pendientes", command=lambda: self.filtrar_tareas(lambda t: not t["completada"])
        )
        self.btn_filtro_pendientes.pack(pady=10, padx=20)
        self.btn_filtro_vencidas = ctk.CTkButton(
            self.frame_derecho, text="Filtrar Vencidas", command=lambda: self.filtrar_tareas(self.es_tarea_vencida)
        )
        self.btn_filtro_vencidas.pack(pady=10, padx=20)
        

        self.btn_mostrar_todas = ctk.CTkButton(
            self.frame_derecho, text="Mostrar Todas", command=self.mostrar_todas
        )
        self.btn_mostrar_todas.pack(pady=10, padx=20)

        self.btn_salir = ctk.CTkButton(self.frame_derecho, text="Salir", command=self.quit)
        self.btn_salir.pack(pady=10, padx=20)

        self.mostrar_tareas()
        
        threading.Thread(target=self.iniciar_recordatorios, daemon=True).start()
    
    def centrar_ventana(self, ancho, alto):
        """Centrar la ventana en la pantalla."""
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")
    
    def centrar_ventana_secundaria(self, ventana, ancho, alto):
        """Centrar una ventana secundaria en la pantalla."""
        pantalla_ancho = ventana.winfo_screenwidth()
        pantalla_alto = ventana.winfo_screenheight()
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
         
    def iniciar_recordatorios(self):
        asyncio.run(self.verificar_recordatorios())

    async def verificar_recordatorios(self):
        while True:
            ahora = datetime.now()
            for tarea in self.tareas:
                if not tarea["completada"]:
                    fecha_vencimiento = datetime.fromisoformat(tarea["fecha_vencimiento"])
                    tiempo_restante = (fecha_vencimiento - ahora).total_seconds() / 60
                    if 0 < tiempo_restante <= tarea["recordatorio"]:
                        messagebox.showwarning(
                            "🔔 Recordatorio de Tarea",
                            f"La tarea '{tarea['titulo']}' está próxima a vencer!",
                        )
            await asyncio.sleep(60)
    
    def mostrar_tareas(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for tarea in self.tareas_filtradas:
            tarea_frame = ctk.CTkFrame(self.scrollable_frame)
            tarea_frame.pack(fill="x", pady=5, padx=10)

            tarea_label = ctk.CTkLabel(
                tarea_frame,
                text=f"{tarea['titulo']} - {tarea['categoria']} - Vence: {tarea['fecha_vencimiento']}",
                anchor="w",
            )
            tarea_label.pack(side="left", fill="x", expand=True, padx=10)

            completar_btn = ctk.CTkButton(
                tarea_frame,
                text="Completar",
                width=80,
                command=lambda t=tarea: self.marcar_completada(t),
            )
            completar_btn.pack(side="right", padx=10)

            eliminar_btn = ctk.CTkButton(
                tarea_frame,
                text="Eliminar",
                width=80,
                command=lambda t=tarea: self.eliminar_tarea(t),
            )
            eliminar_btn.pack(side="right", padx=10)
            
            editar_btn = ctk.CTkButton(
                tarea_frame,
                text="Editar",
                width=80,
                command=lambda t=tarea: self.editar_tarea(t),
            )
            editar_btn.pack(side="right", padx=10)

    def crear_tarea(self):
        ventana_crear = ctk.CTkToplevel(self)
        ventana_crear.title("Crear Tarea")
        ventana_crear.geometry("400x400")
        self.centrar_ventana_secundaria(ventana_crear, 400, 400)

        titulo = ctk.CTkEntry(ventana_crear, placeholder_text="Título")
        titulo.pack(pady=10, padx=20)

        descripcion = ctk.CTkEntry(ventana_crear, placeholder_text="Descripción")
        descripcion.pack(pady=10, padx=20)

        categoria = ctk.CTkEntry(ventana_crear, placeholder_text="Categoría")
        categoria.pack(pady=10, padx=20)

        carpeta = ctk.CTkEntry(ventana_crear, placeholder_text="Carpeta")
        carpeta.pack(pady=10, padx=20)

        fecha_vencimiento = ctk.CTkEntry(ventana_crear, placeholder_text="Fecha de vencimiento (YYYY-MM-DD HH:MM)")
        fecha_vencimiento.pack(pady=10, padx=20)

        recordatorio = ctk.CTkEntry(ventana_crear, placeholder_text="Recordatorio (minutos antes)")
        recordatorio.pack(pady=10, padx=20)

        def guardar_nueva_tarea():
            nueva_tarea = crear_tarea(
                titulo.get(),
                descripcion.get(),
                categoria.get(),
                carpeta.get(),
                fecha_vencimiento.get(),
                int(recordatorio.get()),
            )
            self.tareas.append(nueva_tarea)
            self.tareas_filtradas = self.tareas
            self.mostrar_tareas()
            ventana_crear.destroy()

        btn_guardar = ctk.CTkButton(ventana_crear, text="Guardar", command=guardar_nueva_tarea)
        btn_guardar.pack(pady=20)

    def editar_tarea(self, tarea):
        ventana_editar = ctk.CTkToplevel(self)
        ventana_editar.title("Editar Tarea")
        ventana_editar.geometry("400x400")
        self.centrar_ventana_secundaria(ventana_editar, 400, 400)

        titulo = ctk.CTkEntry(ventana_editar, placeholder_text="Título")
        titulo.insert(0, tarea["titulo"])
        titulo.pack(pady=10, padx=20)

        descripcion = ctk.CTkEntry(ventana_editar, placeholder_text="Descripción")
        descripcion.insert(0, tarea["descripcion"])
        descripcion.pack(pady=10, padx=20)

        categoria = ctk.CTkEntry(ventana_editar, placeholder_text="Categoría")
        categoria.insert(0, tarea["categoria"])
        categoria.pack(pady=10, padx=20)

        carpeta = ctk.CTkEntry(ventana_editar, placeholder_text="Carpeta")
        carpeta.insert(0, tarea["carpeta"])
        carpeta.pack(pady=10, padx=20)

        fecha_vencimiento = ctk.CTkEntry(ventana_editar, placeholder_text="Fecha de vencimiento (YYYY-MM-DD HH:MM)")
        fecha_vencimiento.insert(0, tarea["fecha_vencimiento"])
        fecha_vencimiento.pack(pady=10, padx=20)

        recordatorio = ctk.CTkEntry(ventana_editar, placeholder_text="Recordatorio (minutos antes)")
        recordatorio.insert(0, str(tarea["recordatorio"]))
        recordatorio.pack(pady=10, padx=20)

        def guardar_cambios():
            tarea["titulo"] = titulo.get()
            tarea["descripcion"] = descripcion.get()
            tarea["categoria"] = categoria.get()
            tarea["carpeta"] = carpeta.get()
            tarea["fecha_vencimiento"] = fecha_vencimiento.get()
            tarea["recordatorio"] = int(recordatorio.get())
            self.mostrar_tareas()
            ventana_editar.destroy()

        btn_guardar = ctk.CTkButton(ventana_editar, text="Guardar Cambios", command=guardar_cambios)
        btn_guardar.pack(pady=20)
    
    def eliminar_tarea(self, tarea):
        self.tareas = [t for t in self.tareas if t["id"] != tarea["id"]]
        self.tareas_filtradas = self.tareas
        self.mostrar_tareas()

    def guardar_tareas(self):
        guardar_tareas(self.tareas)
        messagebox.showinfo("Guardar Tareas", "Tareas guardadas correctamente.")

    def es_tarea_vencida(self, tarea):
        ahora = datetime.now()
        fecha_vencimiento = datetime.fromisoformat(tarea["fecha_vencimiento"])
        return fecha_vencimiento < ahora and not tarea["completada"]

    def filtrar_tareas(self, criterio):
        self.tareas_filtradas = list(filter(criterio, self.tareas))
        self.mostrar_tareas()

    def mostrar_todas(self):
        self.tareas_filtradas = self.tareas
        self.mostrar_tareas()

    def marcar_completada(self, tarea):
        for t in self.tareas:
            if t["id"] == tarea["id"]:
                t["completada"] = True
        self.mostrar_tareas()

if __name__ == "__main__":
    app = ToDoApp()
    app.mainloop()