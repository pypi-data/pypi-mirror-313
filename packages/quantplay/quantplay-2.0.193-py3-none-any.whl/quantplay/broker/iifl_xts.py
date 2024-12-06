from quantplay.broker.xts import XTS


class IIFL(XTS):
    def __init__(
        self,
        api_secret: str | None = None,
        api_key: str | None = None,
        md_api_key: str | None = None,
        md_api_secret: str | None = None,
        wrapper: str | None = None,
        md_wrapper: str | None = None,
        client_id: str | None = None,
        load_instrument: bool = True,
    ) -> None:
        super().__init__(
            root_url="https://ttblaze.iifl.com/",
            api_key=api_key,
            api_secret=api_secret,
            md_api_key=md_api_key,
            md_api_secret=md_api_secret,
            wrapper=wrapper,
            md_wrapper=md_wrapper,
            ClientID=client_id,
            load_instrument=load_instrument,
        )
