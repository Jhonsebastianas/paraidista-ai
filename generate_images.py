from PIL import Image, ImageDraw, ImageFont
import os

def create_cromosoma_paracaidista():
    # Crear imagen para cromosoma del paracaidista
    width, height = 500, 250
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)

    # Intentar cargar fuente, si no usar default
    try:
        font = ImageFont.truetype("arial.ttf", 16)
        title_font = ImageFont.truetype("arial.ttf", 20)
        small_font = ImageFont.truetype("arial.ttf", 12)
    except:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Título
    draw.text((10, 10), "Cromosoma del Paracaidista", fill='black', font=title_font)

    # Representación visual del cromosoma como cajas conectadas
    box_width = 80
    box_height = 40
    start_x = 50
    y = 60

    # Cromosoma principal
    draw.rectangle([start_x, y, start_x + box_width*4 + 30, y + box_height], outline='black', width=3)

    # Genes individuales
    genes = ['V', 'B', 'S', 'F']
    values = ['2.34', '-0.56', '0.78', '0.12']
    limits = ['[1.5,6.0]', '[-1.5,1.5]', '[0.0,1.0]', '[0.0,1.0]']

    for i, (gene, value, limit) in enumerate(zip(genes, values, limits)):
        x = start_x + 10 + i * (box_width + 5)
        # Caja del gen
        draw.rectangle([x, y, x + box_width, y + box_height], outline='black', width=2, fill='lightblue')
        # Nombre del gen
        draw.text((x + box_width//2 - 5, y + 5), gene, fill='black', font=font)
        # Valor
        draw.text((x + box_width//2 - 15, y + 20), value, fill='red', font=small_font)
        # Límites abajo
        draw.text((x + 5, y + box_height + 5), limit, fill='black', font=small_font)

    # Flechas entre genes
    for i in range(3):
        arrow_x = start_x + box_width + i * (box_width + 5) + 10
        draw.text((arrow_x, y + 10), "→", fill='black', font=font)

    # Descripción
    draw.text((10, 180), "Cada gen representa un parámetro físico del paracaidista:", fill='black', font=font)
    draw.text((10, 200), "• V: Velocidad de caída", fill='black', font=small_font)
    draw.text((10, 215), "• B: Balanceo lateral", fill='black', font=small_font)
    draw.text((250, 200), "• S: Estabilidad", fill='black', font=small_font)
    draw.text((250, 215), "• F: Factor adicional", fill='black', font=small_font)

    return img

def create_cromosoma_ahorro():
    # Crear imagen para cromosoma del ahorro
    width, height = 400, 200
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 16)
        title_font = ImageFont.truetype("arial.ttf", 20)
        small_font = ImageFont.truetype("arial.ttf", 12)
    except:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Título
    draw.text((10, 10), "Cromosoma del Planificador de Ahorro", fill='black', font=title_font)

    # Representación visual del cromosoma
    box_width = 100
    box_height = 40
    start_x = 150
    y = 60

    # Cromosoma principal
    draw.rectangle([start_x, y, start_x + box_width, y + box_height], outline='black', width=3, fill='lightgreen')

    # Gen
    gene = "Porcentaje"
    value = "0.35"
    limit = "[0.1, 0.8]"

    # Caja del gen
    draw.rectangle([start_x, y, start_x + box_width, y + box_height], outline='black', width=2, fill='lightgreen')
    # Nombre del gen
    draw.text((start_x + box_width//2 - 30, y + 5), gene, fill='black', font=font)
    # Valor
    draw.text((start_x + box_width//2 - 15, y + 20), value, fill='red', font=small_font)
    # Límites abajo
    draw.text((start_x + 10, y + box_height + 5), limit, fill='black', font=small_font)

    # Descripción
    draw.text((10, 130), "El gen representa el porcentaje del ingreso", fill='black', font=font)
    draw.text((10, 150), "mensual destinado al ahorro", fill='black', font=font)
    draw.text((10, 170), "• Rango: 10% - 80% del ingreso", fill='black', font=small_font)

    return img

def create_aplicacion_paracaidista():
    # Placeholder para aplicación del paracaidista
    width, height = 600, 400
    img = Image.new('RGB', (width, height), 'lightblue')
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()

    # Simular interfaz
    draw.rectangle([0, 0, width, 50], fill='gray')
    draw.text((10, 10), "Simulación del Paracaidista - Algoritmo Genético", fill='white', font=font)

    # Área de simulación
    draw.rectangle([50, 100, 350, 350], fill='skyblue', outline='black')
    draw.ellipse([150, 150, 200, 200], fill='blue')  # Paracaidista
    draw.text((160, 170), "P", fill='white', font=font)

    # Panel lateral
    draw.rectangle([400, 50, 580, 350], fill='white', outline='black')
    draw.text((410, 60), "Panel de Control", fill='black', font=font)
    draw.text((410, 90), "Generación: 15", fill='black', font=font)
    draw.text((410, 115), "V: 2.34", fill='black', font=font)
    draw.text((410, 140), "B: -0.56", fill='black', font=font)
    draw.text((410, 165), "S: 0.78", fill='black', font=font)
    draw.text((410, 190), "F: 0.12", fill='black', font=font)
    draw.text((410, 215), "Fitness: 0.85", fill='black', font=font)

    return img

def create_aplicacion_ahorro():
    # Placeholder para aplicación del ahorro
    width, height = 600, 400
    img = Image.new('RGB', (width, height), 'lightgreen')
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 20)
        title_font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()

    # Título
    draw.text((10, 10), "Planificador de Ahorro - Algoritmo Genético", fill='black', font=title_font)

    # Panel izquierdo - Entradas
    draw.rectangle([20, 50, 280, 350], fill='white', outline='black')
    draw.text((30, 60), "💰 Ingreso mensual: $3000", fill='black', font=font)
    draw.text((30, 90), "🎯 Meta de ahorro: $50000", fill='black', font=font)
    draw.text((30, 120), "📅 Plazo: 24 meses", fill='black', font=font)
    draw.rectangle([30, 160, 120, 190], fill='lightblue', outline='black')
    draw.text((40, 165), "Calcular", fill='black', font=font)

    # Panel derecho - Resultados
    draw.rectangle([320, 50, 580, 350], fill='white', outline='black')
    draw.text((330, 60), "🔹 Resultados", fill='black', font=title_font)
    draw.text((330, 100), "Ahorro mensual: 25.0%", fill='black', font=font)
    draw.text((330, 130), "Ahorro mensual: $750.00", fill='black', font=font)
    draw.text((330, 160), "Ahorro total: $18000.00", fill='black', font=font)
    draw.text((330, 190), "Meta: $50000.00", fill='black', font=font)

    return img

def main():
    # Crear directorio assets si no existe
    if not os.path.exists('assets'):
        os.makedirs('assets')

    # Generar imágenes
    cromosoma_paracaidista = create_cromosoma_paracaidista()
    cromosoma_paracaidista.save('assets/cromosoma_paracaidista.png')

    cromosoma_ahorro = create_cromosoma_ahorro()
    cromosoma_ahorro.save('assets/cromosoma_ahorro.png')

    aplicacion_paracaidista = create_aplicacion_paracaidista()
    aplicacion_paracaidista.save('assets/aplicacion_paracaidista.png')

    aplicacion_ahorro = create_aplicacion_ahorro()
    aplicacion_ahorro.save('assets/aplicacion_ahorro.png')

    print("Imágenes generadas exitosamente en la carpeta 'assets'")

if __name__ == "__main__":
    main()