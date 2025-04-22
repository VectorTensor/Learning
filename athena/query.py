import boto3
import time

athena = boto3.client('athena', region_name='us-east-1')

database = 'athena_database'
query = """SELECT * FROM AddressTable  where city = 'Bothell' LIMIT 10;"""
output_bucket = 's3://my-athena-query-results-p64/'  # Required for Athena

# Start query execution
response = athena.start_query_execution(
    QueryString=query,
    QueryExecutionContext={'Database': database},
    ResultConfiguration={'OutputLocation': output_bucket}
)

query_execution_id = response['QueryExecutionId']

# Wait for completion (optional)
while True:
    result = athena.get_query_execution(QueryExecutionId=query_execution_id)
    state = result['QueryExecution']['Status']['State']
    if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
        break
    print("Waiting for query to finish...")
    time.sleep(2)

# Check result
if state == 'SUCCEEDED':
    print("Query succeeded!")
    # Optionally fetch results
    result_response = athena.get_query_results(QueryExecutionId=query_execution_id)
    for row in result_response['ResultSet']['Rows']:
        print([col.get('VarCharValue', '') for col in row['Data']])
else:
    print("Query failed or was cancelled.")
