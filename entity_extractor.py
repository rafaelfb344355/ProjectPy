import re

def extract_entities(text):

    entities = {
        "customer_name": None,
        "product": None,
        "delivery_issue": False,
        "liked_product": False
    }

    name_patterns = [
        r"meu nome é ([A-Za-zÀ-ÿ]+)",
        r"sou ([A-Za-zÀ-ÿ]+)",
        r"Me chamo ([A-Za-zÀ-ÿ]+)",
        r"eu sou ([A-Za-zÀ-ÿ]+)"
    ]

    for pattern in name_patterns:
        match = re.search(pattern, text.lower())
        if match:
            entities["customer_name"] = match.group(1).title()

    delivery_words = [
        "entrega demorou",
        "atraso",
        "atrasada",
        "demorou"
    ]

    entities["delivery_issue"] = any(
        word in text.lower()
        for word in delivery_words
    )

    positive_words = [
        "eu gostei",
        "é excelente",
        "é ótimo",
        "é perfeito"
    ]

    entities["liked_product"] = any(
        word in text.lower()
        for word in positive_words
    )

    return entities
