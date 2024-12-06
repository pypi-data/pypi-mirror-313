import base64
import hashlib
import urllib.parse
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime, UTC
from xml.dom import minidom


def generate_mock_s3_multipart_upload_url(
        bucket_name: str,
        object_key: str,
        region: str = "us-west-2",
        access_key: str = "AKIAIOSFODNN7EXAMPLE",
        secret_key: str = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        expiration: int = 3600
) -> str:
    # Generate the current timestamp
    now = datetime.now(UTC)
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = now.strftime("%Y%m%d")

    # Create the credential scope
    credential_scope = f"{date_stamp}/{region}/s3/aws4_request"

    # Create the canonical query string
    canonical_querystring = urllib.parse.urlencode({
        "X-Amz-Algorithm": "AWS4-HMAC-SHA256",
        "X-Amz-Credential": f"{access_key}/{credential_scope}",
        "X-Amz-Date": amz_date,
        "X-Amz-Expires": str(expiration),
        "X-Amz-SignedHeaders": "host"
    })

    # Generate a mock signature (in reality, this would be a complex calculation)
    mock_signature = hashlib.sha256(secret_key.encode() + amz_date.encode()).hexdigest()

    # Construct the final URL
    endpoint = f"https://{bucket_name}.s3.{region}.amazonaws.com"
    final_url = f"{endpoint}/{object_key}?{canonical_querystring}&X-Amz-Signature={mock_signature}"

    return final_url


def generate_mock_s3_multipart_upload_start_response(
        bucket_name: str,
        object_key: str,
        upload_id: str = None
) -> str:
    # Generate a random upload ID if not provided
    if upload_id is None:
        upload_id = f"2~{uuid.uuid4().hex}"

    # Create the XML structure
    root = ET.Element("InitiateMultipartUploadResult")
    ET.SubElement(root, "Bucket").text = bucket_name
    ET.SubElement(root, "Key").text = object_key
    ET.SubElement(root, "UploadId").text = upload_id

    # Convert to string and pretty print
    xml_string = ET.tostring(root, encoding="unicode")
    pretty_xml = minidom.parseString(xml_string).toprettyxml(indent="  ")

    return pretty_xml


def generate_mock_gcs_upload_url(
        bucket_name: str,
        object_name: str,
        project_id: str = "my-project-123",
        expiration: int = 3600
) -> str:
    # Generate the current timestamp
    now = datetime.now(UTC)

    # Create a mock signature (in reality, this would be a complex calculation)
    mock_signature = base64.b64encode(hashlib.sha256(f"{bucket_name}{object_name}".encode()).digest()).decode()

    # Construct the base URL
    base_url = f"https://storage.googleapis.com/{bucket_name}/{object_name}"

    # Create query parameters
    query_params = {
        "X-Goog-Algorithm": "GOOG4-RSA-SHA256",
        "X-Goog-Credential": f"{project_id}@gs-project-accounts.iam.gserviceaccount.com/{now.strftime('%Y%m%d')}/auto/storage/goog4_request",
        "X-Goog-Date": now.strftime("%Y%m%dT%H%M%SZ"),
        "X-Goog-Expires": str(expiration),
        "X-Goog-SignedHeaders": "host",
        "X-Goog-Signature": mock_signature
    }

    # Encode query parameters
    encoded_params = urllib.parse.urlencode(query_params)

    # Construct the final URL
    final_url = f"{base_url}?{encoded_params}"

    return final_url
