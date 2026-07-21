/*
Module 05 – CASE WHEN & Conditional Aggregation

This module is one of my favorites because it transforms SQL from a querying language into a reporting and analytics tool.

By the end of this module, you'll be able to answer questions like:

How many completed vs cancelled bookings do we have?
What's the cancellation rate by hotel chain?
Which customers are VIPs?
How do we bucket bookings into revenue bands?
How do we create dashboard-ready reports in a single query?

These are very common in Analytics Engineer, Senior Data Engineer, and Product Analytics interviews.
*/
/*Level 1 – CASE WHEN Basics*/
/*
Question 1

Classify every booking into one of the following categories:

High Value (gross_amount ≥ 5000)
Medium Value (2000–4999)
Low Value (<2000)

Expected columns:

booking_id
gross_amount
booking_category
*/
select booking_id, gross_amount,
case
    when gross_amount >= 5000 then 'High Value'
    when gross_amount between 2000 and 4999 then 'Medium Value'
    else 'Low Value'
end as booking_category
from bookings;

/*
Display each booking along with a readable booking status.

Example:

CONFIRMED → Active
CANCELLED → Cancelled
PENDING → Pending
*/
select booking_id,
case
    when booking_status = 'Completed' then 'Active'
    when booking_status = 'Cancelled' then 'Cancelled'
    when booking_status = 'Pending' then 'Pending'
end as booking_status
from bookings;

/*
Classify customers based on age.

Example:

18–30  → Young Adult
31–50  → Adult
51+    → Senior
*/
--No Age column in customers table

/*
Classify hotels based on star rating.

Example:

5 → Luxury

4 → Premium

3 → Standard

Else → Budget
*/
select hotel_name,
case star_rating
    when 5 then 'Luxury'
    when 4 then 'Premium'
    when 3 then 'Standard'
    else 'Budget'
end as hotels_classification
from hotels;

/*
Classify reviews.

5 → Excellent

4 → Good

3 → Average

1–2 → Poor
*/
select review_id,
case rating
    when 5 then 'Excellent'
    when 4 then 'Good'
    when 3 then 'Average'
    else 'Poor'
end as review_classification
from reviews;

/*Level 2 – Conditional Aggregation*/
/*
Find the total number of

Confirmed bookings
Cancelled bookings
Pending bookings

Return everything in a single row.
*/
select
sum(case when booking_status = 'Confirmed' then 1 else 0 end) as confirmed_bookings,
sum(case when booking_status = 'Cancelled' then 1 else 0 end) as cancelled_bookings,
sum(case when booking_status = 'Pending' then 1 else 0 end) as pending_bookings
from bookings;

/*
Question 8

Find, for each hotel chain:

Total bookings
Confirmed bookings
Cancelled bookings
*/
SELECT
    hotel_chain,
    COUNT(*) AS total_bookings,
    SUM(CASE
            WHEN booking_status = 'Confirmed' THEN 1
            ELSE 0
        END) AS confirmed_bookings,
    SUM(CASE
            WHEN booking_status = 'Cancelled' THEN 1
            ELSE 0
        END) AS cancelled_bookings
FROM bookings b
INNER JOIN hotels h
    ON h.hotel_id = b.hotel_id
GROUP BY hotel_chain;

/*
For each payment method, calculate:

Total payments
Successful payments
Failed payments
*/
