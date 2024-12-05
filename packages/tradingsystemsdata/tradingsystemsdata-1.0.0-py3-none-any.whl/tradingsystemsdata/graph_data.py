"""
Graph the performance of the trading strategy

"""
import numpy as np
import pandas as pd
# pylint: disable=unbalanced-tuple-unpacking
# pylint: disable=no-else-return

class GraphData():
    """
    Class of functions used to return data to graph trading system performance

    """

    @staticmethod
    def graph_variables(
        prices: pd.DataFrame,
        entry_type: str,
        entry_signal_indicators: dict | None = None) -> dict:
        """
        Create graph initialization variables

        Returns
        -------
        dates : Pandas Series
            The dates to plot on the x-axis.
        price : Pandas Series
            Closing Prices.
        equity : Pandas Series
            Daily Mark to Market Equity level.
        cumsig : Pandas Series
            The cumulative buy / sell signal.
        lower_bound : Pandas Series
            Lower point to set where trading signals are plotted from.
        upper_bound : Pandas Series
            Upper point to set where trading signals are plotted from.

        """

        # Dictionary to store default params
        graph_params = {}

        # Set the dates to the index of the main DataFrame
        graph_params['dates'] = prices.index

        # Closing Prices
        graph_params['price'] = prices['Close']

        # MTM Equity
        graph_params['equity'] = prices['mtm_equity']

        # Cumulative sum of the combined entry, exit and stop signal
        graph_params['cumsig'] = prices['combined_signal'].cumsum()

        # The lower and upper bounds are used in setting where the trade
        # signals are plotted on the price chart
        # If the entry is a channel breakout
        if entry_type == 'channel_breakout':

            # Set the lower bound as rolling low close prices
            graph_params['lower_bound'] = prices[
                entry_signal_indicators[entry_type][0]]

            # Set the upper bound as rolling high close prices
            graph_params['upper_bound'] = prices[
                entry_signal_indicators[entry_type][1]]

        elif entry_type in ['2ma', '3ma', '4ma']:

            # Set the lower bound as the lowest of the moving average values
            # and the price
            graph_params['lower_bound'] = prices['min_ma']

            # Set the upper bound as the highest of the moving average values
            # and the price
            graph_params['upper_bound'] = prices['max_ma']

        # Otherwise
        else:
            # Set the upper and lower bounds to the closing price
            graph_params['lower_bound'] = graph_params['price']
            graph_params['upper_bound'] = graph_params['price']

        return graph_params


    @staticmethod
    def _bar_color(
        price_data: pd.Series,
        color1: str,
        color2: str) -> np.ndarray:
        """
        Set barchart color to green if positive and red if negative.

        Parameters
        ----------
        price_data : Series
            Price data.
        color1 : Str
            Color for positive data.
        color2 : Str
            Color for negative data.

        Returns
        -------
        Series
            Series of colors for each data point.

        """
        return np.where(price_data.values > 0, color1, color2).T


    @classmethod
    def create_signals(
        cls,
        prices: pd.DataFrame,
        graph_params: dict) -> dict:
        """
        Create trade signals to be plotted on main price chart

        Parameters
        ----------
        cumsig : Pandas Series
            The cumulative buy / sell signal.
        lower_bound : Pandas Series
            Lower point to set where trading signals are plotted from.
        upper_bound : Pandas Series
            Upper point to set where trading signals are plotted from.

        Returns
        -------
        signal_dict : Dict
            Dictionary containing the trade signal details.

        """
        # Create empty dictionary
        signal_dict = {}
        signal_dict['data_markers'] = {}

        upper, lower = cls._set_upper_lower(graph_params=graph_params)

        buy_sell_distance = 0.10 * (upper - lower) # 0.07
        flat_distance = 0.15 * (upper - lower) # 0.1

        # Buy signal to go long is where the current cumulative signal is to be
        # long when yesterday it was flat
        signal_dict['buy_long_signals'] = (
            (graph_params['cumsig'] == 1)
            & (graph_params['cumsig'].shift() != 1))

        # Place the marker at the specified distance below the lower bound
        signal_dict['buy_long_marker'] = (
            graph_params['lower_bound']
            * signal_dict['buy_long_signals']
            - buy_sell_distance)
            #- graph_params['lower_bound'].max()*buy_sell_distance)

        signal_dict['buy_long_marker'] = signal_dict[
            'buy_long_marker'][signal_dict['buy_long_signals']]
        
        # Add raw signal position for use in api
        signal_dict['data_markers']['openLong'] = (
            graph_params['lower_bound']
            * signal_dict['buy_long_signals']
        )

        signal_dict['data_markers']['openLong'] = signal_dict['data_markers'][
            'openLong'][signal_dict['buy_long_signals']]

        # Set the dates for the buy long signals
        signal_dict['buy_long_dates'] = prices.index[
            signal_dict['buy_long_signals']]
        
        signal_dict['data_markers']['openLongDates'] = signal_dict['buy_long_dates']

        # Buy signal to go flat is where the current cumulative signal is to be
        # flat when yesterday it was short
        signal_dict['buy_flat_signals'] = (
            (graph_params['cumsig'] == 0)
            & (graph_params['cumsig'].shift() == -1))

        # Place the marker at the specified distance below the lower bound
        signal_dict['buy_flat_marker'] = (
            graph_params['lower_bound']
            * signal_dict['buy_flat_signals']
            - flat_distance)
            #- graph_params['lower_bound'].max()*flat_distance)

        signal_dict['buy_flat_marker'] = signal_dict[
            'buy_flat_marker'][signal_dict['buy_flat_signals']]
        
        # Add raw signal position for use in api
        signal_dict['data_markers']['closeShort'] = (
            graph_params['lower_bound']
            * signal_dict['buy_flat_signals']
        )
        signal_dict['data_markers']['closeShort'] = signal_dict['data_markers']['closeShort'][signal_dict['buy_flat_signals']]

        # Set the dates for the buy flat signals
        signal_dict['buy_flat_dates'] = prices.index[
            signal_dict['buy_flat_signals']]
        
        signal_dict['data_markers']['closeShortDates'] = signal_dict['buy_flat_dates']

        # Sell signal to go flat is where the current cumulative signal is to
        # be flat when yesterday it was long
        signal_dict['sell_flat_signals'] = (
            (graph_params['cumsig'] == 0)
            & (graph_params['cumsig'].shift() == 1))

        # Place the marker at the specified distance above the upper bound
        signal_dict['sell_flat_marker'] = (
            graph_params['upper_bound']
            * signal_dict['sell_flat_signals']
            + flat_distance)
            #+ graph_params['upper_bound'].max()*flat_distance)
        
        signal_dict['sell_flat_marker'] = signal_dict[
            'sell_flat_marker'][signal_dict['sell_flat_signals']]
        
        # Add raw signal position for use in api
        signal_dict['data_markers']['closeLong'] = (
            graph_params['upper_bound']
            * signal_dict['sell_flat_signals']
        )

        signal_dict['data_markers']['closeLong'] = signal_dict['data_markers']['closeLong'][signal_dict['sell_flat_signals']]

        # Set the dates for the sell flat signals
        signal_dict['sell_flat_dates'] = prices.index[
            signal_dict['sell_flat_signals']]
        
        signal_dict['data_markers']['closeLongDates'] = signal_dict['sell_flat_dates']

        # Set the dates for the sell short signals
        signal_dict['sell_short_signals'] = (
            (graph_params['cumsig'] == -1)
            & (graph_params['cumsig'].shift() != -1))

        # Place the marker at the specified distance above the upper bound
        signal_dict['sell_short_marker'] = (
            graph_params['upper_bound']
            * signal_dict['sell_short_signals']
            + buy_sell_distance)
            #+ graph_params['upper_bound'].max()*buy_sell_distance)

        signal_dict['sell_short_marker'] = signal_dict[
            'sell_short_marker'][signal_dict['sell_short_signals']]
        
        # Add raw signal position for use in api
        signal_dict['data_markers']['openShort'] = (
            graph_params['upper_bound']
            * signal_dict['sell_short_signals']
        )

        signal_dict['data_markers']['openShort'] = signal_dict['data_markers']['openShort'][signal_dict['sell_short_signals']]

        # Set the dates for the sell short signals
        signal_dict['sell_short_dates'] = prices.index[
            signal_dict['sell_short_signals']]
        
        signal_dict['data_markers']['openShortDates'] = signal_dict['sell_short_dates']

        return signal_dict


    @staticmethod
    def _set_upper_lower(
        graph_params: dict) -> tuple[float, float]:
        # Set upper to the max of the upper bound and lower to the lowest
        # non-zero value of the lower bound, stripping zeros and nan values

        upper = graph_params['upper_bound'][
            graph_params['upper_bound'] != 0].dropna().max()
        lower = graph_params['lower_bound'][
            graph_params['lower_bound'] != 0].dropna().min()

        return upper, lower
