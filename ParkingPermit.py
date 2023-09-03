#Take a pdf file of the daily parking permit, automatically crop to the required size and upload to the icloud drive
from tabulate import tabulate
from pdf2image import convert_from_path
from PIL import Image, ImageDraw, ImageFont
from pytesseract import pytesseract
import cv2
import numpy
from pyzbar.pyzbar import decode
import argparse
import os
import telebot


#convert pdf files to images 
def convert_file(pdf):
    images = convert_from_path(pdf, fmt="png")
    grayImage = cv2.cvtColor(numpy.array(images[0]), cv2.COLOR_BGR2GRAY)
    return grayImage 

#extract text from image 
def extract_text(image):
    text = pytesseract.image_to_string(image, lang='eng')
    return text

#crop only the QR code and save as an image 

def crop_QR(image):
    barcode = decode(image)[0]
    roi = barcode.polygon
    
    top_left_x = min([roi[0].x,roi[1].x,roi[2].x,roi[3].x])
    top_left_y = min([roi[0].y,roi[1].y,roi[2].y,roi[3].y])
    bot_right_x = max([roi[0].x,roi[1].x,roi[2].x,roi[3].x])
    bot_right_y = max([roi[0].y,roi[1].y,roi[2].y,roi[3].y])

    cropped_img = image[top_left_y:bot_right_y+1, top_left_x:bot_right_x+1]
    return cropped_img

#pull all text data from the pdf 

def structure_text(raw_text):
    parking_info_dict = {"PARKING LOT":"", "PERMIT ID":"","ADDRESS":"","PERMIT VALID FOR":"","AFFILIATION":"HARVARD Personnel","LICENSE PLATE":"4kcl21"}
    parking_key = parking_info_dict.keys()
    parking_value = parking_info_dict.values()
    text_list = raw_text.split("\n")

    for i in list(parking_key):
        if i in text_list:
            text_list.remove(i)
    
    for i in list(parking_value):
        if i != "":
            if i in text_list:
                text_list.remove(i)

    for i in text_list:
        print(i)
        if "Lot" in i:
            parking_info_dict["PARKING LOT"] = i
            print("PARKING LOT")
        if "AM To" in i:
            parking_info_dict["PERMIT VALID FOR"] = i
            print("PERMIT VALID FOR")
        if " " not in i and len(i) == 8:
            parking_info_dict["PERMIT ID"] = i 
            print("PERMIT ID")
        if parking_info_dict["PARKING LOT"] in i:
            parking_info_dict["ADDRESS"] = i
            print("ADDRESS")

        table_rows = []

        # Format the table and append each row to the list
        for key, value in parking_info_dict.items():
            row = f"""{key}:\n{value}\n"""
            table_rows.append(row)

        # Join the rows into a single string variable
        formatted_table = "\n".join(table_rows)

    return formatted_table

#create a image file 5.3cm in width, unlimited length 

def generate_parking_permit(qr_code, text):
    title_font_size = 28
    title_font = ImageFont.truetype("FONT DIRECTORY", title_font_size)
    title = "Harvard University Parking Permit"
    
    width_cm = 5.3
    dpi = 200  # Typical DPI for print
    width_pixels = int(width_cm * dpi / 2.54)  # Convert cm to pixels
    height_pixels = 900  # Adjust the height as needed
    background_color = (255, 255, 255)  # White background

    image = Image.new("RGB", (width_pixels, height_pixels), background_color)
    draw = ImageDraw.Draw(image)

    draw.text((20,5), title, fill=(128,128,128), font=title_font)

    background_image = Image.fromarray(qr_code)
    
    # Calculate the width and height of the centered image with margins
    margin = 20
    centered_width = width_pixels - 2 * margin
    centered_height = background_image.height * centered_width // background_image.width

    # Resize the background image to fit the centered dimensions
    background_image = background_image.resize((centered_width, centered_height))

    # Paste the background image onto the blank image with margins
    image.paste(background_image, (margin, 50))

    font_size = 23
    font = ImageFont.truetype("FONT DIRECTORY", font_size)

    # Define text color
    text_color = (0, 0, 0)  # Black text

    # Define text position (adjust as needed)
    text_position = (20, background_image.height + 60)

    # Draw the formatted text on the image
    draw.text(text_position, text, fill=text_color, font=font)
    output_image_path = "./output_image.png"
    image.save(output_image_path)

    return output_image_path 

def telegram_bot(output_image_path):
    # Your Telegram bot token
    bot_token = 'BOT TOKEN'
    # Chat ID to send the image to (your own chat ID)
    chat_id = 'CHAT ID'

    # Create a Telegram bot
    bot = telebot.TeleBot(bot_token)
    try:
        with open(output_image_path, "rb") as photo:
            bot.send_photo(chat_id=chat_id, photo=photo)
        print("Image sent successfully!")
    except Exception as e:
        print(f"An error occurred while sending the image: {str(e)}")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process an image file and generate a parking permit.')
    parser.add_argument('file_directory', help='The directory of the image file to process.')
    args = parser.parse_args()
    file_directory = args.file_directory

    img = convert_file(file_directory)
    text = extract_text(img)
    qr_code = crop_QR(img)
    structured_text = structure_text(text)
    output_image_path = generate_parking_permit(qr_code, structured_text)
    telegram_bot(output_image_path)
