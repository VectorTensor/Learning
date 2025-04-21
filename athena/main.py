import boto3
import time

athena_client = boto3.client('athena',region_name='us-east-1')

database_name = 'athena_database'
table_name = 'your_table'
s3_output = 's3://my-athena-query-results-p64/'  # Athena query results go here
data_location = 's3://curated-zone-p64/'  # Path where your CSV files are

query = f"""
CREATE EXTERNAL TABLE IF NOT EXISTS {database_name}.{table_name} (
    id INT,
    name STRING,
    age INT
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
    'serialization.format' = ','
) 
STORED AS TEXTFILE
LOCATION '{data_location}'
TBLPROPERTIES ('skip.header.line.count'='1');
"""

# Start the query
response = athena_client.start_query_execution(
    QueryString=query,
    QueryExecutionContext={'Database': database_name},
    ResultConfiguration={'OutputLocation': s3_output}
)

# Wait for it to finish (optional)
query_execution_id = response['QueryExecutionId']
state = 'RUNNING'
while state in ['RUNNING', 'QUEUED']:
    result = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
    state = result['QueryExecution']['Status']['State']
    if state == 'SUCCEEDED':
        print("Table created successfully!")
    elif state == 'FAILED':
        print("Query failed:", result['QueryExecution']['Status']['StateChangeReason'])
        break
    time.sleep(2)


s3 = boto3.client('s3')

csv_content = "id,namae,age\n1,Prayashah,25\n2,Ayash,23\n3,Leon,30"
bucket = "curated-zone-p64"
key = "curated-zone-p64/sample_data2.csv"  # This should match the Athena table LOCATION

s3.put_object(Body=csv_content, Bucket=bucket, Key=key)
print("Data written to S3.")

