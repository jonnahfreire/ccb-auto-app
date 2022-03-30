import os
import glob

# import pytesseract as tess
# from pdfminer.high_level import extract_text
# To convert PDF into an Image file, we need to pip install wand
# from wand.image import Image
# import PIL


 
# pdf_file = "images/cf.pdf"
 
# # files = []
# def convert_pdf2img(pdf_file):
#     with(Image(filename=pdf_file, resolution = 500)) as conn: 
#         for index, image in enumerate(conn.sequence):
#             image_name = os.path.splitext(pdf_file)[0] + str(index + 1) + '.png'
#             Image(image).save(filename = image_name)
#             # files.append(image_name)

# def get_text_from_image(img_path):
#     img = PIL.Image.open(img_path)
#     text = tess.image_to_string(img)
#     print(text)

# def get_text_from_pdf(pdf_path):
#     text = extract_text(pdf_path)
#     print(text)


def file_read(path):
    for file in glob.glob(path):
        print(file)

# get_text_from_pdf("images/cf.pdf")
# convert_pdf2img("images/cf.pdf")
# get_text_from_image("images/cf1.png")

from document_models.models import *

def get_data_from_filename(document_model, file):

    file_data = [os.path.splitext(f.strip())[0] for f in file.split("-")]

    for data in file_data:

        if len(data) > 0 and "CF" in data:
            document_model["type"] = "NOTA FISCAL"
            document_model["num"] = data.replace("CF", "").strip()
        
        if len(data) > 0 and "NF" in data or "NF RC" in data:
            document_model["type"] = "NOTA FISCAL"
            document_model["num"] = data.replace("CF", "")\
                                        .replace("NF", "")\
                                        .replace("RC", "")\
                                        .replace("NF RC", "").strip()

        if len(data) > 0 and "CH" in data:
            document_model["check-num"] = data.replace("CH", "").strip()

        if len(data) > 0 and ":" in data:
            document_model["date"] = data.split(":")

        if len(data) > 0 and "R$" in data:
            document_model["value"] = data.replace("R$", "").strip()
        
        if len(data) > 0 and not "R$" in data \
            or not "CF" in data or not ":" in data\
                or not "NF" in data or not "RC" in data\
                    or not "CH" in data:
            document_model["emitter"] = data.strip()

    return document_model


files = []
for file in os.listdir("files/1000/3026"):
    files.append(get_data_from_filename(model3026, file))
    
for f in files:
    print(f)