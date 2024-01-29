# Data Ingestion Using Extract, Transform and Load in Pipeline from MySQL to PostgreSQL Using Prefect as Orchestrator and Scheduler

## Project Brief
Data Ingestion with ETL Process manages to extract data from source table MySQL then performing data transformation, data manipulation and normalization then load it to target table in Data Warehouse PosgreSQL, Data Pipeline handled by Prefect as Orchestrator and Scheduler, in the end create Data Visualization Dashboard Using Metabase. The project aims to prove my skills in Data Engineering concept and fundamental using those tools. 

## Success Criteria
- Create `docker-compose.yml` to run all tools in docker container
- Create file to generate dummy data
- Create file to develop models for source and target database
- Load dummy data to source table
- Create ETL script 
- Simulate Data Ingestion Process
- Create Data Visualization and Analytics

## Result
- Created 3 files of `docker-compose.yml` and run successfully they are:
  - `./mysql/docker-compose.yml`
  - `./postgres/docker-compose.yml`
  - `./metabase/docker-compose.yml`
- Created `./generate_data.py` to generate dummy data
- Created 2 files of databases models they are :
  - `./models.py` for source database
  - `./dwh_models.py` for target database
- Loaded dummy data to source table by executing `./models.py`
- Created `./etl_flow.py` to perform ETL which has several steps:
  - `extract` function to extract data from source table
  - `transform` function to perform data transformation, data manipulation 
  - `normalization` function to normalize data
  - `load` function to load data to target table in data warehouse
  - `etl` function to execute all functions in appropriate sequence and concurrency
  - Simulated Data Ingestion Process by deploying and running `./etl_flow.py` in prefect server
  - Created file contains Data Visualization and Analytics `./media/Divistant(3).pdf` in metabase platform

## Insights and Findings
1. Person who have more than 250 transactions
   1. The Result says there are 10 people who have more than 250 transactions
2. Data Visualization
   1. Total sales per product are very fluctuative in range Dec 9, 2001 to Dec 23, 2003.
   2. `Aroma Essence` is the first top in total quantity sold and total sales each product.
   3. Total sales distribution is likely uniform.  