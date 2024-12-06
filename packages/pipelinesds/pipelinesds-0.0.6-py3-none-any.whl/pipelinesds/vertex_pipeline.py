from google.cloud import bigquery, bigquery_storage, storage
import pickle
import json
import pandas as pd

def get_data_from_bq(
        bq_client: bigquery.Client
        , bq_storage_client: bigquery_storage.BigQueryReadClient
        , table: str
        , where_clause: str = None
    ) -> pd.DataFrame:
    """
    Returns data from BigQuery as DataFrame.

    Parameters
    ----------
    bq_client: google.cloud.bigquery.Client
        BigQuery client.
    bq_storage_client: google.cloud.bigquery_storage.BigQueryReadClient
        BigQuery Storage client.
    table: str
        Name of table/view to get data from.
    where_clause: str
        Where clause to filter data.

    Returns
    ----------
    pd.DataFrame
        Data from the view/table.
    """
    sql = f"""
     SELECT * FROM `{table}` {where_clause}
    """
    
    results = bq_client.query(sql).to_dataframe(bqstorage_client=bq_storage_client)
    return results

def call_procedure_and_get_data_from_bq(
        bq_client: bigquery.Client
        , procedure_name: str
        , parameters: list = None
    ) -> pd.DataFrame:
    """
    Calls a stored procedure in BigQuery. If the procedure returns data, it is returned as a DataFrame.

    Parameters
    ----------
    bq_client: google.cloud.bigquery.Client
        BigQuery client.
    procedure_name: str
        Name of the stored procedure to call.
    parameters: list
        List of parameters to pass to the procedure.

    Returns
    ----------
    pd.DataFrame
        Result of the procedure call.
    """
    param_str = ', '.join(parameters) if parameters else ''
    sql = f"""
    CALL `{procedure_name}`({param_str})
    """
    
    query_job = bq_client.query(sql)
        
    if query_job.result().total_rows > 0:
        return query_job.to_dataframe()
    else:
        return None

def delete_old_data(
        bq_client: bigquery.Client
        , table: str
        , where_clause: str
    ) -> None:
    """
    Delete old data from BigQuery table.

    Parameters
    ----------
    bq_client: google.cloud.bigquery.Client
        BigQuery client.
    bq_storage_client: google.cloud.bigquery_storage.BigQueryReadClient
        BigQuery Storage client.
    table: str
        Name of table/view to delete data from.
    where_clause: str
        Where clause to filter data.
    """
    
    sql = f"""
    DELETE FROM `{table}` {where_clause}
    """
    bq_client.query(sql).result()

def write_dataframe_to_bq(
        bq_client: bigquery.Client
        , df: pd.DataFrame
        , table_id: str
        , job_config: bigquery.LoadJobConfig
    ) -> None:
    """
    Function to write dataframe to BigQuery table

    Parameters
    ----------
    bq_client: google.cloud.bigquery.Client
        BigQuery client.
    df: pd.DataFrame
        Dataframe to write
    table_id: string
        Table in BigQuery to write dataframe
    job_config : google.cloud.bigquery.LoadJobConfig
        Job configuration.
    """
    job = bq_client.load_table_from_dataframe(
        df,
        table_id,
        job_config=job_config
    )
    job.result()

def read_gcs_file(
        gcs_client: storage.Client
        , bucket_name: str
        , destination_blob_name: str
        , file_type: str
    ) -> object:
    """
    Function to read a file from a specific path on Google Cloud Storage.
        
    Parameters
    ----------
    gcs_client: google.cloud.storage.Client
        Google Cloud Storage client.
    bucket_name: str
        Name of bucket on GCS, where file is written.
    destination_blob_name: str
        Path in bucket to read file.
    file_type: str
        Type of file to read (either 'pickle' or 'json').

    Returns
    ----------
    object
        The object read from the file.
    """
    bucket = gcs_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    with blob.open(mode='rb') as file:
        if file_type == 'pickle':
            return pickle.load(file)
        elif file_type == 'json':
            return json.load(file)


def save_gcs_file(
        gcs_client: storage.Client
        , bucket_name: str
        , destination_blob_name: str
        , content: str
        , content_type: str
    ) -> None:
    """
    Function to save content to a specific path on Google Cloud Storage.
    
    Parameters
    ----------
    gcs_client: google.cloud.storage.Client
        GCS client.
    bucket_name: str
        Name of the bucket on GCS where the file will be saved.
    destination_blob_name: str
        Path in the bucket to save the file.
    content: str
        The content to be saved.
    content_type: str
        The MIME type of the content (eg. 'text/html' or 'application/json').
    """
    bucket = gcs_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(content, content_type=content_type)