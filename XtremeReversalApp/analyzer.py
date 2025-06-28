
from PIL import Image
import pytesseract

def analyze_screenshot(image_path: str) -> str:
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)

    if "Trigger Base Sell" in text:
        if "Reversal Buffer Buy" in text:
            if "40+" in text and "TB Buy" not in text:
                return "Buy Setup Forming (Reversal Buffer)"
            else:
                return "Invalid"
        else:
            return "Sell Signal (Confirmed)"
    elif "Trigger Base Buy" in text:
        if "Reversal Buffer Sell" in text:
            if "40+" in text and "TB Sell" not in text:
                return "Sell Setup Forming (Reversal Buffer)"
            else:
                return "Invalid"
        else:
            return "Buy Signal (Confirmed)"
    elif "M4 High" in text and "Top BB" in text:
        return "Sell Setup Forming (M4 Out of Top BB)"
    elif "M4 Low" in text and "Low BB" in text:
        return "Buy Setup Forming (M4 Out of Low BB)"
    else:
        return "Invalid"
