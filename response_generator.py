def generate_response(sentiment, entities, product):

    name = entities.get("customer_name")
    product = entities.get("product") if entities.get("product") else product

    greeting = (
        f"Olá {name}!\n\n"
        if name
        else "Olá!\n\n"
    )

    response = greeting

    if entities.get("liked_product"):
        response += (
            f"Ficamos felizes que você tenha gostado do {product}. "
        )

    if entities.get("delivery_issue"):
        response += (
            "Pedimos desculpas pela demora na entrega. "
        )

    if sentiment == "POSITIVE":
        response += (
            "É muito bom saber que sua experiência foi positiva. "
        )
    else:
        response += (
            "Lamentamos que sua experiência não tenha sido a ideal. "
            "Nossa equipe está trabalhando para melhorar nossos serviços. "
        )

    response += "\n\nObrigado por compartilhar sua experiência."

    return response