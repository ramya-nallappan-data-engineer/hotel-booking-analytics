import random
from datetime import datetime
from typing import Any

import pandas as pd

def build_product_lookup(
    products_df: pd.DataFrame
) -> dict[str, dict[str, Any]]:
    """
    Build a lookup dictionary for products.
    """

    return (
        products_df
        .set_index("product_id")
        .to_dict("index")
    )


def generate_order_item_id(
    order_item_number: int
) -> str:
    """
    Generate order item ID.
    """

    return f"OI{order_item_number:06d}"

def build_order_item_record(
    order_item_number: int,
    booking: dict[str, Any],
    product_id: str,
    product: dict[str, Any]
) -> dict[str, Any]:
    """
    Build a single order item record.
    """

    quantity = random.randint(1, 3)

    unit_price = product["cost_price"]

    total_price = round(
        quantity * unit_price,
        2
    )

    audit_timestamp = datetime.now()

    return {

        "order_item_id":
            generate_order_item_id(
                order_item_number
            ),

        "booking_id":
            booking["booking_id"],

        "customer_id":
            booking["customer_id"],

        "hotel_id":
            booking["hotel_id"],

        "product_id": product_id,

        "quantity":
            quantity,

        "unit_price":
            unit_price,

        "total_price":
            total_price,

        "created_at":
            audit_timestamp

    }

def generate_order_items(
    bookings_df: pd.DataFrame,
    products_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Generate ancillary product purchases
    for hotel bookings.
    """

    print("\nStarting Order Item Generation...")

    product_lookup = build_product_lookup(
        products_df
    )

    product_ids = list(
        product_lookup.keys()
    )

    order_item_records = []

    order_item_number = 1

    for _, booking in bookings_df.iterrows():

        item_count = random.choices(
            population=[0, 1, 2, 3],
            weights=[15, 50, 25, 10],
            k=1
        )[0]

        if item_count == 0:
            continue

        selected_products = random.sample(
            product_ids,
            k=min(item_count, len(product_ids))
        )

        for product_id in selected_products:

            product = product_lookup[
                product_id
            ]

            order_item_records.append(

                build_order_item_record(
                    order_item_number=order_item_number,
                    booking=booking.to_dict(),
                    product_id=product_id,
                    product=product
                )

            )

            order_item_number += 1

    order_items_df = pd.DataFrame(
        order_item_records
    )

    if not order_items_df.empty:

        order_items_df["created_at"] = (
            pd.to_datetime(
                order_items_df["created_at"]
            )
        )

        numeric_columns = [
            "quantity",
            "unit_price",
            "total_price"
        ]

        for column in numeric_columns:

            order_items_df[column] = pd.to_numeric(
                order_items_df[column]
            )

        order_items_df = (

            order_items_df

            .sort_values(
                by=[
                    "booking_id",
                    "order_item_id"
                ]
            )

            .reset_index(
                drop=True
            )

        )

    print(
        f"Generated {len(order_items_df):,} order items."
    )

    return order_items_df