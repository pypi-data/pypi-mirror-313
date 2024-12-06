from archytas.tool_utils import tool
import requests


@tool
def drs_uri_info(uris: list[str]) -> str:
    """
    Get information about a DRS URI.
    Data Repository Service (DRS) URIs are used to provide a standard way to locate and access data objects in a cloud environment.
    In the context of the Cancer Data Aggregator (CDA) API, DRS URIs are used to specify how to access data.

    Args:
        uris (list[str]): A list of DRS URIs to get information about. URIs should be of the form 'drs://<hostname>:<id_number>'.

    Returns:
        list[str]: The information from looking up each DRS URI.
    """
    responses = []
    for uri in uris:

        # Split the DRS URI by ':' and take the last part as the object ID
        if not uri.startswith("drs://"):
            raise ValueError("Invalid DRS URI: Must start with 'drs://'")
        try:
            object_id = uri.split(":")[-1]
        except IndexError:
            raise ValueError("Invalid DRS URI: Missing object ID")
   
        # Get information about the object from the DRS server
        url = f"https://nci-crdc.datacommons.io/ga4gh/drs/v1/objects/{object_id}"
        response = requests.get(url)
        response.raise_for_status()

        # Append the response to the list of responses
        responses.append(response.json())

    return responses



# future tools for amazon and google cloud storage
# import boto3
# from urllib.parse import urlparse
# @tool
# def download_s3_file
# etc.


# import boto3
# import os
# from urllib.parse import urlparse

# @tool
# def download_from_s3(s3_url: str) -> str:
#     """
#     Downloads a file from an S3 bucket using the S3 protocol.

#     Args:
#         s3_url (str): The S3 URL of the file (e.g., s3://bucket-name/key).

#     Returns:
#         str: The local file path where the file was saved.
#     """
#     # Parse the S3 URL using urlparse
#     parsed_url = urlparse(s3_url)
#     if parsed_url.scheme != "s3":
#         raise ValueError("Invalid S3 URL. It must start with 's3://'.")

#     bucket_name = parsed_url.netloc
#     key = parsed_url.path.lstrip("/")  # Remove leading '/' from the key

#     # Determine the local file name if not provided
#     local_file_path = os.path.basename(key)

#     # Initialize the S3 client
#     s3 = boto3.client("s3")

#     # Download the file
#     try:
#         print(f"Downloading {s3_url} to {local_file_path}...")
#         s3.download_file(bucket_name, key, local_file_path)
#         print(f"Download completed: {local_file_path}")
#         return local_file_path
#     except Exception as e:
#         print(f"Failed to download {s3_url}: {e}")
#         raise
