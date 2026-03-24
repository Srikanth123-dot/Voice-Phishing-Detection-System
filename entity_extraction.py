import re

def extract_entities(text):
    entities = {}

    # Customer ID: 6 to 12 digit numbers
    customer_ids = re.findall(r'\b\d{6,12}\b', text)

    # Phone numbers: exactly 10 digits
    phone_numbers = re.findall(r'\b\d{10}\b', text)

    # Amounts: ₹2500 or 2500
    amounts = re.findall(r'₹?\s?\d{2,7}', text)

    if customer_ids:
        entities["Customer IDs"] = customer_ids

    if phone_numbers:
        entities["Phone Numbers"] = phone_numbers

    if amounts:
        entities["Amounts"] = amounts

    return entities
