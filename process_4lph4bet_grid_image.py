import cv2
import numpy as np
from PIL import Image, ImageDraw
import os
from datetime import datetime

# Constants for grid cell padding
top_padding = 50
left_padding = 80
right_padding = 120
bottom_padding = 40
num_rows = 10
num_cols = 9

# Threshold for setting background transparency
transparency_threshold = 200

# Function to resize and save intermediate images
def save_resized_image(img, path, size=(1024, 1024)):
    resized_img = cv2.resize(img, size)
    cv2.imwrite(path, resized_img)

# Function to convert white pixels to transparency with gradient
def white_to_transparency_gradient(img, transparency_threshold):
    x = np.asarray(img.convert('RGBA')).copy()
    avg_intensity = x[:, :, :3].mean(axis=2)
    transparency = (255 - avg_intensity).astype(np.uint8)
    transparency[transparency < transparency_threshold] = 0
    x[:, :, 3] = transparency
    return Image.fromarray(x)

# Function to check if two rectangles overlap with padding
def rectangles_overlap(r1, r2, padding):
    (x1, y1, w1, h1) = r1
    (x2, y2, w2, h2) = r2
    return not (x1 + w1 + padding < x2 or x2 + w2 + padding < x1 or
                y1 + h1 + padding < y2 or y2 + h2 + padding < y1)

# Ask user for input image path
input_path = input("Enter the absolute path to your grid image: ").strip('"')

# Load the image
img = cv2.imread(input_path)

# Check if the image was loaded successfully
if img is None:
    raise FileNotFoundError(f"Image not found at {input_path}")

# Extract the filename from the input path
filename = os.path.basename(input_path)
filename_without_extension = os.path.splitext(filename)[0]

# Prepare directory for intermediate outputs
output_dir = os.path.join(os.path.dirname(input_path), f'{filename_without_extension}_intermediate_outputs')
os.makedirs(output_dir, exist_ok=True)

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Save intermediate edges image
edges = cv2.Canny(gray, 50, 150)  # Adjusted thresholds
save_resized_image(edges, os.path.join(output_dir, 'edges_resized.png'))

# Find contours
contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # Using RETR_TREE

# Sort contours by their area in descending order
contours = sorted(contours, key=cv2.contourArea, reverse=True)

# Save intermediate contours image
img_with_contours = img.copy()
cv2.drawContours(img_with_contours, contours, -1, (0, 255, 0), 2)
save_resized_image(img_with_contours, os.path.join(output_dir, 'contours_resized.png'))

# Calculate grid cell dimensions
cell_width = (img.shape[1] - left_padding - right_padding) // num_cols
cell_height = (img.shape[0] - top_padding - bottom_padding) // num_rows

# Function to calculate grid cell centers with padding
def calculate_grid_centers():
    grid_centers = {}
    for row in range(num_rows):
        for col in range(num_cols):
            center_x = left_padding + col * cell_width + cell_width // 2
            center_y = top_padding + row * cell_height + cell_height // 2
            grid_centers[(row, col)] = (center_x, center_y)
    return grid_centers

# Calculate grid cell centers
grid_centers = calculate_grid_centers()

# Assign contours to grid cells based on proximity to center
contours_assigned = {key: [] for key in grid_centers.keys()}
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    contour_center_x = x + w // 2
    contour_center_y = y + h // 2

    min_distance = float('inf')
    closest_cell = None
    for grid_cell, (center_x, center_y) in grid_centers.items():
        distance = np.sqrt((contour_center_x - center_x) ** 2 + (contour_center_y - center_y) ** 2)
        if distance < min_distance:
            min_distance = distance
            closest_cell = grid_cell

    contours_assigned[closest_cell].append(contour)

# Merge contours in each grid cell
merged_contours = []
for grid_cell, cell_contours in contours_assigned.items():
    if len(cell_contours) == 0:
        continue

    if len(cell_contours) == 1:
        merged_contours.append(cell_contours[0])
        continue

    # Merge contours in this cell
    merged_contour = np.concatenate(cell_contours)
    merged_contours.append(merged_contour)

# Save intermediate merged contours image
for idx, contour in enumerate(merged_contours):
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imwrite(os.path.join(output_dir, 'output_with_rectangles.png'), img)

# Save sorted glyph images
for idx, contour in enumerate(merged_contours):
    x, y, w, h = cv2.boundingRect(contour)
    roi = img[y:y+h, x:x+w]
    roi_inverted = cv2.bitwise_not(roi)
    bordered_image = cv2.copyMakeBorder(roi_inverted, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    bordered_image_rgb = cv2.cvtColor(bordered_image, cv2.COLOR_BGR2RGB)
    bordered_pil_image = Image.fromarray(bordered_image_rgb)
    bordered_pil_image_transparent = white_to_transparency_gradient(bordered_pil_image, transparency_threshold)
    bordered_pil_image_transparent.save(os.path.join(output_dir, f'letter_{idx}.png'))

# Load the template image
template_path = '4lph4bet_calligraphr_template.png'
template = Image.open(template_path)

# Define the coordinates for each glyph
glyph_centers = {
    'letter_0': (335, 675),
    'letter_1': (820, 675),
    'letter_2': (1300, 670),
    'letter_3': (1780, 570),
    'letter_4': (2250, 695),
    'letter_5': (2730, 695),
    'letter_6': (3225, 770),
    'letter_7': (340, 1300),
    'letter_8': (820, 1380),
    'letter_9': (1300, 1285),
    'letter_10': (1785, 1285),
    'letter_11': (2270, 1285),
    'letter_12': (2735, 1285),
    'letter_13': (3220, 1285),
    'letter_14': (335, 1900),
    'letter_15': (815, 1900),
    'letter_16': (1300, 1900),
    'letter_17': (1780, 1900),
    'letter_18': (2260, 1900),
    'letter_19': (2745, 1900),
    'letter_20': (3220, 1930),
    'letter_21': (340, 2535),
    'letter_22': (820, 2535),
    'letter_23': (1300, 2535),
    'letter_24': (1780, 2535),
    'letter_25': (2260, 2535),
    'letter_26': (2745, 2535),
    'letter_27': (3220, 2535),
    'letter_28': (3700, 2535),
    'letter_29': (4190, 2535),
    'letter_30': (4660, 2535),
    'letter_31': (340, 3155),
    'letter_32': (820, 3155),
    'letter_33': (1300, 3155),
    'letter_34': (1780, 3155),
    'letter_35': (2260, 3155),
    'letter_36': (2745, 3155),
    'letter_37': (3220, 3155),
    'letter_38': (3700, 3155),
    'letter_39': (4190, 3155),
    'letter_40': (4660, 3155),
    'letter_41': (340, 3775),
    'letter_42': (820, 3775),
    'letter_43': (1300, 3775),
    'letter_44': (1780, 3775),
    'letter_45': (2260, 3775),
    'letter_46': (2745, 3775),
    'letter_47': (3220, 3775),
    'letter_48': (3700, 3775),
    'letter_49': (4190, 3775),
    'letter_50': (4660, 3775),
    'letter_51': (340, 4430),
    'letter_52': (820, 4400),
    'letter_53': (1300, 4430),
    'letter_54': (1780, 4400),
    'letter_55': (2260, 4460),
    'letter_56': (2745, 4400),
    'letter_57': (3220, 4400),
    'letter_58': (3700, 4460),
    'letter_59': (4190, 4400),
    'letter_60': (4660, 4400),
    'letter_61': (340, 5050),
    'letter_62': (820, 5050),
    'letter_63': (1300, 5050),
    'letter_64': (1780, 5075),
    'letter_65': (2260, 5075),
    'letter_66': (2745, 5050),
    'letter_67': (3220, 5050),
    'letter_68': (3700, 5035),
    'letter_69': (4190, 5050),
    'letter_70': (4660, 5050),
    'letter_71': (340, 5675),
    'letter_72': (820, 5675),
    'letter_73': (1300, 5700),
    'letter_74': (1780, 5675),
    'letter_75': (2260, 5675),
    'letter_76': (2745, 5675),
    'letter_77': (3220, 5635),
    'letter_78': (3700, 5635),
    'letter_79': (4190, 5635),
    'letter_80': (4660, 5650),
    'letter_81': (340, 6280),
    'letter_82': (820, 6280),
    'letter_83': (1300, 6280),
    'letter_84': (1780, 6200),
    'letter_85': (2260, 6275),
    'letter_86': (2745, 6275),
    'letter_87': (3220, 6275),
}

# Create a new image to paste the processed glyphs
result_image = template.copy()

# Sort glyph centers by index
sorted_glyph_centers = sorted(glyph_centers.items(), key=lambda x: int(x[0].split('_')[1]))

# Paste each glyph into the template in the correct order
for idx, (letter_key, (center_x, center_y)) in enumerate(sorted_glyph_centers):
    glyph_image_path = os.path.join(output_dir, f'letter_{idx}.png')
    if os.path.exists(glyph_image_path):
        glyph_image = Image.open(glyph_image_path)
        glyph_w, glyph_h = glyph_image.size
        position = (center_x - glyph_w // 2, center_y - glyph_h // 2)
        result_image.paste(glyph_image, position, glyph_image)

# Save the final result with a timestamp
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
final_output_path = os.path.join(os.path.dirname(input_path), f'{filename_without_extension}_processed_grid_{timestamp}.png')
result_image.save(final_output_path)

print(f"Processed image saved as {final_output_path}")
