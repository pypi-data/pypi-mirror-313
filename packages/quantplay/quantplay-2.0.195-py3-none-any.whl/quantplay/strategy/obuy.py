import polars as pl

from quantplay.core.strategy import Strategy


class OvernightOptionBuy(Strategy):
    def __init__(self) -> None:
        super().__init__(name="OBuy")
        self.type = "overnight"
        self.exit_time = "09:30"
        self.index = "NIFTY BANK"

    def generate_signals(self, data: dict[str, pl.DataFrame]) -> pl.DataFrame:
        """
        Generate signals based on below logic
        """
        index_data = data["index_data"]
        opt_data = data["opt_data"]

        index_data = index_data.filter(
            pl.col("date").dt.time() >= pl.time(hour=9, minute=30)
        )
        index_data = index_data.with_columns(pl.col("date").dt.date().alias("date_only"))
        index_data = index_data.with_columns(
            pl.col("close").cum_max().over("date_only").alias("intraday_high")
        )
        index_data = index_data.filter(
            (pl.col("date").dt.time() >= pl.time(hour=13, minute=30))
            & (pl.col("close") >= pl.col("intraday_high"))
        )
        trades = index_data.group_by("date_only").agg(pl.all().first())
        trades = trades.with_columns(pl.col("close").alias("underlying_price"))

        trades = trades[["date", "date_only", "underlying_price"]].join(
            opt_data,
            on=["date"],
            how="left",
        )

        trades = self.add_days_to_expiry(trades)

        trades = trades.filter(
            (pl.col("days_to_expiry") < 7) & pl.col("days_to_expiry").gt(3)
        ).filter(pl.col("close").sub(700).abs().rank("dense").eq(1).over("date_only"))

        return trades


if __name__ == "__main__":
    self = OvernightOptionBuy()
    self.run_backtest()
