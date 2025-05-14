# User Location Prospect Matching Project

## Overview
This project aims to match user prospects based on user location (country and region), providing an efficient way to evaluate and store matched results for future usage.

## Setup

1. Clone the repository:
git clone https://github.com/aviran10/location-based-qualification.git
cd <project-directory>


### 2. Ensure Docker is running
- Make sure Docker is installed and running on your machine. You can check this by running:
  ```
  docker --version
  ```
- Use Docker Compose to set up the required services (like the database). To start the services, run:
  ```
  docker-compose build
  ```

Run Postgress Init:

docker-compose up postgres_init 

## Database Schema
This project uses the following key tables:
- `users`: Stores user details.
- `prospects`: Contains prospect data.
- `user_included_locations`: Stores locations included for each user.
- `user_excluded_locations`: Stores locations excluded for each user.
- `user_prospect_results`: Contains the results of the matching process.

                List of relations
 Schema |          Name           | Type  | Owner
--------+-------------------------+-------+-------
 public | countries               | table | admin
 public | country_regions         | table | admin
 public | prospects               | table | admin
 public | regions                 | table | admin
 public | user_excluded_locations | table | admin
 public | user_included_locations | table | admin
 public | user_prospect_results   | table | admin
 public | users                   | table | admin


## Running the Match Process
The match process filters prospects based on user locations (included and not in excluded). 
After matching, the results are saved in the `user_prospect_results` table.
Run to match:

 docker-compose up match_prospect

## Quering result 

### 1. Retrieve all records where `is_in_location` is `true`
```sql
SELECT * 
FROM user_prospect_results
WHERE is_in_location = 't';
## Notes
- Ensure the postgres_init service finished the load_data() before running match_prospects service.
- The project uses SQLAlchemy for ORM-based interactions with the PostgreSQL database.

### 2. Count the number of prospects checked by each user
'''sql
SELECT user_id, COUNT(*) as checked_count
FROM user_prospect_results
GROUP BY user_id;

### 3. Retrieve all records for a specific user (user_id = 'be3bd455-3858-4d5f-b8e9-1895c51e50e7')
'''sql
SELECT * 
FROM user_prospect_results
WHERE user_id = 'be3bd455-3858-4d5f-b8e9-1895c51e50e7';

