# django_search

# Descriptions
* Fundamental MVT pattern of Django 
* Docker connection with Postgresql
* Full-text search and GIN index in Postgresql
* Data Used with 45,641 rows with 'authors' and 'title' fields

# Main Requirements 
* Python (3.9.1)
* Django (3.2.7)
* Psycopg2-binary (2.9.1)
* Docker (20.10.8)
* Postgresql(11)

# Summaries
## A query flow in Postgres 
1. Assume that we write a query in SQL by using a script to get a specific data in server 
2. A mechanism 'query planner' comes in actions and
3. Execute a query that has the fastest execution time among queries collectd from query planner 
4. Server Output results 

## Full-text search 
* Full Text Searching (or just text search) provides the capability to identify natural-language documents that satisfy a query, 
and optionally to sort them by relevance to the query

## DB indexing 
* A data structure for improving retrieve operation in Database 

## General Inverted Indexing(GIN)
* A technique to enhance execution time in Postgresql
