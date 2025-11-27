import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Usamos customtkinter para una apariencia moderna
import customtkinter as ctk

# Librerías de imagen del código original
from PIL import Image, ImageTk, ImageFilter, ImageOps

# Configuracion de customtkinter
ctk.set_appearance_mode("System")  # Modos: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")


class FotoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Variables de la App
        self.imagen_original_pil = None  # Objeto PIL de la imagen original cargada
        self.imagen_filtrada_pil = None  # Objeto PIL de la última imagen filtrada
        self.imagen_mostrada_tk = None  # Objeto Tkinter para mostrar en la GUI

        # Configuración de la Ventana
        self.title("FotoApp - Editor de Imagenes")
        self.geometry("1000x700")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Marco Lateral (Controles)
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        ctk.CTkLabel(self.sidebar_frame, text="Controles", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0,
                                                                                                          column=0,
                                                                                                          padx=20,
                                                                                                          pady=(20, 10))

        # Botones de Acción
        ctk.CTkButton(self.sidebar_frame, text="1. Cargar Imagen", command=self.cargar_imagen_gui).grid(row=1, column=0,
                                                                                                        padx=20,
                                                                                                        pady=10)
        ctk.CTkButton(self.sidebar_frame, text="2. Guardar Imagen", command=self.guardar_imagen).grid(row=2, column=0,
                                                                                                      padx=20, pady=10)
        ctk.CTkButton(self.sidebar_frame, text="3. Salir", command=self.quit).grid(row=3, column=0, padx=20, pady=10)

        # Marco Principal (Imagen y Filtros)
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Contenedor de la Imagen
        self.image_container = ctk.CTkFrame(self.main_frame)
        self.image_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.image_container.grid_columnconfigure(0, weight=1)
        self.image_container.grid_rowconfigure(0, weight=1)

        self.image_label = ctk.CTkLabel(self.image_container, text="Cargue una imagen para empezar.")
        self.image_label.grid(row=0, column=0, sticky="nsew")

        # Controles de Filtros
        self.filter_frame = ctk.CTkFrame(self.main_frame)
        self.filter_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))

        self.agregar_botones_filtros(self.filter_frame)

    # Metodos de Manejo de la GUI y Imagenes

    def agregar_botones_filtros(self, parent_frame):

        filtros = {   #Crea y posiciona los botones de filtro
            "Original": "ORIGINAL",
            "Contraste": "CONTRASTE",
            "Boceto": "BOCETO",
            "Difuminado": "BLUR",
            "Realce": "SHARPEN",
            "Relieve": "EMBOSS",
            "Contorno": "CONTOUR",
            "Suavizar": "SMOOTH"
        }

        # Distribuye los botones en una fila
        for i, (nombre, filtro_key) in enumerate(filtros.items()):
            parent_frame.grid_columnconfigure(i, weight=1)
            ctk.CTkButton(parent_frame, text=nombre, command=lambda f=filtro_key: self.aplicar_filtro_gui(f)).grid(
                row=0, column=i, padx=5, pady=10)

    def cargar_imagen_gui(self):
        #Abre un cuadro de dialogo para seleccionar la imagen.
        ruta_imagen = filedialog.askopenfilename(
            title="Seleccionar Imagen",
            filetypes=[("Archivos de Imagen", "*.png;*.jpg;*.jpeg;*.webp")]
        )

        if ruta_imagen:
            try:
                # 1. Cargar el objeto PIL (similar a de la funcion cargar_imagen, sin el redimensionamiento)
                self.imagen_original_pil = Image.open(ruta_imagen)
                self.imagen_filtrada_pil = self.imagen_original_pil.copy()  # Inicializar con original

                # 2. Mostrar la imagen original
                self.mostrar_imagen(self.imagen_original_pil)

            except Exception as e:
                messagebox.showerror("Error de Carga", f"No se pudo cargar la imagen: {e}")

    def mostrar_imagen(self, img_pil):
        """Redimensiona la imagen para que encaje y la muestra en el Label."""

        # Obtener el tamaño del contenedor
        container_width = self.image_container.winfo_width()
        container_height = self.image_container.winfo_height()

        # Redimensionar la imagen manteniendo la proporción para que quepa en el contenedor
        img_width, img_height = img_pil.size
        ratio = min(container_width / img_width, container_height / img_height)
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)

        img_resized = img_pil.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Convertir el objeto PIL a un objeto compatible con Tkinter/CustomTkinter
        self.imagen_mostrada_tk = ImageTk.PhotoImage(img_resized)

        # Actualizar el Label
        self.image_label.configure(image=self.imagen_mostrada_tk, text="")
        self.image_label.image = self.imagen_mostrada_tk  # Importante para evitar que Python la borre

    def aplicar_filtro_gui(self, nombre_filtro): #Aplica el filtro y actualiza la vista.
        if self.imagen_original_pil is None:
            messagebox.showwarning("Advertencia", "Primero debes cargar una imagen.")
            return

        try:
            img = self.imagen_original_pil.copy()

            if nombre_filtro == "ORIGINAL":
                self.imagen_filtrada_pil = img

            elif nombre_filtro == "CONTRASTE":
                # Utiliza tu lógica de ecualización de contraste
                img_rgb = img.convert("RGB")
                self.imagen_filtrada_pil = ImageOps.equalize(img_rgb)

            elif nombre_filtro == "BOCETO":
                # Utiliza tu lógica de Modo Pintor
                img_gris = img.convert("L")
                img_bordes = img_gris.filter(ImageFilter.FIND_EDGES)
                self.imagen_filtrada_pil = ImageOps.invert(img_bordes)

            # Filtros de matriz de Pillow
            elif nombre_filtro in ["BLUR", "SHARPEN", "EMBOSS", "CONTOUR", "SMOOTH"]:
                filtro_obj = getattr(ImageFilter, nombre_filtro)
                self.imagen_filtrada_pil = img.filter(filtro_obj)

            # Muestra el resultado
            self.mostrar_imagen(self.imagen_filtrada_pil)

        except Exception as e:
            messagebox.showerror("Error de Filtro", f"Error al aplicar filtro {nombre_filtro}: {e}")

    def guardar_imagen(self):
        """Abre un cuadro de dialogo para guardar la imagen filtrada."""
        if self.imagen_filtrada_pil is None:
            messagebox.showwarning("Advertencia", "No hay imagen filtrada para guardar.")
            return

        ruta_guardado = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[
                ("JPEG", "*.jpg"),
                ("PNG", "*.png"),
                ("Bitmap", "*.bmp")
            ],
            title="Guardar Imagen Filtrada Como"
        )

        if ruta_guardado:
            try:
                self.imagen_filtrada_pil.save(ruta_guardado)
                messagebox.showinfo("Éxito", f"Imagen guardada en: {ruta_guardado}")
            except Exception as e:
                messagebox.showerror("Error de Guardado", f"No se pudo guardar la imagen: {e}")


if __name__ == "__main__":
    app = FotoApp()
    app.mainloop()