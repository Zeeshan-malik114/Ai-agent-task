def get_invoice(contact: str):
    """
    Mock function to retrieve latest invoice for a contact.
    """
    return {
        "contact": contact,
        "invoice_id": "INV-12345",
        "amount": "$100",
        "details": "Invoice for September subscription."
    }


def get_rate_plans(contact: str):
    """
    Mock function to retrieve available rate plans.
    """
    return [
        {"plan": "Basic", "price": "$10", "features": "Email support, 10GB storage"},
        {"plan": "Premium", "price": "$25", "features": "Priority support, 100GB storage"}
    ]
