import face_recognition
import cv2
from PIL import Image, ImageDraw
from datetime import datetime as dt

def makeup(image_path):
    my_image = cv2.imread(image_path)

    face_landmarks = face_recognition.face_landmarks(my_image)
    my_image = cv2.cvtColor(my_image, cv2.COLOR_BGR2RGB)

    pil_image = Image.fromarray(my_image)
    drawer = ImageDraw.Draw(pil_image, mode='RGBA')
    for face_lnd in face_landmarks:
        #
        drawer.polygon(face_lnd['left_eyebrow'], fill=(43, 21, 14, 230))
        drawer.polygon(face_lnd['right_eyebrow'], fill=(43, 21, 14, 230))
        #
        drawer.polygon(face_lnd['left_eye'], fill=(250, 20, 20, 50))
        drawer.polygon(face_lnd['right_eye'], fill=(250, 20, 20, 50))
        #
        drawer.line(face_lnd['left_eye'] + [face_lnd['left_eye'][0]],
                    fill=(0, 0, 0, 200), width=3)
        drawer.line(face_lnd['right_eye'] + [face_lnd['right_eye'][0]],
                    fill=(0, 0, 0, 200), width=3)
        #
        drawer.polygon(face_lnd['bottom_lip'], fill=(205, 20, 20, 200))
        drawer.polygon(face_lnd['top_lip'], fill=(205, 20, 20, 200))
    now = str(dt.now().day) + str(dt.now().hour) + str(dt.now().minute) + str(dt.now().second) + str(
        dt.now().microsecond)
    file_name = f'New Image - {now}.jpg'
    pil_image.save(file_name)
    return file_name
