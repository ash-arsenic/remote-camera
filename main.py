from flask import Flask, request, render_template
import cv2 as cv
from time import time_ns
import firebase_admin as fb
from firebase_admin import storage

# Initialising firebase storage
cred = fb.credentials.Certificate('./opencv-49a1b-firebase-adminsdk-j8c2f-51b048b4bb.json')
fb.initialize_app(cred, {
    'storageBucket': 'opencv-49a1b.appspot.com'
})
bucket = storage.bucket()

# Flask Constructor
app = Flask(__name__)


# Main Page
@app.route("/")
def showHomePage():
    return "This is home page"


# Logic
@app.route("/debug", methods=["GET"])
def debug():
    imgs = cv.VideoCapture(0)
    result, image = imgs.read()

    if result:
        print("Photo Clicked")
        current_time = time_ns()
        file_name = 'gg' + str(current_time) + '.png'
        cv.imwrite(file_name, image)

        print("Photo Saved")

        blob = bucket.blob(file_name)
        blob.upload_from_filename(file_name)

        print("Photo Uploaded")
        blob.make_public()
        print(blob.public_url)
        return blob.public_url
    else:
        return "https://www.elegantthemes.com/blog/wp-content/uploads/2020/08/000-http-error-codes.png"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
