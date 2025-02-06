import streamlit as st
from PIL import Image, ImageOps
import io

# Function to process the image
def process_product_image(image):
    base_width, base_height = 1200, 800
    img = Image.open(image).convert("RGBA")

    # Resize image while maintaining aspect ratio
    img.thumbnail((base_width - 100, base_height - 100), Image.LANCZOS)

    # Create a white canvas
    white_canvas = Image.new("RGBA", (base_width, base_height), (255, 255, 255, 255))

    # Get center position with proper margins
    img_w, img_h = img.size
    x_offset = (base_width - img_w) // 2
    y_offset = (base_height - img_h) // 2

    # Paste image onto white canvas
    white_canvas.paste(img, (x_offset, y_offset), img)
    processed_img = white_canvas.convert("RGB")

    return processed_img

# Streamlit UI
def main():
    st.title("Deliveroo Product Image Formatter")
    st.write("Upload a product image, and this tool will process it to 1200x800 with a white background.")
    
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        if st.button("Process Image"):
            processed_img = process_product_image(uploaded_file)
            st.image(processed_img, caption="Formatted Image", use_column_width=True)
            
            # Convert image to downloadable format
            img_byte_arr = io.BytesIO()
            processed_img.save(img_byte_arr, format='JPEG', quality=100)
            img_byte_arr = img_byte_arr.getvalue()
            
            st.download_button(
                label="Download Processed Image",
                data=img_byte_arr,
                file_name="formatted_product.jpg",
                mime="image/jpeg"
            )

if __name__ == "__main__":
    main()
