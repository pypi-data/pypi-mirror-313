import os
from threading import Lock

import boto3
import pandas as pd
import polars as pl
import pyarrow.dataset as ds  # type:ignore
import s3fs  # type:ignore
from boto3.s3.transfer import TransferConfig
from retrying import retry  # type: ignore

from quantplay.utils.constant import Constants

lock = Lock()

TransferConfig(use_threads=False)


class S3Bucket:
    quantplay_market_data = "quantplay-market-data"


class S3Utils:
    @staticmethod
    def get_parquet(path: str) -> pl.DataFrame:
        # set up
        fs = s3fs.S3FileSystem()  # type:ignore

        # read parquet
        dataset = ds.dataset(f"s3://{path}", filesystem=fs, format="parquet")  # type: ignore
        df_parquet = pl.scan_pyarrow_dataset(dataset)  # type: ignore
        return df_parquet.collect()

    @staticmethod
    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_attempt_number=2,
    )
    def read_csv(bucket: str, key: str) -> pd.DataFrame:
        full_path = f"/tmp/{bucket}/{key}"

        try:
            try:
                lock.acquire()
                data = pd.read_csv(full_path)  # type: ignore
                return data

            except Exception:
                Constants.logger.info("[S3_READ_FAILED] failed to read from s3")
                raise

            finally:
                lock.release()

        except Exception:
            print(f"Data not found for {key}")

        print(f"fetching bucket from s3 {bucket} key {key}")

        client = boto3.client("s3")  # type: ignore

        raw_stream = client.get_object(Bucket=bucket, Key=key)
        content = raw_stream["Body"].read().decode("utf-8")

        print(f"Saving data at /tmp/{key}")
        full_folder_path = full_path[0 : full_path.rfind("/")]

        if not os.path.exists(full_folder_path):
            os.makedirs(full_folder_path)

        text_file = open(full_path, "w")
        text_file.write(content)
        text_file.close()

        return pd.read_csv(full_path)  # type: ignore
