/*
=========================================================
SQL Interview Lab
Module 02 - SQL Basics
Dataset : Hotel Booking Analytics
=========================================================
*/

-- Find the total number of customers.
select count(*) as total_customers from customers;

-- List Hotels - Return all hotel names.
Select hotel_name from hotels limit 10;

-- List Countries - Return distinct countries from hotels.
select distinct country from hotels;

--Find all active hotels
select * from hotels where hotel_status='Active';

--Return all 5-star hotels
select hotel_name from hotels where star_rating = 5;

--Hotels in Germany
select hotel_name, country from hotels where country='Germany';

--Hotels in Germany or Netherlands
select hotel_name, country from hotels where country in ('Germany', 'Netherlands');

--Hotels with Swimming Pool
select hotel_name from hotels where has_pool = True;

--Hotels Without Gym
select hotel_name from hotels where has_gym = False;

--Customers with Platinum Membership
select customer_name, loyalty_tier from customers where loyalty_tier='Platinum';

--Frequent Travelers
select customer_name, traveler_type from customers where traveler_type='Frequent';

--Customers from India
select customer_name, country from customers where country='India';

--Customers Who Signed Up in 2024
select customer_name, signup_date from customers where signup_date >= DATE '2024-01-01'
  AND signup_date < DATE '2025-01-01';

--Hotels Ordered by Rating
select hotel_name, star_rating from hotels order by star_rating desc, hotel_name;

--Find all inactive products
select product_name, is_active from products where is_active=False;

--List all hotel chains
select distinct hotel_chain from hotels;

--Find all customers whose preferred language is English
select customer_name, preferred_language from customers where preferred_language='English';

--Display bookings with status Cancelled
select booking_id from bookings where booking_status='Cancelled';

--Show bookings where guest_count > 4
select booking_id, guest_count from bookings where guest_count > 4;

--Find bookings with discount_percentage > 20
select booking_id, discount_percentage from bookings where discount_percentage > 20;

--Display hotels opened after 2015
select hotel_name, opened_year from hotels where opened_year > 2015;

--Show customers from Germany or France
select customer_name, country from customers where country in ('Germany', 'France');

--List products where unit_price > 100
select product_name, unit_price from products where unit_price > 100;

--Display the first 20 bookings ordered by booking date
select booking_id, booking_date from bookings order by booking_date asc limit 20;

--Show only hotels that are active and have a rating of at least 4
select hotel_name, hotel_status, star_rating from hotels where hotel_status='Active' and star_rating >= 4;