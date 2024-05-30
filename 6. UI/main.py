from tkinter import *
import cv2
from PIL import Image, ImageTk
import sqlite3
import tensorflow.compat.v2 as tf
from keras.models import load_model
import numpy as np
import pygame
import io
import urllib.request
from gtts import gTTS
import pygame

language = "ne"
gender = "female"

words = {"text": "", "words1": "", "words2": ""}

model = load_model("model.h5")

root = Tk()
root.title("Nepali Sign Language Recognition and Translation")
root.iconbitmap("icon.ico")
root.config(background="#000000")

text = StringVar()
words1 = StringVar()
words2 = StringVar()

bold_font = ("Roboto", 15, "bold")
label = Label(
    root,
    text="Nepali Sign Language Recognition and Translation",
    font=bold_font,
    foreground="#e11d3a",
    background="black",
    padx=10,
    pady=10,
)
label.pack()

label1 = Label(
    root,
    text="Predicted Sign Language",
    font=bold_font,
    foreground="#F7941D",
    background="black",
    padx=10,
    pady=10,
)
label1.pack()

label2 = Label(
    root,
    textvariable=text,
    font=bold_font,
    foreground="white",
    background="black",
    padx=10,
    pady=10,
)
label2.pack()

label3 = Label(
    root,
    text="Word",
    font=bold_font,
    foreground="#F7941D",
    background="black",
    padx=10,
    pady=10,
)
label3.pack()

label4 = Label(
    root,
    textvariable=words1,
    font=bold_font,
    foreground="white",
    background="black",
    padx=10,
    pady=10,
)
label4.pack()


label5 = Label(
    root,
    text="Sentence",
    font=bold_font,
    foreground="#F7941D",
    background="black",
    padx=10,
    pady=10,
)
label5.pack()

label6 = Label(
    root,
    textvariable=words2,
    font=bold_font,
    foreground="white",
    background="black",
    padx=10,
    pady=10,
)
label6.pack()

video_label = Label(root, padx=10, pady=5)
video_label.pack()


def check_keypress(event):
    if event.keysym == "s":
        words["words1"] += words["text"]
    elif event.keysym == "q":
        words["words2"] += words["words1"]
        words["words2"] += " "
        words["words1"] = ""
    elif event.keysym == "a":
        # Create a gTTS object and specify the text and language
        tts = gTTS(words["words2"], lang="ne")

        # Save the speech as an MP3 file
        tts.save("hello.mp3")

        # Initialize Pygame mixer
        pygame.mixer.init()

        # Load the MP3 file into a Pygame mixer Sound object
        sound = pygame.mixer.Sound("hello.mp3")

        # Play the sound
        sound.play()

        # Wait for the sound to finish playing
        pygame.time.wait(int(sound.get_length() * 1000))


video_label.bind("<Key>", check_keypress)
# video_label.bind("<Key>", audio_stream)
video_label.focus_set()


def update_text():
    # dynamically import the variable from a module
    dynamic_text = words["text"]
    dynamic_words = words["words1"]
    dynamic_words2 = words["words2"]
    text.set(dynamic_text)
    words1.set(dynamic_words)
    words2.set(dynamic_words2)

    # text.set("dynamic_text")
    # schedule another check after 500 milliseconds
    root.after(500, update_text)


def keras_process_image(img):
    img = cv2.resize(img, (300, 300))
    img = np.array(img, dtype=np.float32)
    img = np.reshape(img, (1, 300, 300, 1))
    return img


def keras_predict(model, image):
    processed = keras_process_image(image)
    pred_probab = model.predict(processed)[0]
    pred_class = list(pred_probab).index(max(pred_probab))
    return max(pred_probab), pred_class


def get_pred_text_from_db(pred_class):
    conn = sqlite3.connect("gesture_db1.db")
    cmd = "SELECT g_name FROM gesture WHERE g_id=" + str(pred_class)
    cursor = conn.execute(cmd)
    for row in cursor:
        return row[0]


# create a video capture object to capture video from the default camera
cap = cv2.VideoCapture(0)


def show_frame():
    # capture a frame from the video stream
    ret, frame = cap.read()

    if ret:
        # convert the OpenCV frame to a PIL image
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(image, 1)
        cv2.rectangle(frame, (270 - 1, 9), (620 + 1, 355), (265, 0, 0), 1)
        roi = frame[50:350, 270:570]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 2)
        blur = cv2.bilateralFilter(blur, 3, 75, 75)
        th3 = cv2.adaptiveThreshold(
            blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
        )
        ret, roi = cv2.threshold(th3, 70, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        interrupt = cv2.waitKey(10)
        roi = cv2.resize(roi, (300, 300))
        save_img = roi
        pred_probab, pred_class = keras_predict(model, save_img)
        if pred_probab * 100 == 100:
            text = get_pred_text_from_db(pred_class)
            words["text"] = text
            print(words["text"])
        # interrupt = -1
        # if interrupt & 0xFF == ord("b"):
        #     words["words1"] += words["text"]
        #     print(words["words1"])

        # words["words1"] += text
        # print(words["words1"])
        image = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image)

        # display the PIL image in the label
        video_label.config(image=photo)
        video_label.image = photo

    # schedule the next frame capture
    label.after(10, show_frame)


show_frame()
update_text()
root.mainloop()
