# -*- coding: utf-8 -*-
"""Utility functions and classes."""
import logging
from collections import defaultdict
from typing import DefaultDict, Dict, Iterable, Optional, Union

import pandas as pd
import requests as req

# Local imports
from . import exceptions as E
from . import version

BASE_URL = "https://api.24sea.eu/routes/v1/"
PYDANTIC_V2 = version.parse_version(version.__version__).major >= 2

if PYDANTIC_V2:
    from pydantic import BaseModel, field_validator, validate_call  # noqa: F401

else:
    from pydantic import BaseModel, validator  # noqa: F401

    # Fallback for validate_call (acts as a no-op)
    def validate_call(*args, **kwargs):
        # Remove config kwarg if present since it's not supported in v1
        if "config" in kwargs:
            del kwargs["config"]

        def decorator(func):
            return func

        if args and callable(args[0]):
            return decorator(args[0])
        return decorator

    # Shim for field_validator to behave like validator
    def field_validator(field_name, *args, **kwargs):
        def decorator(func):
            # Convert mode='before' to pre=True for v1 compatibility
            if "mode" in kwargs:
                if kwargs["mode"] == "before":
                    kwargs["pre"] = True
                del kwargs["mode"]
            return validator(field_name, *args, **kwargs)(func)

        return decorator


def handle_request(
    url: str,
    params: Dict,
    auth: Optional[req.auth.HTTPBasicAuth],
    headers: Dict,
) -> req.models.Response:
    """Handle the request to the 24SEA API and manage errors.

    Parameters
    ----------
    url : str
        The URL to which to send the request.
    params : dict
        The parameters to send with the request.
    auth : requests.auth.HTTPBasicAuth
        The authentication object.
    headers : dict
        The headers to send with the request.

    Returns
    -------
    requests.models.Response
        The response object if the request was successful, otherwise error.
    """
    if auth is None:
        auth = req.auth.HTTPBasicAuth("", "")
    try:
        r_ = req.get(url, params=params, auth=auth, headers=headers)

        if r_.status_code in [400, 401, 403, 404, 502, 503, 504]:
            print(f"Request failed because: \033[31;1m{r_.text}\033[0m")
            r_.raise_for_status()
        # this will handle all other errors
        elif r_.status_code == 500:
            # fmt: off
            print("\033[31;1mInternal server error. You will need to contact "
                  "support at \033[32;1;4msupport.api@24sea.eu\033[0m")
            # fmt: on
            r_.raise_for_status()
        elif r_.status_code > 400:
            # fmt: off
            print("Request failed with status code: "
                  f"\033[31;1m{r_.status_code}\033[0m")
            # fmt: on
            r_.raise_for_status()
    except (req.exceptions.ConnectionError, req.exceptions.Timeout) as exc:
        print(f" Request failed because: \033[31;1m{exc}\033[0m")
        raise exc
    return r_


def default_to_regular_dict(d_: Union[DefaultDict, Dict]) -> Dict:
    """Convert a defaultdict to a regular dictionary."""
    if isinstance(d_, defaultdict):
        d_ = {k_: default_to_regular_dict(v_) for k_, v_ in d_.items()}
    return dict(d_)


# def check_authentication(func):
#     """Check authentication before making the request to the 24SEA API."""

#     def wrapper(self, *args, **kwargs):
#         """Wrapper function to check authentication."""
#         # fmt: off
#         if not isinstance(self._auth, req.auth.HTTPBasicAuth) or not self.authenticated:
#             raise E.AuthenticationError(
#                 "\033[31;1mAuthentication needed before querying the metrics.\n"
#                 "\033[0mUse the \033[34;1mdatasignals.\033[0mauthenticate("
#                 "\033[32;1m<username>\033[0m, \033[32;1m<password>\033[0m) "
#                 "method."
#             )
#         return func(self, *args, **kwargs)
#         # fmt: on

#     return wrapper


def require_auth(func):
    """Decorator to ensure authentication before executing a method"""

    def wrapper(self, *args, **kwargs):
        """Wrapper function to check authentication."""
        if not self.authenticated:
            self._lazy_authenticate()
        if not self.authenticated:
            raise E.AuthenticationError(
                "\033[31;1mAuthentication needed before querying the metrics.\n"
                "\033[0mUse the \033[34;1mdatasignals.\033[0mauthenticate("
                "\033[32;1m<username>\033[0m, \033[32;1m<password>\033[0m) "
                "method."
            )
        return func(self, *args, **kwargs)

    return wrapper


def parse_timestamp(
    df: pd.DataFrame,
    formats: Iterable[str] = ("ISO8601", "mixed"),
    dayfirst: bool = False,
    keep_index_only: bool = True,
) -> pd.DataFrame:
    """Parse timestamp column in DataFrame using multiple format attempts.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame containing timestamp column or index
    formats : Iterable[str], default ('ISO8601', 'mixed')
        List of datetime format strings to try
    dayfirst : bool, default False
        Whether to interpret dates as day first

    Returns
    -------
    pandas.DataFrame
        DataFrame with parsed timestamp column

    Raises
    ------
    ValueError
        If timestamp parsing fails with all formats
    """
    series = None
    d_e = (
        f"No format matched the timestamp index/column among {formats}.\n"
        "            Try calling `parse_timestamp` manually with another "
        "format, e.g.,\n"
        "            \033[32;1m>>>\033[31;1m import\033[0m api_24sea.utils "
        "\033[31;1mas \033[0mU\n"
        "            \033[32;1m>>>\033[0m U.parse_timestamp(df,\n"
        "                                  formats=\033[32m[\033[36m"
        "'YYYY-MM-DDTHH:MM:SSZ'\033[32m]\033[0m,\n"
        "                                  dayfirst=\033[34mFalse\033[0m)"
    )

    if df.index.name == "timestamp":
        if "timestamp" in df.columns:
            # fmt: off
            logging.warning("Both index and column named 'timestamp' found. "
                            "Index takes precedence.")
            # fmt: on
            # Drop the column if it's not the index
            df.drop(columns="timestamp", inplace=True)
        series = df.index.to_series()
    else:
        if "timestamp" in df.columns:
            if df["timestamp"].isnull().all():
                # fmt: off
                raise E.DataSignalsError("`data` must include a 'timestamp' "
                                         "column or indices convertible to "
                                         "timestamps.")
                # fmt: on
            series = df["timestamp"]
    if series is None:
        raise E.DataSignalsError(d_e)
    try:
        # Try parsing with different formats
        for fmt in formats:
            try:
                df["timestamp"] = pd.to_datetime(
                    series, format=fmt, dayfirst=dayfirst, errors="raise"
                )
                if keep_index_only:
                    df.set_index("timestamp", inplace=True)
                return df
            except ValueError:
                continue
        # fmt: off
        # If all previous attempts failed, it means that pandas version
        # is not compatible with the formats provided, therefore try
        # with the following formats.
        formats = ["%Y-%m-%dT%H:%M:%S%z", "%d.%m.%YT%H:%M:%S.%f%z",
                   "%Y-%m-%dT%H:%M:%SZ", "%d.%m.%YT%H:%M:%S.%fZ"]
        # fmt: on
        df["timestamp"] = pd.NaT
        for fmt in formats:
            temp_series = pd.to_datetime(series, format=fmt, errors="coerce")
            df["timestamp"].fillna(temp_series, inplace=True)
        if keep_index_only:
            df.set_index("timestamp", inplace=True)
        return df
    except Exception as exc:
        logging.error(f"All timestamp parsing attempts failed: {str(exc)}")
        raise E.DataSignalsError("Could not parse timestamp data") from exc
