# proposed 3nf 
# tables
customer, company, subscription, location, city, country

# logic 
- each customer is linked to a company (and thus to a location and phones via company).
- each company is linked to a location (which is a city/country pair).
- each subscription links a customer to a subscription date.
- location is normalized into city and country tables.

# map
customer (customer_id, first_name, last_name, company_id, email, website)
   |
   |--< company (company_id, location_id, phone_1, phone_2)
   |         |
   |         |--< location (location_id, city_id, country_id)
   |                   |           |
   |                   |           |--< city (city_id, city_name)
   |                   |
   |                   |--< country (country_id, country_name)
   |
   |--< subscription (subscription_id, customer_id, subscription_date)

# considerations as of 23june2025
dynamically creating the correct tables with their respective columns is no small feat. i propose a more interactive interface which back-end that identifies all columns in the dataset and asks the user to identify which will become tables and which will become properties of a table.

next **distil database** version will implement logic to give users control over table creation.