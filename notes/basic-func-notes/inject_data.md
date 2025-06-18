# pseudocode for 3nf data injection
### mission statement
- to store data as a single unit, while honoring relationships between units
- to allow link data to be retrieved as complete information 

## table definitions
- **state**: Stores unique state names
- **city**: Stores unique city names
- **location**: Associates a city with a state (city_id, state_id)
- **customer**: Stores customer data, referencing location_id

## potential table relationships
- each customer references a location
- each location references a city and a state
- each customer references an email (though may be unnecessary to place emails in seperate table at this time)

## example data flow
from csv file header row - > "state" inserted into 'state' table with 'state id'
- "Illinois" inserted/found in `state` table → `state_id`
- "Springfield" inserted/found in `city` table → `city_id`
- (`city_id`, `state_id`) inserted/found in `location` table → `location_id`
- Customer data inserted in `customer` table with `location_id`

## why 3NF?
- Reduces data redundancy (no repeated city/state names)
- Ensures data integrity (city always linked to correct state)
- Makes updates and queries more efficient

## pseudocode
for each header in CSV:
    if header == "state":
        if "state" table does not exist:
            create "state" table (state_id, state_name)
    if header == "city":
        if "city" table does not exist:
            create "city" table (city_id, city_name)
    # ...handle other headers as needed...

if "location" table does not exist:
    create "location" table (location_id, city_id, state_id)

if "customer" table does not exist:
    create "customer" table (customer_id, ..., location_id, ...)

for each row in CSV:
    # Insert or get state_id
    if state not in "state" table:
        insert state into "state" table
    get state_id for state

    # Insert or get city_id
    if city not in "city" table:
        insert city into "city" table
    get city_id for city

    # Insert or get location_id
    if (city_id, state_id) not in "location" table:
        insert (city_id, state_id) into "location" table
    get location_id for (city_id, state_id)

    # Insert customer, referencing location_id
    insert customer data into "customer" table, using location_id


## scalability concerns
- Aad a `country` table for international data
- handle missing or malformed data gracefully
-- if customer only has "city" listed, how is "state" determined and can the current code determine this missing information?