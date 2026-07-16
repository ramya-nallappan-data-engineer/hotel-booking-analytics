-- Dimension table storing customer information
CREATE TABLE customers(
    customer_id VARCHAR PRIMARY KEY,
    customer_name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    city VARCHAR NOT NULL,
    country VARCHAR NOT NULL,
    signup_date DATE NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
-- Dimension table storing hotel information
CREATE TABLE hotels (
    hotel_id VARCHAR PRIMARY KEY,
    hotel_name VARCHAR NOT NULL,
    city VARCHAR NOT NULL,
    country VARCHAR NOT NULL,
    star_rating INTEGER CHECK (star_rating BETWEEN 1 AND 5),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
-- Dimension table storing product information
CREATE TABLE products (
    product_id VARCHAR PRIMARY KEY,
    product_name VARCHAR NOT NULL,
    category VARCHAR,
    price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
-- Fact table containing hotel booking transactions
CREATE TABLE bookings (
    booking_id VARCHAR PRIMARY KEY,
    customer_id VARCHAR NOT NULL,
    hotel_id VARCHAR NOT NULL,
    booking_date DATE NOT NULL,
    checkin_date DATE,
    checkout_date DATE,
    amount DECIMAL(10,2) NOT NULL,
    booking_status VARCHAR, -- VALUES: CONFIRMED, CANCELLED, PENDING
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY(customer_id)
        REFERENCES customers(customer_id),
    FOREIGN KEY(hotel_id)
        REFERENCES hotels(hotel_id)
);
-- Fact table containing payment transactions
CREATE TABLE payments (
    payment_id VARCHAR PRIMARY KEY,
    booking_id VARCHAR NOT NULL,
    payment_date DATE,
    payment_method VARCHAR, -- CARD, UPI, NETBANKING, WALLET
    payment_status VARCHAR, -- SUCCESS, FAILED, PENDING
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY(booking_id)
        REFERENCES bookings(booking_id)
);
-- Fact table containing order items transactions
CREATE TABLE order_items (
    booking_id VARCHAR NOT NULL,
    product_id VARCHAR NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    PRIMARY KEY(booking_id, product_id),
    FOREIGN KEY(booking_id)
        REFERENCES bookings(booking_id),
    FOREIGN KEY(product_id)
        REFERENCES products(product_id)
);
-- Fact table containing reviews and comments
CREATE TABLE reviews (
    review_id VARCHAR PRIMARY KEY,
    booking_id VARCHAR NOT NULL,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    review_date DATE,
    comments VARCHAR,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY(booking_id)
        REFERENCES bookings(booking_id)
);