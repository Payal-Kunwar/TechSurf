from PIL import Image

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from io import BytesIO

class Solution:
    def __init__(self, image):
        self.original_image = image
    
    def image_filter(self):
        width,height = self.original_image.size
        print("Dimensions of Original Image: ")
        print("Height: ", height, "and Width: ", width)
        print()
        temp = self.original_image.resize((width,height), Image.Resampling.LANCZOS)
        self.original_image = temp
        filtered_image = BytesIO()
        self.original_image.save(filtered_image, "JPEG")
        filtered_image.seek(0)
        print("Dimensions of Processed Image: ")
        print("Height: ", temp.size[1], "and Width: ", temp.size[0])
        print("The density of image is ",temp.info['dpi'][0])
        return StreamingResponse(filtered_image, media_type="image/jpeg")

    

app = FastAPI()

@app.post("/")
def calling(img: UploadFile = File(...)):
    original_image = Image.open(img.file)
    obj = Solution(original_image)  
    return obj.image_filter()

    

