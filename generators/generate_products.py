import random
from datetime import datetime

import pandas as pd

from config import (
    PRODUCTS,
    PRODUCT_VENDORS,
    DEFAULT_TAX_PERCENTAGE
)


def generate_products():
    """
    Generate hotel products/services master data.

    Returns:
        pandas.DataFrame
    """

    products = []

    current_timestamp = datetime.now()

    for index, (product_name, category, unit_price) in enumerate(PRODUCTS, start=1):

        tax_percentage = DEFAULT_TAX_PERCENTAGE

        # Simulate procurement cost
        cost_price = round(
            unit_price * random.uniform(0.45, 0.75),
            2
        )

        vendor = random.choice(PRODUCT_VENDORS)

        # 98% active products
        is_active = random.random() < 0.98

        product = {

            "product_id": f"PROD{index:04}",

            "product_name": product_name,

            "category": category,

            "unit_price": round(unit_price, 2),

            "tax_percentage": tax_percentage,

            "cost_price": cost_price,

            "vendor": vendor,

            "is_active": is_active,

            "created_at": current_timestamp,

            "updated_at": current_timestamp

        }

        products.append(product)

    return pd.DataFrame(products)