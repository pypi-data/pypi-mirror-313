"""
Train test validation split function
"""

# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals

from sklearn.model_selection import train_test_split


def train_test_validation_split(
    data,
    col_target,
    train_percent=0.7,
    test_percent=0.15,
    validate_percent=0.15,
    random_state=2024,
    col_order=None,
):
    """
    Splits a Pandas dataframe into three subsets (train, val, and test).
    Function uses train_test_split (from sklearn) and stratify to receive
    the same ratio response (y, target) in each splits.
    If col_order is given, split is not shuffled, but divided by col_order order (eg. to train, test and validate on separate time spans).

    Parameters
    ----------
    data: pd.DataFrame
        Data to split
    col_target: str
        Name of column target
    train_percent: float (0,1)
        Percent of train data
    validate_percent: float (0,1)
        Percent of validate data
    test_percent: float (0,1)
        Percent of test data
    random_state: int, optional
        Random state for reproducibility. Defaults to 2024.
    col_order: string, optional. Defaults to None.
        Column to sort values for train/test/validation split by date. If none, standard split is done - data are shuffled.

    WARNING:
        Sum of train_percent, validate_percent and test_percent have to be equal 1.0.

    Returns
        X_train, X_test, X_val : Dataframes containing the three splits.
        y_train, y_test, y_val : Series with target variables
    """

    # assertions for params
    if train_percent + validate_percent + test_percent != 1.0:
        raise ValueError("Sum of train, validate and test is not 1.0")
    if col_target not in data.columns:
        raise ValueError(f"{col_target} is not a column in the dataframe")

    # ordering and dropping columns
    if col_order is not None:
        data = data.sort_values(by=col_order, ignore_index=True)
        data = data.drop(col_order, axis=1)
    y = data[[col_target]]
    data = data.drop(col_target, axis=1)

    # Split original dataframe into train and temp dataframes.
    train_temp_params = (
        {"stratify": y}
        if col_target is not None and col_order is None
        else {"shuffle": False} if col_target is not None and col_order is not None else {}
    )
    X_train, X_temp, y_train, y_temp = train_test_split(
        data, y, test_size=(1.0 - train_percent), random_state=random_state, **train_temp_params
    )

    # Split the temp dataframe into val and test dataframes.
    test_val_params = (
        {"stratify": y_temp}
        if col_target is not None and col_order is None
        else {"shuffle": False} if col_target is not None and col_order is not None else {}
    )
    validate_to_split = validate_percent / (validate_percent + test_percent)
    X_test, X_val, y_test, y_val = train_test_split(
        X_temp, y_temp, test_size=validate_to_split, random_state=random_state, **test_val_params
    )

    # assertions for outputs
    assert len(data) == len(X_train) + len(X_test) + len(
        X_val
    ), "Length of X is different than sum of x_train + x_test + x_val"
    assert len(y) == len(y_train) + len(y_test) + len(
        y_val
    ), "Length of y is different than sum of y_train + y_test + y_val"
    assert len(X_train) == len(y_train), "Length of X_train is different than y_train"
    assert len(X_test) == len(y_test), "Length of X_test is different than y_test"
    assert len(X_val) == len(y_val), "Length of X_val is different than y_val"

    return (
        X_train,
        X_test,
        X_val,
        y_train,
        y_test,
        y_val,
    )
