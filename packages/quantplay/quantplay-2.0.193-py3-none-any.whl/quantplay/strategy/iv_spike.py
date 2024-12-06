import polars as pl
from datetime import time

from quantplay.core.strategy import Strategy
from quantplay.indicator.iv import ImpliedVolatility


class IVSpike(Strategy):
    def __init__(self) -> None:
        super().__init__(name="iv_spike")
        self.type = "intraday"
        self.exit_time = "15:10"
        self.index = "NIFTY BANK"

    def generate_signals(self, data: dict[str, pl.DataFrame]) -> pl.DataFrame:
        """
        Generate signals based on below logic
        """
        index_data = data["index_data"]
        opt_data = data["opt_data"]

        index_data = index_data.with_columns(pl.col("close").alias("underlying_price"))

        opt_data = opt_data.with_columns(pl.col("date").dt.date().alias("date_only"))
        opt_data = self.add_days_to_expiry(opt_data)

        opt_data = opt_data.filter(pl.col("days_to_expiry").lt(2))
        opt_data = opt_data.join(
            index_data["date", "underlying_price"],
            on=["date"],
            how="left",
        )
        opt_data = opt_data.filter(
            pl.col("date").dt.time() <= pl.time(hour=14, minute=45)
        )
        opt_data = opt_data.filter(pl.col("date").dt.year() >= 2024)
        opt_data = opt_data.filter(pl.col("date").dt.month() >= 8)
        print(len(opt_data))

        opt_data = opt_data.with_columns(
            pl.col("symbol")
            .str.extract(r"[A-Z]+[0-9]{2}.{3}([0-9]+)[P|C]E")
            .cast(pl.Float64)
            .alias("strike"),
            pl.col("symbol")
            .str.extract(r"[A-Z]+[0-9]{2}.{3}[0-9]+([P|C])E")
            .str.to_lowercase()
            .alias("option_type"),
            (
                (pl.col("expiry").dt.combine(time(15, 30, 0)).dt.timestamp("ms"))
                .sub(pl.col("date").dt.timestamp("ms"))
                .truediv(31536000000)
            ).alias("tte"),
        )

        opt_data = opt_data.with_columns(
            pl.struct(
                [
                    "close",
                    "strike",
                    "option_type",
                    "underlying_price",
                    "tte",
                ]
            )
            .map_elements(
                lambda x: int(
                    ImpliedVolatility.iv(
                        x["close"],
                        x["strike"],
                        x["option_type"],
                        x["underlying_price"],
                        x["tte"],
                    )
                ),
                return_dtype=pl.Float64,
            )
            .alias("iv")
        )

        trades = opt_data
        trades = trades.filter(pl.col("iv") > 40).filter(
            pl.col("close").sub(30).abs().rank("dense").eq(1).over("date_only")
        )

        trades = trades.with_columns(pl.lit("SELL").alias("transaction_type"))
        print(trades)
        return trades


if __name__ == "__main__":
    self = IVSpike()
    self.run_backtest()
