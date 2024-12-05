from pandas import Series, concat


def calculate_peak_prominence(series: Series) -> Series:
    """
    Get peak prominence for each value in a numerical series
    """
    # Calculate the absolute value of each element (we're comparing absolute magnitudes)
    abs_series = series.abs()

    # Shift the series to get the previous and next values
    left_rolling = abs_series.shift(1)  # previous element
    right_rolling = abs_series.shift(-1)  # next element

    # For boundary cases, assume the value itself to avoid NaNs
    left_rolling.fillna(abs_series, inplace=True)
    right_rolling.fillna(abs_series, inplace=True)

    # Identify peaks by checking if the current value is larger than both neighbors
    is_peak = ((abs_series > left_rolling) & (abs_series > right_rolling)) | ((abs_series < left_rolling) & (abs_series < right_rolling))

    # Calculate prominence for peaks only
    prominence = Series(0, index=series.index)  # Initialize with zeros
    prominence[is_peak] = (
        abs_series[is_peak]
        - concat([left_rolling, right_rolling], axis=1).min(axis=1)[is_peak]
    )

    return prominence.abs()
