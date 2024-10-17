import os
import customtkinter as ctk  # Import CustomTkinter
from tkinter import filedialog, messagebox
from google.cloud import vision
from PIL import Image

# Set up the environment variable for the API Key
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] =r"C:\Users\Momelezi.Qasana\OneDrive - Cape IT Initiative\Documents\AI Project\ai-project-438309-68f0096a3a05.json"

# Initialize the Vision API client
client = vision.ImageAnnotatorClient()

def analyze_image(image_path, result_label):
    try:
        # Load image into memory
        with open(image_path, 'rb') as image_file:
            content = image_file.read()

        # Create image object
        image = vision.Image(content=content)

        # Define the features for detection
        features = [
            vision.Feature(type=vision.Feature.Type.LABEL_DETECTION),
            vision.Feature(type=vision.Feature.Type.TEXT_DETECTION),
            vision.Feature(type=vision.Feature.Type.FACE_DETECTION),
            vision.Feature(type=vision.Feature.Type.LANDMARK_DETECTION),
            vision.Feature(type=vision.Feature.Type.LOGO_DETECTION),
            vision.Feature(type=vision.Feature.Type.OBJECT_LOCALIZATION),
        ]

        # Perform image analysis
        response = client.annotate_image({
            'image': image,
            'features': features
        })

        # Collect the results
        results = []

        # Process labels
        labels = response.label_annotations
        if labels:
            results.append("Labels Detected:")
            for label in labels:
                results.append(f"- {label.description}")

        # Process text
        texts = response.text_annotations
        if texts:
            results.append("\nText Detected:")
            for text in texts:
                results.append(f"- {text.description}")

        # Process faces
        faces = response.face_annotations
        if faces:
            results.append("\nFaces Detected:")
            for face in faces:
                results.append(f"- Detection confidence: {face.detection_confidence}")

        # Process landmarks
        landmarks = response.landmark_annotations
        if landmarks:
            results.append("\nLandmarks Detected:")
            for landmark in landmarks:
                results.append(f"- {landmark.description}")

        # Process logos
        logos = response.logo_annotations
        if logos:
            results.append("\nLogos Detected:")
            for logo in logos:
                results.append(f"- {logo.description}")

        # Display the results in the label (on the right)
        result_label.configure(text="\n".join(results))

    except Exception as e:
        messagebox.showerror("Error", f"Failed to analyze image: {e}")

def upload_image(result_label):
    # Open file dialog to select an image
    image_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
    )
    if image_path:
        # Display image preview (using CTkImage for high DPI support)
        img = Image.open(image_path)
        img.thumbnail((300, 300))
        ctk_image = ctk.CTkImage(light_image=img, size=(300, 300))

        # Create an image label if it's not created already
        if not hasattr(upload_image, "image_label"):
            upload_image.image_label = ctk.CTkLabel(window, text="")
            upload_image.image_label.place(relx=0.2, rely=0.3, anchor="n")  # Place on the left

        # Set the CTkImage to the label
        upload_image.image_label.configure(image=ctk_image)
        upload_image.image_label.image = ctk_image  # Store reference to avoid garbage collection

        # Analyze the image and display results (on the right side)
        analyze_image(image_path, result_label)

# Set up CustomTkinter theme
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

# Create the CustomTkinter window
window = ctk.CTk()
window.title("Image Analysis with Google Cloud Vision API")
window.geometry("900x600")  # Increased width to fit both image and text side by side

# Create and place an upload button (centered and bigger)
upload_button = ctk.CTkButton(window, text="Upload Image", command=lambda: upload_image(result_label),
                              font=("Helvetica", 14), fg_color="#4CAF50", hover_color="#45a049", text_color="white", width=200, height=50)
upload_button.place(relx=0.5, rely=0.1, anchor="center")

# Create a label to display the results (placed on the right side of the image)
result_label = ctk.CTkLabel(window, text="", justify="left", font=("Arial", 12), wraplength=400)
result_label.place(relx=0.6, rely=0.3, anchor="n")  # Place on the right side of the image

# Start the CustomTkinter loop
window.mainloop()
