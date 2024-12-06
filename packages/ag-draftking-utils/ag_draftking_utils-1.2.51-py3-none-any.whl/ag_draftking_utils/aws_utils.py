from io import StringIO
import boto3


def csv_to_s3(df, bucket, key, index=False):
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=index)
    s3_client = boto3.client('s3')
    s3_client.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())


def dump_string_to_s3(string, bucket, key):
    s3 = boto3.resource('s3')
    object = s3.Object(bucket, key)
    object.put(Body=string)
    print(f'Successfully wrote to file s3://{bucket}/{key}')