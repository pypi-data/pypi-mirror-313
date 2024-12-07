import blosc
import boto3
import finter
from finter.rest import ApiException
from finter.settings import get_api_client


def get_aws_credentials(object_type, object_value, bucket, personal):
    api_instance = finter.AWSCredentialsApi(get_api_client())

    try:
        if bucket:
            api_response = api_instance.aws_credentials_quanda_retrieve(
                object_type=object_type,
                object_value=object_value,
                bucket=bucket,
                personal=personal
            )
        else:
            api_response = api_instance.aws_credentials_quanda_retrieve(
                object_type=object_type,
                object_value=object_value,
                personal=personal
            )
        return api_response
    except ApiException as e:
        print("Exception when calling AWSCredentialsApi->aws_credentials_quanda_retrieve: %s\n" % e)
        return None


def get_user_info():
    api_instance = finter.UserApi(get_api_client())
    user = api_instance.user_info_retrieve(item='id')
    return user


class QuandaLoader:
    bucket = 'quanda-data-production'

    @staticmethod
    def get_object_full_path(object_value, personal=False):
        if personal:
            user = get_user_info()
            return f"personal/{user.data}/{object_value}"
        return object_value

    @staticmethod
    def _get_s3_client(object_type, object_value, bucket, personal):
        credentials = get_aws_credentials(object_type, object_value, bucket, personal)
        if credentials is None:
            raise Exception(f"Access to unauthorized data({object_value}). Please check the data permission.")
        else:
            return boto3.client(
                's3',
                aws_access_key_id=credentials.aws_access_key_id,
                aws_secret_access_key=credentials.aws_secret_access_key,
                aws_session_token=credentials.aws_session_token
            )

    @classmethod
    def get_object_list(cls, object_type, object_value, bucket=None, personal=False):
        if bucket is None:
            bucket = cls.bucket
        try:
            object_value = cls.get_object_full_path(object_value, personal)
            s3_client = cls._get_s3_client(object_type, object_value, bucket, personal)
            paginator = s3_client.get_paginator('list_objects_v2')

            response_iterator = paginator.paginate(
                Bucket=bucket if bucket else cls.bucket,
                Prefix=object_value
            )
            result = []
            for page in response_iterator:
                for content in page.get('Contents', []):
                    result.append(content['Key'])

            return result
        except Exception as e:
            raise Exception(f"QuandaLoader.get_object_list failed: {e}")

    @classmethod
    def get_data(cls, object_name, bucket=None, personal=False):
        if bucket is None:
            bucket = cls.bucket
        object_type = "name"
        try:
            object_value = cls.get_object_full_path(object_name, personal)
            s3_client = cls._get_s3_client(object_type, object_value, bucket, personal)

            response = s3_client.get_object(Bucket=bucket, Key=object_name)
            data = response['Body'].read()
        except Exception as e:
            raise Exception(f"QuandaLoader.get_data failed: {e}")

        try:
            return blosc.decompress(data)
        except Exception as e:
            pass

        return data
