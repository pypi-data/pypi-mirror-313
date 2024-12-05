from PIL import Image as PILImage

import io
import base64
import imghdr

class Image:
    def __init__(self, file_handle):
        self.file_handle = file_handle
        self.converted_image = None

    def __str__(self):
        return f"<Image(file_handle={self.file_handle})>"
    
    def read_file(self):
        self.file_handle.seek(0)
        return self.file_handle.read()
    
    def convert_image(self, image_format: str, quality: int = 90, width: int = 600, height: int = 600):

        # Read the image data
        image_data = self.read_file()
        
        # Open the image using PIL
        with PILImage.open(io.BytesIO(image_data)) as img:
            # Resize the image while maintaining aspect ratio
            img.thumbnail((width, height))
            
            # Create a new BytesIO object to store the converted image
            output = io.BytesIO()
            
            # Convert and save the image to the specified format
            img.save(output, format=image_format.upper(), quality=quality)
            
            # Reset the BytesIO object to the beginning
            output.seek(0)
            
            # Update the file_handle with the new image data
            return output
    
    def convert_to_base64(self, image_data):
        # Encode the image data to base64
        image_data.seek(0)
        return base64.b64encode(image_data.read()).decode("utf-8")
        
    @property
    def safe_image(self):
        # Return cached version if it exists
        if self.converted_image:
            self.converted_image[1].seek(0)
            return self.converted_image

        # Read image data
        image_data = self.read_file()

        # Retrieve image format through parsing the file data
        image_format = imghdr.what(None, image_data)
        
        # Check file size (2MB = 2 * 1024 * 1024 bytes)
        if len(image_data) > 2 * 1024 * 1024:
            needs_conversion = True
        else:
            # Check dimensions
            with PILImage.open(io.BytesIO(image_data)) as img:
                width, height = img.size
                needs_conversion = width > 600 or height > 600

        if needs_conversion:
            # Create converted version
            image_data = self.convert_image("jpeg", quality=90, width=600, height=600)
            
            # Cache the converted version
            self.converted_image = ("jpeg", image_data)
            return self.converted_image
        
        # Image is safe to use as-is
        return (image_format, image_data)
    
    @property
    def data_url(self):
        image_format, image_data = self.safe_image
        return f"data:image/{image_format};base64,{self.convert_to_base64(image_data)}"

    def to_json(self):
        # Convert to OpenAI image format
        return {
            "type": "image_url",
            "image_url": {
                "url": self.data_url
            }
        }