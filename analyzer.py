import io
import cv2
import numpy as np
from PIL import Image

def detect_line_color_ratio(image_np, lower, upper):
    mask = cv2.inRange(image_np, np.array(lower), np.array(upper))
    ratio = cv2.countNonZero(mask) / (image_np.shape[0] * image_np.shape[1])
    return ratio

def analyze_chart(uploaded_file):
    image_bytes = uploaded_file.file.read()
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image_np = np.array(img)
    image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # Define color ranges in BGR
    m4_high_red = ([0, 0, 150], [80, 80, 255])         # Red for M4 High
    m4_low_magenta = ([150, 0, 150], [255, 80, 255])   # Magenta for M4 Low
    bb_blue = ([150, 100, 0], [255, 180, 100])         # Blue for BB

    # Visual indicators (placeholder ratios)
    m4_high_ratio = detect_line_color_ratio(image_np, *m4_high_red)
    m4_low_ratio = detect_line_color_ratio(image_np, *m4_low_magenta)
    bb_ratio = detect_line_color_ratio(image_np, *bb_blue)

    # Placeholder bar count estimation
    bar_count = int(image_np.shape[1] / 10)  # assume each candle is ~10px wide

    # Simulated SOP decision logic
    if bar_count >= 40 and (m4_high_ratio > 0.005 or m4_low_ratio > 0.005):
        return "Buy Signal (Confirmed)" if m4_low_ratio > m4_high_ratio else "Sell Signal (Confirmed)"
    elif bar_count >= 30:
        if m4_high_ratio > 0.005 or m4_low_ratio > 0.005:
            return "Setup Forming"
    return "Invalid"