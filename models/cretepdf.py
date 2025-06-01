import os
import json
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from PIL import Image

def create_pdf_from_images(image_dir, output_path, padding=0.5*inch):
    # Define the PDF page size
    page_width, page_height = letter

    # Create the PDF canvas
    c = canvas.Canvas(output_path, pagesize=letter)

    image_index = 1

    for i in range(0, 12):
        image_path = os.path.join(image_dir, f"panel-{image_index}.png")
        
        # Check if the image file exists
        if not os.path.exists(image_path):
            break

        # Load the image
        image = Image.open(image_path)
        img_width, img_height = image.size

        # Calculate the maximum image dimensions to fit the page width
        max_img_width = page_width - 2 * padding
        scale_factor = max_img_width / img_width
        scaled_img_width = max_img_width
        scaled_img_height = img_height * scale_factor

        # Calculate positions to center the image
        image_x = (page_width - scaled_img_width) / 2
        image_y = (page_height - scaled_img_height) / 2 + padding

        # Draw the image centered on the page
        c.drawImage(image_path, image_x, image_y, width=scaled_img_width, height=scaled_img_height)

        # Show page
        c.showPage()

        image_index += 1

    # Save the PDF
    c.save()
    print("saved pdf successfully")
    
    # Return the output path
    return output_path

# Example usage:
pdf_path = create_pdf_from_images('C:\sd\mini-proj\output', 'output-new.pdf')
print(f"PDF saved at: {pdf_path}")
