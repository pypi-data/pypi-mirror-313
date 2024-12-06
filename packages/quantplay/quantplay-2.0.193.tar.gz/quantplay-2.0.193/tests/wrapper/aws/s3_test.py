from quantplay.wrapper.aws.s3 import S3Utils


def test_instrument_data():
    df = S3Utils.read_csv("quantplay-market-data", "symbol_data/shoonya_instruments.csv")

    actual_unique_exchanges = set(df["exchange"].unique())  # type: ignore
    expected_unique_exchanges = {"BSE", "NSE", "BFO", "NFO"}

    assert actual_unique_exchanges == expected_unique_exchanges
