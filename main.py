from pathlib import Path

from generators.generate_bookings import generate_bookings
from generators.generate_customers import generate_customers
from generators.generate_hotels import generate_hotels
from generators.generate_order_items import generate_order_items
from generators.generate_payments import generate_payments
from generators.generate_products import generate_products
from generators.generate_reviews import generate_reviews


def save_dataframe(df, filename: str) -> None:
    """
    Save dataframe as CSV.
    """

    output_dir = Path("data")
    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    filepath = output_dir / filename

    df.to_csv(
        filepath,
        index=False
    )

    print(f"Saved {filepath}")


def print_summary(
    customers,
    hotels,
    products,
    bookings,
    payments,
    reviews,
    order_items
):

    print("\n")
    print("=" * 60)
    print("DATA GENERATION SUMMARY")
    print("=" * 60)

    print(f"Customers    : {len(customers):,}")
    print(f"Hotels       : {len(hotels):,}")
    print(f"Products     : {len(products):,}")
    print(f"Bookings     : {len(bookings):,}")
    print(f"Payments     : {len(payments):,}")
    print(f"Reviews      : {len(reviews):,}")
    print(f"Order Items  : {len(order_items):,}")

    print("=" * 60)


def main():

    print("=" * 60)
    print("HOTEL BOOKING ANALYTICS DATA GENERATOR")
    print("=" * 60)

    # -------------------------------------------------------------
    # Master Data
    # -------------------------------------------------------------

    customers_df = generate_customers()

    hotels_df = generate_hotels()

    products_df = generate_products()

    # -------------------------------------------------------------
    # Transaction Data
    # -------------------------------------------------------------

    bookings_df = generate_bookings(
        customers_df,
        hotels_df
    )

    payments_df = generate_payments(
        bookings_df,
        customers_df
    )

    reviews_df = generate_reviews(
        bookings_df
    )

    order_items_df = generate_order_items(
        bookings_df,
        products_df
    )

    # -------------------------------------------------------------
    # Export CSVs
    # -------------------------------------------------------------

    save_dataframe(
        customers_df,
        "customers.csv"
    )

    save_dataframe(
        hotels_df,
        "hotels.csv"
    )

    save_dataframe(
        products_df,
        "products.csv"
    )

    save_dataframe(
        bookings_df,
        "bookings.csv"
    )

    save_dataframe(
        payments_df,
        "payments.csv"
    )

    save_dataframe(
        reviews_df,
        "reviews.csv"
    )

    save_dataframe(
        order_items_df,
        "order_items.csv"
    )

    # -------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------

    print_summary(
        customers_df,
        hotels_df,
        products_df,
        bookings_df,
        payments_df,
        reviews_df,
        order_items_df
    )

    print("\nData generation completed successfully.")


if __name__ == "__main__":
    main()