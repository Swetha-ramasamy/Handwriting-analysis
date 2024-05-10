# import cv2
# import pytesseract

# def extract_text_from_image(image_path):
#     # Read the image using OpenCV
#     img = cv2.imread(image_path)

#     # Convert the image to grayscale
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # Apply thresholding to preprocess the image
#     _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

#     # Use pytesseract to do OCR on the preprocessed image
#     text = pytesseract.image_to_string(thresh)

#     return text

# # Provide the path to your handwritten image
# image_path = 'my.png'

# # Extract text from the image
# extracted_text = extract_text_from_image(image_path)

# # Print the extracted text
# print(extracted_text)


import cv2
import tkinter as tk
from tkinter import filedialog
import pytesseract



selected_filename = ""

def classify_letter_size(image_path):
    # Load image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply thresholding
    _, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Classify letter size based on contour area
    sizes = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < SMALL_THRESHOLD:
            sizes.append("Small")
        elif area < MEDIUM_THRESHOLD:
            sizes.append("Medium")
        else:
            sizes.append("Large")

    return sizes

def conclude_overall_size(sizes):
    small_count = sizes.count('Small')
    medium_count = sizes.count('Medium')
    large_count = sizes.count('Large')
    
    if large_count >= medium_count and large_count >= small_count:
        return 'Large'
    elif medium_count >= large_count and medium_count >= small_count:
        return 'Medium'
    else:
        return 'Small'

# Constants for thresholding
SMALL_THRESHOLD = 100
MEDIUM_THRESHOLD = 200




def classify_letter_spacing(image_path):
    # Load image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply thresholding
    _, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours from left to right
    contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[0])

    # Calculate spacing between contours
    spacing = []
    for i in range(len(contours) - 1):
        curr_contour = contours[i]
        next_contour = contours[i + 1]
        curr_x, _, _, _ = cv2.boundingRect(curr_contour)
        next_x, _, _, _ = cv2.boundingRect(next_contour)
        space = next_x - (curr_x + cv2.boundingRect(curr_contour)[2])
        spacing.append(space)

    # Classify spacing
    spacing_classification = []
    for space in spacing:
        if space > WIDE_THRESHOLD:
            spacing_classification.append("Wide")
        else:
            spacing_classification.append("Narrow")
    # print(spacing_classification)
    return spacing_classification

def conclude_overall_spacing(spacing_classification):
    wide_count = spacing_classification.count('Wide')
    narrow_count = spacing_classification.count('Narrow')
    
    if wide_count >= narrow_count:
        return 'Wide'
    else:
        return 'Narrow'

# Constants for spacing classification
WIDE_THRESHOLD = 2 

def check_left_margin(image_path):
    # Load image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply thresholding
    _, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the leftmost contour
    leftmost_contour = min(contours, key=lambda x: cv2.boundingRect(x)[0])

    # Calculate the left margin
    left_margin = cv2.boundingRect(leftmost_contour)[0]

    return left_margin

def check_right_margin(image_path):
    # Load image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply thresholding
    _, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the rightmost contour
    rightmost_contour = max(contours, key=lambda x: cv2.boundingRect(x)[0])

    # Calculate the right margin
    right_margin = image.shape[1] - (cv2.boundingRect(rightmost_contour)[0] + cv2.boundingRect(rightmost_contour)[2])

    return right_margin

def analyze_slanting(contours, is_left_handed=False):
    # Calculate the bounding box of all contours
    x_min = min([cv2.boundingRect(contour)[0] for contour in contours])
    x_max = max([cv2.boundingRect(contour)[0] + cv2.boundingRect(contour)[2] for contour in contours])
    y_min = min([cv2.boundingRect(contour)[1] for contour in contours])
    y_max = max([cv2.boundingRect(contour)[1] + cv2.boundingRect(contour)[3] for contour in contours])

    # Calculate the angle of slant
    if x_max - x_min != 0:
        slant_angle = (y_max - y_min) / (x_max - x_min)
    else:
        slant_angle = 0

    # Determine the direction of slant based on the angle
    if slant_angle > 0:
        if is_left_handed:
            return 'left'
        else:
            return 'right'
    elif slant_angle < 0:
        if is_left_handed:
            return 'right'
        else:
            return 'left'
    else:
        return 'upright'
def analyze_pressure(image):
    # You can implement your pressure analysis logic here
    # For demonstration, let's assume that heavy pressure corresponds to darker ink
    # and light pressure corresponds to lighter ink
    average_pixel_intensity = image.mean()
    # print(average_pixel_intensity)
    if average_pixel_intensity > 240:
        return 'light'
    else:
        return 'heavy'
    
def analyze_handwriting(image_path, output_text):
    # Load image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply thresholding
    _, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Analyze handwriting features
    features = {'narrow_e': False, 'high_dot_i': False, 'large_I': False, 'long_t_cross': False, 'open_o': False}

    # Narrow loop in lowercase "e"
    for contour in contours:
        if cv2.contourArea(contour) > 100:  # Exclude very small contours
            x, y, w, h = cv2.boundingRect(contour)
            if w < 0.5 * h:  # Check if the width is less than half the height
                features['narrow_e'] = True
                break

    # Dot on lowercase "i"
    for contour in contours:
        if cv2.contourArea(contour) > 100:  # Exclude very small contours
            x, y, w, h = cv2.boundingRect(contour)
            if w < 0.5 * h:  # Check if the width is less than half the height
                if y < h / 2:  # Check if the dot is positioned above the center
                    features['high_dot_i'] = True
                    break

    # Capital "I" size
    for contour in contours:
        if cv2.contourArea(contour) > 100:  # Exclude very small contours
            x, y, w, h = cv2.boundingRect(contour)
            if w > 2 * h:  # Check if the width is significantly larger than the height
                features['large_I'] = True
                break

    # "t" crossing length
    for contour in contours:
        if cv2.contourArea(contour) > 100:  # Exclude very small contours
            x, y, w, h = cv2.boundingRect(contour)
            if h > w:  # Check if the height is larger than the width
                features['long_t_cross'] = True
                break

    # "o" openness
    for contour in contours:
        if cv2.contourArea(contour) > 100:  # Exclude very small contours
            x, y, w, h = cv2.boundingRect(contour)
            if abs(w - h) > 0.2 * max(w, h):  # Check if the width and height are significantly different
                features['open_o'] = True
                break
    
    # Print personality traits based on features
    if features['narrow_e']:
        output_text.insert(tk.END, "📌 Skepticism or suspicion towards others\n")
    else:
        output_text.insert(tk.END, "📌 Open to new people and experiences\n")

    if features['high_dot_i']:
        output_text.insert(tk.END, "📌 Creative and free-spirited\n")
    else:
        output_text.insert(tk.END, "📌 Structured and detail-oriented\n")

    if features['large_I']:
        output_text.insert(tk.END, "📌 Cocky and overly confident\n")
    else:
        output_text.insert(tk.END, "📌 Content with who they are\n")

    if features['long_t_cross']:
        output_text.insert(tk.END, "📌 Enthusiastic and determined\n")
    else:
        output_text.insert(tk.END, "📌 Apathetic and lacking determination\n")

    if features['open_o']:
        output_text.insert(tk.END, "📌 Expressive and willing to share secrets\n")
    else:
        output_text.insert(tk.END, "📌 Treasures privacy and tends toward introversion\n")

    # Loopy and rounded letters
    for contour in contours:
        if cv2.contourArea(contour) > 100:  # Exclude very small contours
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            if len(approx) > 10:  # Check if the contour is loopy and rounded
                features['loopy_rounded'] = True
                break

    # Pointed letters
    for contour in contours:
        if cv2.contourArea(contour) > 100:  # Exclude very small contours
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            if len(approx) < 10:  # Check if the contour is pointed
                features['pointed'] = True
                break

    # Connected letters
    if len(contours) > 1:
        features['connected'] = True

    # Print personality traits based on features
    if features['loopy_rounded']:
        output_text.insert(tk.END, "📌 Imaginative, artistic, and creative\n")
    elif features['pointed']:
        output_text.insert(tk.END, "📌 Aggression, intelligence, and intensity\n")

    if features['connected']:
        output_text.insert(tk.END, "📌 Orderly and methodological\n")

    is_left_handed = False
    slant_direction = analyze_slanting(contours, is_left_handed)
    if slant_direction == 'right':
        output_text.insert(tk.END, "📌 Open and enjoy meeting new people\n")
    elif slant_direction == 'left':
        output_text.insert(tk.END, "📌 Tend to keep to yourself\n")
    else:
        output_text.insert(tk.END, "📌 Logical and practical\n")

    pressure_intensity = analyze_pressure(image)
    if pressure_intensity == 'heavy':
        output_text.insert(tk.END, "📌 Good with commitment, but can be rigid and volatile\n")
    elif pressure_intensity == 'light':
        output_text.insert(tk.END, "📌 Compassionate and sensitive, but may also lack energy and liveliness\n")


def extract_text_from_image(output_text,image_path):
    # image_path = "my.png"
    output_text.delete(1.0, tk.END)  # Clear the previous content
    # output_text.insert(tk.END, "You chose option 2: Image to Text Conversion\n")

    # Read the image using OpenCV
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to preprocess the image
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Use pytesseract to do OCR on the preprocessed image
    text = pytesseract.image_to_string(thresh)
    output_text.insert(tk.END, text)

def analyze_personality(output_text,filename):
    # filename = "my.png"
    output_text.delete(1.0, tk.END)  # Clear the previous content
    output_text.insert(tk.END, "Personality Analysis:\n\n")

    sizes = classify_letter_size(filename)
    overall_size = conclude_overall_size(sizes)
    if overall_size =="Large":
        output_text.insert(tk.END,"📌 Outgoing, people-oriented, outspoken\n")
    elif overall_size=="Medium":
        output_text.insert(tk.END,"📌 Shy, studious,concentrated,meticulous\n")
    else: 
        output_text.insert(tk.END,"📌 Well-adjusted and adaptable\n")
   

    spacing_classification = classify_letter_spacing(filename)
    overall_spacing = conclude_overall_spacing(spacing_classification)
    if overall_spacing =="Narrow":
        output_text.insert(tk.END, "📌 Enjoy freedom, dont like to be crowded\n")
    else:
        output_text.insert(tk.END, "📌 Dislikes being alone, tend to crowd people and be intrusive\n")

    left_margin = check_left_margin(filename)
    right_margin = check_right_margin(filename)
    if left_margin > right_margin:
        output_text.insert(tk.END, "📌 Tend to live in the past & have a hard time letting go of things\n")
    elif right_margin > left_margin:
        output_text.insert(tk.END, "📌 Fear the unknown, constantly worry about the future\n")
    else:
        output_text.insert(tk.END, "📌 Can't sit still or relax, mind is constantly running\n")

    handwriting_features = analyze_handwriting(filename,output_text)
    # output_text.insert(tk.END, "{}\n".format(handwriting_features))

def fullscreen_window(window):
    window.attributes('-fullscreen', True)

def exit_fullscreen(window):
    window.attributes('-fullscreen', False)

def main():
    root = tk.Tk()
    root.title("Handwritten Text Analysis")
    fullscreen_window(root)

    frame = tk.Frame(root)
    frame.pack(pady=20)

    def choose_file():
        global selected_filename
        selected_filename = filedialog.askopenfilename(initialdir="/", title="Select Image File", filetypes=(("Image Files", "*.png *.jpg *.jpeg"),))
        if selected_filename:
            selected_file_label.config(text="Selected file: {}".format(selected_filename))
            button_analyze.config(state=tk.NORMAL)
            button_convert.config(state=tk.NORMAL)
        else:
            selected_file_label.config(text="Please select file")
            button_analyze.config(state=tk.DISABLED)
            button_convert.config(state=tk.DISABLED)
            button_analyze.config(disabledforeground="black")
            button_convert.config(disabledforeground="black")
            
            
    title_label = tk.Label(frame, text="Handwriting Analysis and Text Conversion", font=("Helvetica", 16), fg="white")
    title_label.grid(row=0, columnspan=3, pady=10)
    
    button_choose_file = tk.Button(frame, text="Choose File", command=choose_file, padx=10, pady=5)
    button_choose_file.grid(row=1, columnspan=2, padx=10, pady=5)

    button_analyze = tk.Button(frame, text="Personality Analysis", command=lambda: analyze_personality(output_text, selected_filename), padx=10, pady=5, state=tk.DISABLED,disabledforeground="black")
    button_analyze.grid(row=2, column=0, padx=10, pady=5)

    button_convert = tk.Button(frame, text="Image to Text Conversion", command=lambda: extract_text_from_image(output_text, selected_filename), padx=10, pady=5, state=tk.DISABLED,disabledforeground="black")
    button_convert.grid(row=2, column=1, padx=10, pady=5)

    selected_file_label = tk.Label(frame, text="", fg="white")
    selected_file_label.grid(row=3, columnspan=2, padx=10, pady=5)

    output_text = tk.Text(root, height=20, width=100, fg="white", font=("Times New Roman", 20))
    output_text.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    main()