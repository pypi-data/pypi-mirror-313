from typing import Optional

from pydantic import BaseModel


class OracleCloudStorage(BaseModel):
    bucket: str
    customer_access_key_id: str
    customer_secret_key: str
    region: str
    namespace: str
    path_prefix: Optional[str] = None


class GoogleEarthEngine(BaseModel):
    project: str
    collection: str
    credentials: Optional[str] = None


class GoogleCloudStorage(BaseModel):
    bucket: str
    credentials: str
    path_prefix: Optional[str] = None


class AzureBlobStorage(BaseModel):
    account: str
    container: str
    sas_token: str
    storage_endpoint_suffix: Optional[str] = None
    path_prefix: Optional[str] = None


class Amazons3(BaseModel):
    bucket: str
    aws_region: str
    aws_access_key_id: str
    aws_secret_access_key: str
    path_prefix: Optional[str] = None


class Layout(BaseModel):
    format: str


class OrderDelivery(BaseModel):
    """
    For more information see https://developers.planet.com/apis/orders/reference/#tag/Orders
    """
    single_archive: Optional[bool] = None
    archive_type: Optional[str] = None
    archive_filename: Optional[str] = None
    layout: Optional[Layout] = None
    amazon_s3: Optional[Amazons3] = None
    azure_blob_storage: Optional[AzureBlobStorage] = None
    google_cloud_storage: Optional[GoogleCloudStorage] = None
    google_earth_engine: Optional[GoogleEarthEngine] = None
    oracle_cloud_storage: Optional[OracleCloudStorage] = None
