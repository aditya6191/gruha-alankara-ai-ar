import os
from PIL import Image

def process_uploaded_image(file_path):
    """
    Validates and resizes an uploaded room image before AI processing.
    Ensures the model receives a standardized input size.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Image not found at {file_path}")

    try:
        with Image.open(file_path) as img:
            # Convert to RGB in case of RGBA
            if img.mode != 'RGB':
                img = img.convert('RGB')
                
            # Resize image to a standard dimension (e.g. 512x512) for model input
            img = img.resize((512, 512), Image.Resampling.LANCZOS)
            
            # Save the processed image back
            processed_path = file_path.replace('.', '_processed.')
            img.save(processed_path, "JPEG")
            
            print(f"[Image Processor] Successfully processed {file_path} -> {processed_path}")
            return processed_path
            
    except Exception as e:
        print(f"[Image Processor] Error processing image: {e}")
        return None

if __name__ == '__main__':
    # Add a mock image test later
    pass
