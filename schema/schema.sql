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

    customer_id            VARCHAR PRIMARY KEY,
    customer_name          VARCHAR,
    gender                 VARCHAR,
    date_of_birth          DATE,
    email                  VARCHAR,
    city                   VARCHAR,
    country                VARCHAR,
    preferred_language     VARCHAR,
    signup_date            DATE,
    loyalty_tier           VARCHAR,
    traveler_type          VARCHAR,
    customer_segment       VARCHAR,
    signup_channel         VARCHAR,
    is_active              BOOLEAN,
    created_at             TIMESTAMP,
    updated_at             TIMESTAMP

);

-- ==========================================================
-- HOTELS
-- ==========================================================

CREATE TABLE hotels (

    hotel_id                    VARCHAR PRIMARY KEY,
    hotel_name                  VARCHAR,
    hotel_chain                 VARCHAR,
    hotel_type                  VARCHAR,
    hotel_status                VARCHAR,
    city                        VARCHAR,
    country                     VARCHAR,
    star_rating                 INTEGER,
    room_count                  INTEGER,
    average_occupancy_rate      INTEGER,
    opened_year                 INTEGER,
    has_spa                     BOOLEAN,
    has_pool                    BOOLEAN,
    has_gym                     BOOLEAN,
    created_at                  TIMESTAMP,
    updated_at                  TIMESTAMP

);

-- ==========================================================
-- PRODUCTS
-- ==========================================================

CREATE TABLE products (

    product_id          VARCHAR PRIMARY KEY,
    product_name        VARCHAR,
    category            VARCHAR,
    unit_price          DECIMAL(10,2),
    tax_percentage      INTEGER,
    cost_price          DECIMAL(10,2),
    vendor              VARCHAR,
    is_active           BOOLEAN,
    created_at          TIMESTAMP,
    updated_at          TIMESTAMP

);

-- ==========================================================
-- BOOKINGS
-- ==========================================================

CREATE TABLE bookings (

    booking_id              VARCHAR PRIMARY KEY,
    booking_sequence        INTEGER,
    customer_id             VARCHAR,
    hotel_id                VARCHAR,
    booking_date            DATE,
    booking_year            INTEGER,
    booking_month           INTEGER,
    booking_quarter         VARCHAR,
    lead_time_days          INTEGER,
    check_in_date           DATE,
    check_out_date          DATE,
    stay_nights             INTEGER,
    season                  VARCHAR,
    room_type               VARCHAR,
    guest_count             INTEGER,
    occupancy_type          VARCHAR,
    booking_channel         VARCHAR,
    booking_source          VARCHAR,
    booking_status          VARCHAR,
    booking_priority        VARCHAR,
    demand_level            VARCHAR,
    available_rooms         INTEGER,
    upgrade_given           BOOLEAN,
    cancellation_date       DATE,
    created_at              TIMESTAMP,
    updated_at              TIMESTAMP,
    room_rate               DECIMAL(12,2),
    total_room_charges      DECIMAL(12,2),
    discount_percentage     INTEGER,
    discount_amount         DECIMAL(12,2),
    tax_amount              DECIMAL(12,2),
    service_fee             DECIMAL(12,2),
    gross_amount            DECIMAL(12,2),
    net_amount              DECIMAL(12,2),

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id)

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
    updated_at              TIMESTAMP,

    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
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
    updated_at              TIMESTAMP,

    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id)
);

-- ==========================================================
-- ORDER ITEMS
-- ==========================================================

CREATE TABLE order_items (

    order_item_id       VARCHAR PRIMARY KEY,
    booking_id          VARCHAR,
    customer_id         VARCHAR,
    hotel_id            VARCHAR,
    product_id          VARCHAR,
    quantity            INTEGER,
    unit_price          DECIMAL(10,2),
    total_price         DECIMAL(12,2),
    created_at          TIMESTAMP,

    FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id),
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);