-- ==========================================================
-- HOTEL BOOKING ANALYTICS DATABASE
-- ==========================================================

-- Drop existing tables (child tables first)
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS hotels;
DROP TABLE IF EXISTS customers;

-- ==========================================================
-- CUSTOMERS
-- ==========================================================

CREATE TABLE customers (

    customer_id             VARCHAR PRIMARY KEY,

    first_name              VARCHAR,
    last_name               VARCHAR,
    gender                  VARCHAR,
    age                     INTEGER,

    email                   VARCHAR,
    phone_number            VARCHAR,

    city                    VARCHAR,
    state                   VARCHAR,
    country                 VARCHAR,

    traveler_type           VARCHAR,
    loyalty_tier            VARCHAR,

    registration_date       DATE,

    created_at              TIMESTAMP,
    updated_at              TIMESTAMP
);

-- ==========================================================
-- HOTELS
-- ==========================================================

CREATE TABLE hotels (

    hotel_id                VARCHAR PRIMARY KEY,

    hotel_name              VARCHAR,

    city                    VARCHAR,
    state                   VARCHAR,
    country                 VARCHAR,

    hotel_type              VARCHAR,
    star_rating             INTEGER,

    room_capacity           INTEGER,

    created_at              TIMESTAMP,
    updated_at              TIMESTAMP
);

-- ==========================================================
-- PRODUCTS
-- ==========================================================

CREATE TABLE products (

    product_id              VARCHAR PRIMARY KEY,

    product_name            VARCHAR,
    category                VARCHAR,

    price                   DECIMAL(10,2),

    created_at              TIMESTAMP,
    updated_at              TIMESTAMP
);

-- ==========================================================
-- BOOKINGS
-- ==========================================================

CREATE TABLE bookings (

    booking_id              VARCHAR PRIMARY KEY,

    customer_id             VARCHAR,

    hotel_id                VARCHAR,

    booking_date            DATE,
    checkin_date            DATE,
    checkout_date           DATE,

    booking_status          VARCHAR,

    room_type               VARCHAR,

    booking_source          VARCHAR,

    nights                  INTEGER,
    guests                  INTEGER,

    gross_amount            DECIMAL(12,2),
    discount_amount         DECIMAL(12,2),
    tax_amount              DECIMAL(12,2),
    net_amount              DECIMAL(12,2),

    created_at              TIMESTAMP,
    updated_at              TIMESTAMP
);

-- ==========================================================
-- PAYMENTS
-- ==========================================================

CREATE TABLE payments (

    payment_id              VARCHAR PRIMARY KEY,

    booking_id              VARCHAR,

    customer_id             VARCHAR,

    payment_date            DATE,

    payment_method          VARCHAR,
    payment_provider        VARCHAR,
    payment_gateway         VARCHAR,

    payment_status          VARCHAR,
    payment_type            VARCHAR,

    currency                VARCHAR,

    transaction_reference   VARCHAR,

    gross_amount            DECIMAL(12,2),
    discount_amount         DECIMAL(12,2),
    tax_amount              DECIMAL(12,2),

    processing_fee          DECIMAL(10,2),

    refund_amount           DECIMAL(12,2),

    final_amount            DECIMAL(12,2),

    settlement_days         INTEGER,
    settlement_date         DATE,

    created_at              TIMESTAMP,
    updated_at              TIMESTAMP
);

-- ==========================================================
-- REVIEWS
-- ==========================================================

CREATE TABLE reviews (

    review_id               VARCHAR PRIMARY KEY,

    booking_id              VARCHAR,

    customer_id             VARCHAR,

    hotel_id                VARCHAR,

    rating                  INTEGER,

    review_title            VARCHAR,

    review_text             VARCHAR,

    review_date             DATE,

    created_at              TIMESTAMP,
    updated_at              TIMESTAMP
);

-- ==========================================================
-- ORDER ITEMS
-- ==========================================================

CREATE TABLE order_items (

    order_item_id           VARCHAR PRIMARY KEY,

    booking_id              VARCHAR,

    customer_id             VARCHAR,

    hotel_id                VARCHAR,

    product_id              VARCHAR,

    quantity                INTEGER,

    unit_price              DECIMAL(10,2),

    total_price             DECIMAL(12,2),

    created_at              TIMESTAMP
);