import os
from PIL import Image, ImageFilter, ImageOps
import matplotlib.pyplot as plt

imagen_actual = None

def cargar_imagen(ruta_imagen, plataforma):
    """
    Carga y redimensiona imagen segun red social.
    Mantiene proporcion sin distorsionar.
    """
    global imagen_actual
    
    dimensiones = {
        "Youtube": (1280, 720),
        "Instagram": (1080, 1080),
        "Twitter": (1024, 512),
        "Facebook": (1200, 630)
    }
    
    if plataforma not in dimensiones:
        print(f"Error: Plataforma '{plataforma}' no reconocida.")
        return None
    
    if not os.path.exists(ruta_imagen):
        print("Error: Archivo no encontrado.")
        return None
    
    try:
        img = Image.open(ruta_imagen)
        target_size = dimensiones[plataforma]
        img.thumbnail(target_size, Image.Resampling.LANCZOS)
        
        fondo = Image.new('RGB', target_size, 'white')
        offset = ((target_size[0] - img.width) // 2, (target_size[1] - img.height) // 2)
        fondo.paste(img, offset)
        
        imagen_actual = fondo
        print(f"Imagen cargada para {plataforma}: {fondo.size}")
        return fondo
    except Exception as e:
        print(f"Error al abrir imagen: {e}")
        return None


def ajustar_contraste(imagen):
    """
    Aplica ecualizacion de histograma para mejorar contraste.
    """
    if imagen is None:
        print("Error: Primero carga una imagen.")
        return None
    
    img_rgb = imagen.convert("RGB")
    img_ecualizada = ImageOps.equalize(img_rgb)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].imshow(img_rgb)
    axes[0].set_title("Original")
    axes[0].axis("off")
    
    axes[1].imshow(img_ecualizada)
    axes[1].set_title("Contraste Ecualizado")
    axes[1].axis("off")
    
    plt.tight_layout()
    plt.savefig("comparacion_contraste.png")
    plt.show()
    
    img_ecualizada.save("imagen_ecualizada.jpg")
    print("Guardado: comparacion_contraste.png e imagen_ecualizada.jpg")
    return img_ecualizada


def aplicar_filtro(imagen, nombre_filtro):
    """
    Aplica uno de los 9 filtros de Pillow.
    """
    if imagen is None:
        print("Error: Primero carga una imagen.")
        return None
    
    filtros = {
        "BLUR": ImageFilter.BLUR,
        "CONTOUR": ImageFilter.CONTOUR,
        "DETAIL": ImageFilter.DETAIL,
        "EDGE_ENHANCE": ImageFilter.EDGE_ENHANCE,
        "EDGE_ENHANCE_MORE": ImageFilter.EDGE_ENHANCE_MORE,
        "EMBOSS": ImageFilter.EMBOSS,
        "FIND_EDGES": ImageFilter.FIND_EDGES,
        "SHARPEN": ImageFilter.SHARPEN,
        "SMOOTH": ImageFilter.SMOOTH
    }
    
    if nombre_filtro not in filtros:
        print("Filtro no valido.")
        return None
    
    img_filtrada = imagen.filter(filtros[nombre_filtro])
    
    plt.figure()
    plt.imshow(img_filtrada)
    plt.title(f"Filtro: {nombre_filtro}", fontsize=14)
    plt.axis("off")
    plt.savefig(f"filtro_{nombre_filtro}.jpg")
    plt.show()
    
    print(f"Guardado: filtro_{nombre_filtro}.jpg")
    return img_filtrada


def mostrar_todos_filtros(imagen):
    """
    Muestra la imagen original y los 9 filtros en una sola figura.
    """
    if imagen is None:
        print("Error: Primero carga una imagen.")
        return None
    
    filtros = ["BLUR", "CONTOUR", "DETAIL", "EDGE_ENHANCE", 
               "EDGE_ENHANCE_MORE", "EMBOSS", "FIND_EDGES", 
               "SHARPEN", "SMOOTH"]
    
    fig, axes = plt.subplots(2, 5, figsize=(18, 8))
    axes = axes.flatten()
    
    axes[0].imshow(imagen)
    axes[0].set_title("ORIGINAL", fontsize=12, fontweight='bold')
    axes[0].axis("off")
    
    for i, nombre in enumerate(filtros, start=1):
        filtro_obj = getattr(ImageFilter, nombre)
        img_filtrada = imagen.filter(filtro_obj)
        axes[i].imshow(img_filtrada)
        color = 'red' if nombre == "FIND_EDGES" else 'black'
        axes[i].set_title(nombre, color=color, fontsize=10)
        axes[i].axis("off")
    
    plt.tight_layout()
    plt.savefig("todos_filtros.png", dpi=150)
    plt.show()
    print("Guardado: todos_filtros.png")


def modo_pintor(imagen):
    """
    Genera un boceto estilo lapiz para pintores.
    """
    if imagen is None:
        print("Error: Primero carga una imagen.")
        return None
    
    img_gris = imagen.convert("L")
    img_bordes = img_gris.filter(ImageFilter.FIND_EDGES)
    img_boceto = ImageOps.invert(img_bordes)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].imshow(imagen)
    axes[0].set_title("Foto Original")
    axes[0].axis("off")
    
    axes[1].imshow(img_boceto, cmap='gray')
    axes[1].set_title("Boceto para Pintores")
    axes[1].axis("off")
    
    plt.tight_layout()
    plt.savefig("boceto_comparacion.png")
    plt.show()
    
    img_boceto.save("boceto.jpg")
    print("Guardado: boceto.jpg y boceto_comparacion.png")
    return img_boceto


def menu():
    """
    Menu principal interactivo.
    """
    global imagen_actual
    
    while True:
        print("\n" + "="*40)
        print("         FOTOAPP - MENU")
        print("="*40)
        print("1. Cargar Imagen")
        print("2. Ajustar Contraste")
        print("3. Aplicar Filtro")
        print("4. Mostrar Todos los Filtros")
        print("5. Modo Pintor")
        print("0. Salir")
        print("="*40)
        
        opcion = input("\nSelecciona opcion: ")
        
        try:
            if opcion == '1':
                ruta = input("Ruta de la imagen: ")
                red = input("Red social (Youtube/Instagram/Twitter/Facebook): ")
                imagen_actual = cargar_imagen(ruta, red)
            
            elif imagen_actual is None:
                print("Debes cargar una imagen primero (opcion 1).")
                continue
            
            elif opcion == '2':
                ajustar_contraste(imagen_actual)
            
            elif opcion == '3':
                filtro = input("Nombre del filtro: ").upper()
                aplicar_filtro(imagen_actual, filtro)
            
            elif opcion == '4':
                mostrar_todos_filtros(imagen_actual)
            
            elif opcion == '5':
                modo_pintor(imagen_actual)
            
            elif opcion == '0':
                print("Saliendo...")
                break
            
            else:
                print("Opcion no valida.")
        
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    menu()
