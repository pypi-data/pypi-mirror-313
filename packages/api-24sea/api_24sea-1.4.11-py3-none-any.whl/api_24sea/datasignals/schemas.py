# -*- coding: utf-8 -*-
"""Data signals types."""
import datetime
from typing import Dict, List, Optional, Union

from .. import utils as U

# class Metric(BaseModel):
#     """A pydantic schema for the metrics names."""

#     start_timestamp: str
#     end_timestamp: str
#     site: str
#     location: str
#     data_group: Optional[str]
#     metric: str
#     statistic: Optional[str]
#     short_hand: Optional[str]
#     unit_str: Optional[str]
#     print_str: Optional[str]
#     description: Optional[str]
#     crud_privileges: Optional[str]


# class Metrics(BaseModel):
#     """A pydantic schema for the metrics names."""

#     metrics: List[Metric]


class GetData(U.BaseModel):
    """A pydantic schema for the data signals."""

    start_timestamp: Union[datetime.datetime, str]
    end_timestamp: Union[datetime.datetime, str]
    sites: Optional[Union[str, List[str]]] = None
    locations: Optional[Union[str, List[str]]] = None
    metrics: Union[str, List[str]]
    outer_join_on_timestamp: bool
    as_dict: Optional[bool] = False
    as_star_schema: Optional[bool] = False
    headers: Dict[str, str] = {"accept": "application/json"}

    @U.field_validator("start_timestamp", "end_timestamp", mode="before")
    def validate_timestamp(cls, v: Union[datetime.datetime, str]) -> str:
        """Validate the timestamps."""
        if isinstance(v, str):
            try:
                datetime.datetime.strptime(v, "%Y-%m-%dT%H:%M:%SZ")
            except Exception:
                try:
                    from shorthand_datetime import parse_shorthand_datetime

                    return parse_shorthand_datetime(v).strftime(  # type: ignore
                        "%Y-%m-%dT%H:%M:%SZ"
                    )
                except Exception as exc:
                    raise ValueError(
                        "\033[31mIncorrect start timestamp format, expected "
                        "one of the following formats:"
                        "\n               \033[1m• 'YYYY-MM-DDTHH:MM:SSZ'"
                        "\033[22m, \n               \033[1m• shorthand_datetime"
                        "-compatible string\033[22m "
                        "(https://pypi.org/project/shorthand-datetime/), or, "
                        "\n               "
                        "\033[1m• datetime.datetime\033[22m object.\033[0m\n\n"
                        "Exception originated from\n" + str(exc)
                    )

        if isinstance(v, datetime.datetime):
            # Enforce timezone UTC as well
            return v.strftime("%Y-%m-%dT%H:%M:%SZ")

        return v

    @U.field_validator("sites", "locations", mode="before")
    def validate_sites_locations(cls, v):
        """Validate and normalize sites and locations."""
        if isinstance(v, str):
            v = [v]
        if isinstance(v, List):
            v = [str(item).lower() for item in v]
        return v

    @U.field_validator("metrics", mode="before")
    def validate_metrics(cls, v):
        """Validate and normalize metrics."""
        if isinstance(v, str):
            v = [v]
        if isinstance(v, List):
            # fmt: off
            v = [item.replace(" ", ".*")
                     .replace("_", ".*")
                     .replace("-", ".*") for item in v]
            # fmt: on
        return "|".join(v)

    @U.field_validator("outer_join_on_timestamp", mode="before")
    def validate_outer_join_on_timestamp(cls, v):
        """Validate the outer join on timestamp."""
        if v is None:
            return False
        return v

    @U.field_validator("headers", mode="before")
    def validate_headers(cls, v):
        """Validate the headers."""
        if v is None:
            return {"accept": "application/json"}
        return v
