import os
import re
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize the OpenAI client with the API key from environment variables
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Predefined categories for receipt classification
CATEGORIES = ["Meals", "Transport", "Lodging", "Office Supplies",
              "Entertainment", "Other"]

def check_price(price):
    """Sanitizes the price string to ensure it is a valid float.

    Removes currency symbols (like '$') and converts the string to a float.
    If conversion fails or input is None, returns None.

    Args:
        price (str or float or None): The price value returned by the model.

    Returns:
        float or None: The cleaned float value, or None if conversion fails.
    """
    if price is None:
        return None
        
    # If it's already a number, return it directly
    if isinstance(price, (int, float)):
        return float(price)
        
    # Remove '$' and whitespace
    cleaned_price = str(price).replace("$", "").strip()
    
    try:
        return float(cleaned_price)
    except ValueError:
        return None

def extract_receipt_info(image_b64):
    """Extracts receipt details from a base64-encoded image using OpenAI API.

    Constructs a prompt with predefined categories and sends the image to a
    language model to parse specific fields (date, amount, vendor, category).
    Applies sanity checks to the amount field.

    Args:
        image_b64 (str): The receipt image encoded as a base64 string.

    Returns:
        dict: A dictionary containing the extracted fields: 'date', 'amount',
            'vendor', and 'category'. Returns keys with null values if
            extraction fails for specific fields.
    """
    # Construct the extraction prompt with the allowed categories
    prompt = f"""
You are an information extraction system.
Extract ONLY the following fields from the receipt image:

date: the receipt date as a string
amount: the total amount paid as it appears on the receipt
vendor: the merchant or vendor name
category: one of [{", ".join(CATEGORIES)}]

Return EXACTLY one JSON object with these four keys and NOTHING ELSE.
Do not include explanations, comments, or formatting.
Do not wrap the JSON in markdown.
If a field cannot be determined, use null.

The output must be valid JSON.
"""
    # Send the request to the model including text prompt and image
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        seed=43,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_b64}"
                        }
                    }
                ]
            }
        ]
    )
    # Parse the JSON content from the response
    data = json.loads(response.choices[0].message.content)

    # Sanity check: clean the amount field
    if "amount" in data:
        data["amount"] = check_price(data["amount"])

    return data