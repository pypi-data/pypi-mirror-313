###############################################################################
#
# (C) Copyright 2024 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################

###############################################################################
#   Imports
###############################################################################
from everysk.config import settings
from everysk.core.fields import DateField, ListField, StrField, BoolField, ChoiceField
from everysk.core.datetime import Date
from everysk.sdk.base import BaseSDK

###############################################################################
#   MarketData Implementation
###############################################################################
class MarketData(BaseSDK):

    date = DateField(default=Undefined)
    start_date = DateField(default=None)
    end_date = DateField(default=None)
    ticker_list = ListField(default=None)
    ticker_type = ChoiceField(default=None, choices=settings.ENGINES_MARKET_DATA_TICKER_TYPES)
    projection = StrField(default=None)
    nearest = BoolField(default=False)
    real_time = BoolField(default=False)

    def get_security(
        self,
        date: Date = Undefined,
        ticker_list: list[str] = Undefined,
        ticker_type: list[str] = Undefined,
        projection: str = Undefined,
        nearest: bool = Undefined
    ) -> dict:
        """
        Get security data.

        Args:
            date (Date): The date.
            ticker_list (list[str]): The ticker list.
            ticker_type (list[str]): The ticker type.
            projection (str): The projection.
            nearest (bool): The nearest flag.

        Returns:
            dict: The security data.
        """
        return self.get_response(self_obj=self, params={'date': date, 'ticker_list': ticker_list, 'ticker_type': ticker_type, 'projection': projection, 'nearest': nearest})

    def get_historical(
        self,
        date: Date = Undefined,
        start_date: Date = Undefined,
        end_date: Date = Undefined,
        ticker_list: list[str] = Undefined,
        ticker_type: str = Undefined,
        projection: str = Undefined,
        nearest: bool = Undefined,
        real_time: bool = Undefined
    ) -> dict:
        """
        Get historical data.

        Args:
            date (Date): The date.
            start_date (Date): The start date.
            end_date (Date): The end date.
            ticker_list (list[str]): The ticker list.
            ticker_type (str): The ticker type.
            projection (str): The projection.

        Returns:
            dict: The historical data.
        """
        return self.get_response(self_obj=self, params={'date': date, 'start_date': start_date, 'end_date': end_date, 'ticker_list': ticker_list, 'ticker_type': ticker_type, 'projection': projection, 'nearest': nearest, 'real_time': real_time})
