import cv2
import numpy as np
import argparse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import fitz
from PIL import Image

from toolbox import update_ui
from toolbox import CatchException, report_exception
from toolbox import write_history_to_file, promote_file_to_downloadzone
from .crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
import pypandoc
fast_debug = False

# Adjustable font and size
font_name = "Helvetica"
font_size = 30
import pdfkit
import tempfile
import shutil
import os



def create_pdf_with_markdown(markdown_text):
    # 指定wkhtmltopdf的路徑
    path_wkhtmltopdf = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    
    # 創建一個暫存檔案
    # temp_pdf = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)  # delete=False 是必須的，這樣檔案不會在關閉時被刪除
    pdf_path = "output.pdf"
    # Convert the Markdown text to PDF using pypandoc
    pypandoc.convert_text(markdown_text, 'pdf', format='md', outputfile=pdf_path, extra_args=['--pdf-engine=xelatex'])


    return pdf_path



def create_pdf_with_text(text, pdf_filename='output'):
    # Create a PDF document
    pdf_path = pdf_filename + ".pdf"
    c = canvas.Canvas(pdf_path, pagesize=A4)

    # Set font and size
    c.setFont(font_name, font_size)

    # Add text to the PDF with word wrapping
    width, height = A4
    max_width = width - 2 * 50  # Adjusted for left and right margins
    y_position = height - 50  # Starting position for text

    def draw_text_with_word_wrap(text):
        lines = []
        current_line = ""

        for word in text.split():
            if c.stringWidth(current_line + word, font_name, font_size) <= max_width:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "

        lines.append(current_line.strip())

        return lines

    wrapped_lines = draw_text_with_word_wrap(text)

    for line in wrapped_lines:
        c.drawString(50, y_position, line)
        y_position -= font_size  # Adjust for the next line

    # Save the PDF
    c.save()

    return pdf_path

def convert_pdf_to_image(pdf_path, image_filename):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document.load_page(0)  # Load the first page (index 0)

    # Get the dimensions of the page
    mat = fitz.Matrix(2, 2)  # You can adjust the scaling factor
    pix = page.get_pixmap(matrix=mat)

    # Convert the pixmap to a PIL Image
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Save the image
    img_path = image_filename + ".png"
    img.save(img_path, "PNG")

    pdf_document.close()

    return img_path

# Step 1: Read the image


def imageProcessor(image_filename):
    image = cv2.imread(image_filename)
    image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    image = cv2.flip(image, 0)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blur, 10, 255)
    contours, hierarchy = cv2.findContours(
        edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return contours

# Step 4: Convert contours to G-code


def contour2Gcode(contours):
    feedrate = 1000
    gcode = []

    for contour in contours:
        gcode.append('M3 S40')  # Raise pen
        for point in contour:
            # The machine moves in inches, turn into mm first
            x, y = point[0] / 25.4
            gcode.append('G00 X{:.3f} Y{:.3f} F{}'.format(
                x, y, feedrate))  # Move pen to starting point
            gcode.append('M5')  # Lower pen
            gcode.append('G01 X{:.3f} Y{:.3f} F{}'.format(
                x, y, feedrate))  # Draw the contour

    # Move to the origin
    gcode.append('M3 S40')
    gcode.append('\n')
    gcode.append('G00 X0 Y0 F{}'.format(feedrate))

    # Save gcode file
    with open('out.gcode', 'w') as file:
        for command in gcode:
            file.write(command + '\n')

    print("G-code generation complete.")

@CatchException
def answer_to_gcode(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port, model="gpt-4-vision-preview"):
    chatbot.append(
        ["Function plugin?", "Making chatbot answers to gcode. Contributors: Brian, Dow"])
    yield from update_ui(chatbot=chatbot, history=history)  # 刷新介面

    try:
        import cv2
        import numpy as np
        import argparse
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        import fitz
        from PIL import Image
    except Exception as e:
        report_exception(chatbot, history, a="Robot Test", b=str(e))

    history = []

    yield from update_ui(chatbot=chatbot, history=history)
    
    pdf_path = create_pdf_with_markdown(txt)

    image_path = convert_pdf_to_image(pdf_path, 'output_image')

    contours = imageProcessor(image_path)

    contour2Gcode(contours)
    
    res = write_history_to_file(history)
    promote_file_to_downloadzone(res, chatbot=chatbot)
    chatbot.append(["Finished?", res])
    yield from update_ui(chatbot=chatbot, history=history)

# Main execution
if __name__ == "__main__":
    history = []
    chatbot = []  # Replace with actual chatbot object if available
    system_prompt = ""
    web_port = 8000  # Replace with actual web port if necessary
    answer_to_gcode(chatbot, history, system_prompt, web_port)
