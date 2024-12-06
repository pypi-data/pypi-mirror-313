import fitz
import boto3
import pandas as pd
from typing import Dict, Any

# Variable global para el cliente de Textract
textract_client = None

def credentials(aws_access_key_id: str, aws_secret_access_key: str, region: str ="us-east-1"):
    """
    Configura las credenciales de AWS para usar Textract
    """
    global textract_client
    textract_client = boto3.client(
        service_name='textract',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region
    )

def extract_text_and_tables_with_textract(image_bytes) -> str:
    """
    Extrae texto y tablas de una imagen usando AWS Textract.
    """
    if textract_client is None:
        raise ValueError("AWS credentials not set. Call credentials() first.")

    response = textract_client.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['TABLES']
    )
    
    result = ""
    has_table = False
    
    # Verificar si hay tablas en el documento
    for block in response['Blocks']:
        if block['BlockType'] == 'TABLE':
            has_table = True
            # Encontrar las dimensiones máximas de la tabla
            max_row = 0
            max_col = 0
            for cell_block in response['Blocks']:
                if cell_block['BlockType'] == 'CELL':
                    row_index = cell_block['RowIndex']
                    col_index = cell_block['ColumnIndex']
                    max_row = max(max_row, row_index)
                    max_col = max(max_col, col_index)
            
            # Crear una matriz vacía con las dimensiones correctas
            table_array = [['' for _ in range(max_col)] for _ in range(max_row)]
            
            # Llenar la matriz con los valores
            for cell_block in response['Blocks']:
                if cell_block['BlockType'] == 'CELL':
                    row_index = cell_block['RowIndex'] - 1
                    col_index = cell_block['ColumnIndex'] - 1
                    
                    if 'Relationships' in cell_block:
                        cell_text = ''
                        for relationship in cell_block['Relationships']:
                            if relationship['Type'] == 'CHILD':
                                for child_id in relationship['Ids']:
                                    for child_block in response['Blocks']:
                                        if child_block['Id'] == child_id and child_block['BlockType'] == 'WORD':
                                            cell_text += child_block['Text'] + ' '
                        table_array[row_index][col_index] = cell_text.strip()
            
            # Convertir la matriz a DataFrame
            df = pd.DataFrame(table_array)
            
            # Si hay datos en el DataFrame, usar la primera fila como encabezados
            if not df.empty:
                df.columns = df.iloc[0]
                df = df[1:]
                
                # Convertir DataFrame a string en formato CSV
                result += "\n=== TABLA ===\n"
                result += df.to_csv(index=False)
                result += "=== FIN TABLA ===\n"
    
    # Si no hay tabla, procesar como texto normal
    if not has_table:
        for block in response['Blocks']:
            if block['BlockType'] == 'LINE':
                result += block['Text'] + "\n"
    
    return result

def process_pdf(file_path: str, pages: int = 0) -> Dict[str, Any]:
    """
    Procesa un PDF mixto (texto e imágenes/tablas) y extrae el contenido en orden.
    """
    if textract_client is None:
        raise ValueError("AWS credentials not set. Call credentials() first.")

    pdf_file = fitz.open(file_path)
    num_pages = len(pdf_file)
    document_index = {}

    if pages > 0:
        num_pages = pages

    for page_index in range(num_pages):
        page = pdf_file[page_index]
        full_text = ""

        # Calcular el área de la página
        page_rect = page.rect
        page_width = page_rect.width
        page_height = page_rect.height
        page_area = page_width * page_height

        # Obtener las imágenes primero
        image_list = page.get_images(full=True)
        image_regions = []

        # Crear un conjunto de regiones ocupadas por imágenes
        for img in image_list:
            xref = img[0]
            bbox = page.get_image_bbox(img)
            
            image_width = bbox.width
            image_height = bbox.height
            image_area = image_width * image_height
            percentage = (image_area / page_area) * 100

            if percentage > 5:
                image = pdf_file.extract_image(xref)
                image_bytes = image["image"]
                image_regions.append({
                    "type": "image",
                    "content": image_bytes,
                    "bbox": bbox
                })

        # Obtener bloques de texto que no se superponen con imágenes
        text_blocks = page.get_text("blocks")
        content_list = []

        for block in text_blocks:
            x0, y0, x1, y1, text, _, _ = block
            block_bbox = fitz.Rect(x0, y0, x1, y1)
            
            # Verificar si el bloque se superpone con alguna imagen
            overlaps_with_image = False
            for img_region in image_regions:
                img_bbox = img_region["bbox"]
                if block_bbox.intersects(img_bbox):
                    overlaps_with_image = True
                    break
            
            # Solo añadir el bloque si no se superpone con una imagen
            if not overlaps_with_image and text.strip():
                content_list.append({
                    "type": "text",
                    "content": text.strip(),
                    "bbox": block_bbox
                })

        # Añadir las regiones de imagen a la lista de contenido
        content_list.extend(image_regions)

        # Ordenar contenido por posición vertical (y0)
        content_list.sort(key=lambda x: x["bbox"].y0)

        # Procesar contenido en orden
        for item in content_list:
            if item["type"] == "text":
                full_text += item["content"] + "\n"
            elif item["type"] == "image":
                ocr_text = extract_text_and_tables_with_textract(item["content"])
                full_text += ocr_text + "\n"
        
        document_index[page_index + 1] = full_text

    pdf_file.close()
    return document_index