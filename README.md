# User Location Prospect Matching Project

## Overview
This project aims to match user prospects based on user location (country and region), providing an efficient way to evaluate and store matched results for future usage.

## Setup

1. Clone the repository:
  ```
  git clone https://github.com/aviran10/location-based-qualification.git
  ```

then, navigate to project dir:
  ```
cd <project-directory>
  ```


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

This process build the Postgres Tables and load the given data.

  ```
docker-compose up postgres_init 
  ```

NOTE: wait until the service finished the process.

## Database Schema

### List of relations

| Schema | Name                     | Type  | Owner |
|--------|---------------------------|-------|-------|
| public | countries                 | table | admin |
| public | country_regions           | table | admin |
| public | prospects                 | table | admin |
| public | regions                   | table | admin |
| public | user_excluded_locations   | table | admin |
| public | user_included_locations   | table | admin |
| public | user_prospect_results     | table | admin |
| public | users                     | table | admin |

### Table Recap

1. **countries**:
   - Contains data about different countries.
   - Useful for associating prospects or users with geographical regions.

2. **country_regions**:
   - Stores regional data for each country.
   - Helps in mapping countries to specific regions for more granular location-based matching.

3. **prospects**:
   - Stores information about the prospects (potential users or entities that are being matched).
   - Contains details that will be evaluated against users' preferences and location data.

4. **regions**:
   - Contains regional-specific data.
   - Used to classify and manage prospects and users based on their geographical location.

5. **user_excluded_locations**:
   - Stores locations that the user has explicitly excluded.
   - Helps in filtering out prospects that fall within these locations.

6. **user_included_locations**:
   - Stores locations that the user has explicitly included.
   - Used to filter and match prospects that meet the user's preferred location criteria.

7. **user_prospect_results**:
   - Stores the results of the matching process.
   - Tracks which prospects are a match based on the user's criteria (including included/excluded locations).

8. **users**:
   - Stores information about users.
   - Contains essential user details used for matching prospects against their preferences and location settings.


## Running the Match Process
The match process filters prospects based on user locations (included and not in excluded). 
After matching, the results are saved in the `user_prospect_results` table.

Run to match:
  ```
 docker-compose up match_prospect
  ```

## Quering result 
To connect the postgres DB set for this assignment, please run:
```
docker exec -it postgres_db psql -U admin -d SampleadDB
```
To query the results please run one of the following queries (or any other :) )

### 1. Count the number of prospects checked by each user
'''sql
SELECT user_id, COUNT(*) as checked_count
FROM user_prospect_results
GROUP BY user_id;  ```


### User Check Count - (partially)

| user_id                                | checked_count |
|----------------------------------------|---------------|
| 6d69ee7a-9e3b-49b9-99a4-96fe5ffeffb3  | 76            |
| f42e7328-1cb8-43a2-ad08-008b0a493db4  | 11            |
| 1776a737-8794-476c-aad6-7004dc4e64f5  | 48            |
| b16dca0d-e714-4a4b-aa63-f07073f751d3  | 250           |
| 6fabfb54-9c90-4910-8d07-0dddef15384c  | 16            |
| 11008ab0-c90a-4a3e-9163-b09e4d4336e0  | 68            |
| 07548ae5-846d-4749-b831-00d4bb818974  | 248           |
| e0d5d905-d9dd-446e-89e4-6ac899155e3f  | 118           |
| aecbce84-80cb-46fb-a2f0-9b0f488871f1  | 226           |


### 2. Retrieve all records where `is_in_location` is `true`
```sql
SELECT * 
FROM user_prospect_results
WHERE is_in_location = 't';  ```

### 3. Retrieve all records for a specific user (user_id = 'be3bd455-3858-4d5f-b8e9-1895c51e50e7')
'''sql
SELECT * 
FROM user_prospect_results
WHERE user_id = 'be3bd455-3858-4d5f-b8e9-1895c51e50e7';  ```


## Notes
- Ensure the postgres_init service finished the load_data() before running match_prospects service.
- The project uses SQLAlchemy for ORM-based interactions with the PostgreSQL database.


## More..
- If I had more time, I would add a RestAPI to retrieve queries and display the results in a better way.



