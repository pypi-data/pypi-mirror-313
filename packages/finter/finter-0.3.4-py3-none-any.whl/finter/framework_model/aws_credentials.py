import numpy as np
import pandas as pd
import s3fs

import finter
from finter.framework_model import serializer
from finter.log import PromtailLogger
from finter.rest import ApiException
from finter.settings import get_api_client, logger


def get_aws_credentials(identity_name):
    api_instance = finter.AWSCredentialsApi(get_api_client())

    try:
        api_response = api_instance.aws_credentials_retrieve(
            identity_name=identity_name
        )
        return api_response
    except ApiException as e:
        print(
            "Exception when calling AWSCredentialsApi->aws_credentials_retrieve: %s\n"
            % e
        )


def get_parquet_df(identity_name, columns: list = None):
    credentials = get_aws_credentials(identity_name)
    fs = s3fs.S3FileSystem(
        key=credentials.aws_access_key_id,
        secret=credentials.aws_secret_access_key,
        token=credentials.aws_session_token,
    )

    s3_bucket_name = "finter-parquet"
    file_name = f"{identity_name}.parquet"
    s3_uri = f"s3://{s3_bucket_name}/{file_name}"

    if columns:
        str_columns = [str(column) for column in columns]
        import pyarrow.parquet as pq

        parquet_file = pq.ParquetFile(fs.open(s3_uri, "rb"))
        metadata_columns = parquet_file.metadata.schema.names

        # check columns in metadata
        assert all(
            column in metadata_columns for column in str_columns
        ), f"{[col for col in str_columns if col not in metadata_columns]} columns not in the parquet file"

        pyarrow_index = "__index_level_0__"
        if pyarrow_index in metadata_columns:
            str_columns.append(pyarrow_index)

        selected_df = parquet_file.read(columns=str_columns, use_pandas_metadata=True)
        df = selected_df.to_pandas()

    else:
        with fs.open(s3_uri, "rb") as f:
            df = pd.read_parquet(f, engine="pyarrow")

    PromtailLogger.send_log(
        level="INFO",
        message=f"{identity_name}",
        service="finterlabs-jupyterhub",
        user_id=PromtailLogger.get_user_info(),
        operation="load_model_data_parquet",
        status="success",
    )

    if pd.api.types.is_datetime64_any_dtype(df.index):
        df.index = df.index.astype("datetime64[ns]")

    if serializer.is_serializer_target(identity_name):
        df = serializer.apply_deserialization(df)

    # FL-2089 content model이 아닌 경우 항상 None을 nan으로 변경한다 c2환경에서만 이슈이고 c3에서는 이슈없음
    if not identity_name.startswith("content."):
        df.replace({None: np.nan}, inplace=True)

    return df
