from datetime import datetime
import polars as pl
import logging

pl.Config.set_tbl_cols(10)


class Strategy:
    def __init__(self, name: str = "BaseStrategy") -> None:
        self.index: str
        self.type: str
        self.exit_time: str
        self.index: str

        self.name = name
        self.underlying_map = {"NIFTY BANK": "BANKNIFTY"}
        self.data_source = "~/.quantplay"
        self.symbol_expiry = pl.read_parquet(f"{self.data_source}/symbol_expiry.parquet")

        logging.basicConfig(level=logging.INFO)

        self.logger = logging.getLogger("testing")

    def add_days_to_expiry(self, trades: pl.DataFrame) -> pl.DataFrame:
        trades = trades.join(self.symbol_expiry, on=["symbol"], how="left")
        trades = trades.with_columns(
            pl.col("expiry")
            .sub(pl.col("date_only"))
            .dt.total_days()
            .alias("days_to_expiry")
        )

        return trades

    def backtest(self, trades: pl.DataFrame):
        """
        Backtest the strategy using historical data.

        Parameters:
            data (pl.DataFrame): Historical OHLC data.

        Returns:
            pl.DataFrame: DataFrame containing signals and performance metrics.
        """
        underlying_name = self.underlying_map[self.index]
        opt_data = pl.read_parquet(
            f"{self.data_source}/RAW/OPT/{underlying_name}.parquet"
        )

        if self.type == "intraday":
            trades = trades.select(
                [
                    "date",
                    "date_only",
                    "underlying_price",
                    "symbol",
                    "close",
                ]
            ).rename({"close": "entry_price", "date": "entry_time"})

            market_data = (
                opt_data.filter(
                    pl.col("date")
                    .dt.time()
                    .eq(datetime.strptime(self.exit_time, "%H:%M").time())
                )
                .select(["symbol", "date", "close"])
                .with_columns(pl.col("date").dt.date().alias("date_only"))
                .rename({"close": "exit_price", "date": "exit_time"})
            )

            bt_trades = trades.join(market_data, on=["date_only", "symbol"], how="left")
            bt_trades = bt_trades.with_columns(
                (pl.col("exit_price").sub(pl.col("entry_price")).alias("pnl"))
            ).select(
                [
                    "symbol",
                    "entry_time",
                    "exit_time",
                    "entry_price",
                    "exit_price",
                    "pnl",
                ]
            )

            print(bt_trades)
            print(bt_trades.select(pl.col("exit_price").sub(pl.col("entry_price"))).sum())
            bt_trades.write_parquet(f"./out/{self.name}.parquet")

        elif self.type == "overnight":
            trades = (
                trades.with_columns(
                    pl.col("date_only")
                    .add(
                        pl.when(pl.col("date_only").dt.weekday().eq(5))
                        .then(pl.duration(days=3))
                        .when(pl.col("date_only").dt.weekday().eq(6))
                        .then(pl.duration(days=2))
                        .otherwise(pl.duration(days=1))
                    )
                    .alias("next_day")
                )
                .select(
                    [
                        "date",
                        "next_day",
                        "date_only",
                        "underlying_price",
                        "symbol",
                        "close",
                    ]
                )
                .rename({"close": "entry_price", "date": "entry_time"})
            )

            market_data = (
                opt_data.filter(pl.col("date").dt.time().eq(pl.time(9, 30, 0)))
                .select(["symbol", "date", "close"])
                .with_columns(pl.col("date").dt.date().alias("next_day"))
                .rename({"close": "exit_price", "date": "exit_time"})
            )

            bt_trades = trades.join(market_data, on=["next_day", "symbol"], how="left")

            bt_trades = bt_trades.with_columns(
                (pl.col("exit_price").sub(pl.col("entry_price")).alias("pnl"))
            ).select(
                [
                    "symbol",
                    "entry_time",
                    "exit_time",
                    "entry_price",
                    "exit_price",
                    "pnl",
                ]
            )

            print(bt_trades)
            print(bt_trades.select(pl.col("exit_price").sub(pl.col("entry_price"))).sum())

            bt_trades.write_parquet(f"./out/{self.name}.parquet")

    def calculate_performance(self, data: pl.DataFrame) -> pl.DataFrame:
        """
        Calculate performance metrics based on signals.vv

        Parameters:
            data (pl.DataFrame): DataFrame with signals.

        Returns:
            pl.DataFrame: DataFrame with performance metrics.
        """
        # Implement performance calculation
        raise NotImplementedError("Please implement the calculate_performance method.")

    def load_data(self) -> None:
        self.logger.info("Loading data")
        # Load data based on the provided data format

        index_data = pl.read_parquet(
            f"{self.data_source}/NSE/INDICES/minute/{self.index}.parquet"
        )
        underlying_name = self.underlying_map[self.index]
        opt_data = pl.read_parquet(
            f"{self.data_source}/RAW/OPT/{underlying_name}.parquet"
        )
        self.data = {"index_data": index_data, "opt_data": opt_data}
        self.logger.info("Data loaded successfully ....")

    def run_backtest(self, **kwargs: ...):
        """
        Run backtest for a given strategy by loading data internally.

        Parameters:
            strategy (Strategy): An instance of a Strategy subclass.
            **kwargs: Additional keyword arguments for data loading.

        Returns:
            pl.DataFrame: DataFrame with backtest results.
        """
        # Set up logging

        try:
            self.load_data()
            trades = self.generate_signals(self.data)
            self.backtest(trades)

            self.logger.info("Backtest completed successfully.")
        except Exception as e:
            self.logger.error(f"An error occurred during backtest: {e}")
            raise

    def generate_signals(self, data: dict[str, pl.DataFrame]) -> pl.DataFrame: ...
