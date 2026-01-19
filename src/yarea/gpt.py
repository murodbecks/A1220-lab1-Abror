import os
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

def extract_receipt_info(image_b64):
    """Extracts receipt details from a base64-encoded image using OpenAI API.

    Constructs a prompt with predefined categories and sends the image to a
    language model to parse specific fields (date, amount, vendor, category).

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
    # Parse and return the JSON content from the response
    return json.loads(response.choices[0].message.content)