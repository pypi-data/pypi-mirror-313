from tensorkube.services.s3_access_service import create_s3_access_to_pods
import click

def apply():
    try:
        create_s3_access_to_pods()
    except Exception as e:
        raise e
