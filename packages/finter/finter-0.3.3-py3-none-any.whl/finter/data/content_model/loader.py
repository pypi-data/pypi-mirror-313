import fnmatch

from cachetools import TTLCache

from finter import BaseAlpha
from finter.api.content_api import ContentApi
from finter.calendar import iter_days, iter_trading_days
from finter.data.content_model.catalog_sheet import get_data
from finter.settings import get_api_client, logger


class ContentFactory:
    """
    A class representing a content model (CM) factory that generates and manages content models
    based on a specified universe name and a time range.

    Attributes:
        start (int): Start date for the content in YYYYMMDD format.
        end (int): End date for the content in YYYYMMDD format.
        universe_name (str): Name of the universe to base content models on.
        match_list (list[str]): Patterns used to match content models based on the universe name.
        cm_dict (dict[str, list[str]]): Dictionary mapping content match patterns to lists of corresponding content model names.

    Methods:
        get_df(item_name: str) -> pd.DataFrame:
            Retrieves the DataFrame associated with a specified item name.
        get_full_cm_name(item_name: str) -> str:
            Retrieves the full content model name for a specified item name.
        determine_base() -> list[str]:
            Determines the base match patterns for content models based on the universe name.
        get_cm_dict() -> dict:
            Generates the content model dictionary based on the universe's match list.
        show():
            Displays an interactive widget for exploring content model information in a scrollable list format.

    Property:
        item_list (list[str]): Provides a sorted list of unique item names from the content model dictionary.
    """

    # 클래스 레벨 캐시
    _global_cache = None

    def __init__(
        self,
        universe_name: str,
        start: int,
        end: int,
        cache_timeout: int = 0,
        cache_maxsize: int = 10,
        sub_universe=None,  # : Optional[list | pd.DataFrame]
    ):
        """
        Initializes the ContentFactory with the specified universe name, start date, and end date.

        Args:
            universe_name (str): The name of the universe which the content models are based on.
                Example: 'raw', 'kr_stock'.
            start (int): The start date for the content in YYYYMMDD format.
                Example: 20210101.
            end (int): The end date for the content in YYYYMMDD format.
                Example: 20211231.
            cache_timeout (int): The number of seconds after which the cache expires.
                Example: 3600 (1 hour).
            cache_maxsize (int): The maximum number of items to store in the cache.
                Example: 1000.
            sub_universe (Optional[list | pd.DataFrame]): A list or DataFrame of sub-universe items.

        Raises:
            ValueError: If the universe name is not supported.
        """
        self.client = get_api_client()
        self.start = start
        self.end = end
        self.universe_name = universe_name
        self.sub_universe = sub_universe
        self.api_instance = ContentApi(self.client)

        self.gs_df = get_data(content_api=self.api_instance)
        self.us_gs_df = None

        self.match_list = self.determine_base()
        self.cm_dict = self.get_cm_dict()

        self.trading_days = self.get_trading_days(start, end, universe_name)

        if cache_timeout > 0:
            self.use_cache = True
        else:
            self.use_cache = False

        if self.use_cache and ContentFactory._global_cache is None:
            ContentFactory.initialize_cache(maxsize=cache_maxsize, ttl=cache_timeout)

    def _get_us_gs_df(self):
        if self.us_gs_df is None:
            self.us_gs_df = get_data(
                content_api=self.api_instance, cm_type="us_financial"
            )
        return self.us_gs_df

    @staticmethod
    def get_trading_days(start, end, universe_name):
        if universe_name in ["kr_stock"]:
            return sorted(iter_trading_days(start, end, exchange="krx"))
        elif universe_name in ["us_stock", "us_etf", "us"]:
            return sorted(iter_trading_days(start, end, exchange="us"))
        elif universe_name in ["vn_stock"]:
            return sorted(iter_trading_days(start, end, exchange="vnm"))
        elif universe_name in ["id_stock"]:
            return sorted(iter_trading_days(start, end, exchange="id"))
        else:
            logger.warning(
                f"Unsupported universe: {universe_name}, All days are returned"
            )
            return sorted(iter_days(start, end))

    # Todo: Migrate universe with db or gs sheet or ...
    def determine_base(self):
        def __match_data(u):
            df = self.gs_df
            return list(df[df["Universe"] == u]["Object Path"])

        if self.universe_name == "raw":
            return []
        elif self.universe_name == "kr_stock":
            return __match_data("KR STOCK")
        elif self.universe_name == "us_etf":
            return __match_data("US ETF")
        elif self.universe_name == "us_stock":
            return __match_data("US STOCK")
        elif self.universe_name == "us":
            return __match_data("US")
        elif self.universe_name == "vn_stock":
            return __match_data("VN STOCK")
        elif self.universe_name == "id_stock":
            return __match_data("ID STOCK")
        elif self.universe_name == "crypto_spot":
            return __match_data("CRYPTO SPOT")
        elif self.universe_name == "crypto_future":
            return __match_data("CRYPTO FUTURE")
        elif self.universe_name == "common":
            return __match_data("COMMON")
        else:
            raise ValueError(f"Unknown universe: {self.universe_name}")

    def get_cm_dict(self):
        if self.universe_name == "raw":
            return {}

        cm_dict = {}
        for match in self.match_list:
            api_category = self.gs_df[self.gs_df["Object Path"] == match][
                "Category"
            ].tolist()[0]
            api_sub_category = self.gs_df[self.gs_df["Object Path"] == match][
                "Sub Category"
            ].tolist()[0]

            category = match.split(".")[3]
            try:
                cm_list = self.api_instance.content_identities_retrieve(
                    category=category
                ).cm_identity_name_list

                net_cm_list = [
                    item.split(".")[4]
                    for item in cm_list
                    if fnmatch.fnmatchcase(item, match)
                ]

                if self.universe_name == "us_etf":
                    net_cm_list = [
                        cm.replace("us-etf-", "")
                        for cm in net_cm_list
                        if "us-etf" in cm
                    ]
                elif self.universe_name == "us":
                    net_cm_list = [
                        cm.replace("us-all-", "")
                        for cm in net_cm_list
                        if "us-all" in cm
                    ]
                elif self.universe_name == "us_stock":
                    if category in ["price_volume", "classification"]:
                        net_cm_list = [
                            cm.replace("us-stock-", "")
                            for cm in net_cm_list
                            if "us-stock-" in cm
                        ]
                    elif category == "financial":
                        self.us_gs_df = self._get_us_gs_df()
                        identity_format = match.split(".")[4]
                        if identity_format[-2] == "-":
                            net_cm_list = list(self.us_gs_df["items"].values)
                        elif identity_format[-2] == "_":
                            net_cm_list = list(self.us_gs_df["pit_items"].values)
                    elif category == "factor":
                        net_cm_list = [
                            cm.replace("us-stock_pit-", "")
                            for cm in net_cm_list
                            if "us-stock_pit-" in cm
                        ]
                elif self.universe_name == "vn_stock":
                    net_cm_list = [
                        cm.replace("vnm-stock-", "") if "vnm-stock" in cm else cm
                        for cm in net_cm_list
                    ]
                elif self.universe_name == "id_stock":
                    net_cm_list = [
                        cm.replace("id-all-", "") if "id-all-" in cm else cm
                        for cm in net_cm_list
                    ]

                elif self.universe_name == "crypto_spot":
                    net_cm_list = [
                        cm.replace("spot-", "") if "spot-" in cm else cm
                        for cm in net_cm_list
                        if not cm.split("_")[-1].isdigit()
                    ]
                elif self.universe_name == "crypto_future":
                    net_cm_list = [
                        cm
                        for cm in net_cm_list
                        if not cm.split("_")[-1].isdigit() and "_m" in cm
                    ]

                cm_dict[match, api_category, api_sub_category] = net_cm_list
            except Exception as e:
                logger.error(f"API call failed: {e}")
        return cm_dict

    def get_df(self, item_name, category=None, freq="1d", **kwargs):
        cm_name = self.get_full_cm_name(item_name, category, freq)
        param = {
            "start": self.start,
            "end": self.end,
            "sub_universe": self.sub_universe,
        }
        if self.sub_universe is None:
            param.pop("sub_universe")
        param.update(kwargs)
        if self.client.user_group in ["free_tier", "data_beta"]:
            param["code_format"] = "short_code"
            param["trim_short"] = True
            if "ftp.financial" in cm_name or "ftp.consensus" in cm_name:
                param["code_format"] = "cmp_cd"

        if self.use_cache and ContentFactory._global_cache is not None:
            cache_key = (cm_name, frozenset(param.items()))
            if cache_key in ContentFactory._global_cache:
                return ContentFactory._global_cache[cache_key]

        df = BaseAlpha.get_cm(cm_name).get_df(**param)
        if self.use_cache and ContentFactory._global_cache is not None:
            ContentFactory._global_cache[cache_key] = df

        return df

    # Todo: Dealing duplicated item name later
    def get_full_cm_name(self, item_name, category=None, freq="1d"):
        if self.universe_name == "raw":
            return item_name

        try:
            if "crypto_spot" in self.universe_name:
                cm_list = [
                    key[0].replace("*", "{}").format(*item_name.split("-"))
                    for key, items in self.cm_dict.items()
                    if item_name in items
                ]
            else:
                cm_list = [
                    key[0].replace("*", item_name)
                    for key, items in self.cm_dict.items()
                    if item_name in items
                ]

            if len(cm_list) > 1:
                logger.info(
                    f"""
                    Multiple matching cm are detected
                    Matching cm list : {str([cm_name.split('.')[3] + '.' + item_name + '.' + cm_name.split('.')[5] for cm_name in cm_list])}
                    """
                )
                if category is not None:
                    cm_list = [cm for cm in cm_list if category in cm]
                if freq != "1d":
                    cm_list = [cm for cm in cm_list if freq.lower() in cm]
                cm_name = cm_list[0]
                logger.info(
                    f"""
                    {cm_name.split('.')[3] + '.' + item_name + '.' + cm_name.split('.')[5]} is returned
                    To specify a different cm, use category or freq parameters.
                    For example, .get_df('SP500_EWS', freq = '1M')  \t .get_df('all-mat_cat_rate', category = 'sentiment_exp_us')
                    """
                )
                return cm_name
            else:
                return next(iter(cm_list))

        except StopIteration:
            raise ValueError(f"Unknown item_name: {item_name}")

    def show(self):
        from IPython.display import HTML, display
        from ipywidgets import widgets

        # Build mappings for categories and subcategories
        category_mapping = {}
        subcategory_mapping = {}

        for key in self.cm_dict.keys():
            category = key[1]
            subcategory = key[2]
            freq = key[0].split(".")[-1]

            subcategory = f"{subcategory} ({freq})"

            if self.universe_name == "vn_stock":
                if "spglobal" in key[0]:
                    category = f"{category} (deprecated)"
                else:
                    category = category

            if "-v2" in key[0].split(".")[-3]:
                category = f"{category} (v2)"

            elif category_mapping.get(category):
                if self.universe_name == "us_stock" and category == "financial":
                    category = "PIT financial"

            # Initialize category and subcategory mappings
            if category not in category_mapping:
                category_mapping[category] = set()
            category_mapping[category].add(subcategory)

            if category not in subcategory_mapping:
                subcategory_mapping[category] = {}
            if subcategory not in subcategory_mapping[category]:
                subcategory_mapping[category][subcategory] = []
            subcategory_mapping[category][subcategory].extend(self.cm_dict[key])

        # Create sorted lists for dropdown options
        categories = sorted(category_mapping.keys())

        # Widgets for category and subcategory
        category_widget = widgets.Dropdown(options=categories, description="Category:")
        subcategory_widget = widgets.Dropdown(description="Subcategory:")

        # Function to update subcategory options based on selected category
        def update_subcategories(*args):
            selected_category = category_widget.value
            subcategories = sorted(category_mapping[selected_category])
            subcategory_widget.options = subcategories
            if subcategories:
                subcategory_widget.value = subcategories[0]
            else:
                subcategory_widget.value = None

        # Observe changes in category selection
        category_widget.observe(update_subcategories, names="value")

        # Initialize subcategory options
        update_subcategories()

        # Function to display information based on selections
        def show_info(category, subcategory):
            items = subcategory_mapping[category][subcategory]

            # Find the matching key for the current category and subcategory
            matching_key = next(
                key
                for key in self.cm_dict.keys()
                if key[1]
                == category.replace(" (deprecated)", "")
                .replace(" (v2)", "")
                .replace("PIT ", "")
                and key[2] == subcategory.split(" (")[0]
            )

            url = self.gs_df[self.gs_df["Object Path"] == matching_key[0]][
                "URL"
            ].tolist()[0]

            # Display items in a scrollable list
            scrollable_list = (
                '<div style="height:600px;width:400px;border:1px solid #ccc;overflow:auto;float:left;margin-right:10px;">'
                + "<ul>"
                + "".join(f"<li>{item}</li>" for item in items)
                + "</ul></div>"
            )

            iframe_html = f'<iframe src="{url}" width="1000" height="600" style="float:left;"></iframe>'

            clear_div = '<div style="clear:both;"></div>'

            display(
                HTML(
                    f"<h3>{category} - {subcategory}</h3>"
                    + scrollable_list
                    + iframe_html
                    + clear_div
                )
            )

        # Layout the widgets
        ui = widgets.VBox([category_widget, subcategory_widget])

        out = widgets.interactive_output(
            show_info, {"category": category_widget, "subcategory": subcategory_widget}
        )

        display(ui, out)

    @property
    def item_list(self):
        return sorted(
            set(item for sublist in self.cm_dict.values() for item in sublist)
        )

    @classmethod
    def reset_cache(cls):
        """Resets the global cache."""
        cls._global_cache = None

    @classmethod
    def initialize_cache(cls, maxsize, ttl):
        """Initializes the global cache with given parameters."""
        cls._global_cache = TTLCache(maxsize=maxsize, ttl=ttl)
