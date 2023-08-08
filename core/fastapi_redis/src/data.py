import pandas as pd


def session_data_preprocessing(session_df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess session data

    Args:
        session_df (pd.DataFrame): raw session DataFrame

    Returns:
        pd.DataFrame: session DataFrame after preprocessing
    """
    # Remove the index columns
    session_df = session_df.iloc[:, 1:]

    # Remove duplicated rows in session data
    session_df.drop_duplicates(
        subset=["session_id", "position_in_list", "venue_id", "purchased"],
        keep="last",
        inplace=True,
    )

    # keep only venues that has been seen by users:
    # 1. has_seen_venue_in_this_session=True
    df_list = [session_df[session_df["has_seen_venue_in_this_session"] == True]]

    # 2. When has_seen_venue_in_this_session is missing,
    # only keep venues before the purchased item(<=position_in_list)
    nan_sessions = session_df[session_df["has_seen_venue_in_this_session"].isna()]
    nan_sessions_purchased_index = nan_sessions[nan_sessions["purchased"] == True][
        ["session_id", "position_in_list"]
    ].values.tolist()
    for session, purchased_index in nan_sessions_purchased_index:
        df = nan_sessions[
            (nan_sessions["session_id"] == session)
            & (nan_sessions["position_in_list"] <= purchased_index)
        ]
        df_list.append(df)

    # Concatenate dataframe from 1 and 2
    session_df = pd.concat(df_list)
    return session_df


def venue_data_preprocessing(venue_df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess venue data

    Args:
        session_df (pd.DataFrame): raw venue DataFrame

    Returns:
        pd.DataFrame: venue DataFrame after preprocessing
    """
    # Remove the index columns
    venue_df = venue_df.iloc[:, 1:]

    # Impute missing values for venues data:
    missing_cols = ["conversions_per_impression", "rating", "retention_rate"]
    # Impute missing value with 30th percentile
    imputed_values = venue_df[missing_cols].quantile(0.3).values.tolist()
    imputed_dict = {a: b for a, b in zip(missing_cols, imputed_values)}
    venue_df.fillna(value=imputed_dict, inplace=True)

    # Scale venue features into range [0,1]
    venue_df["rating"] /= venue_df["rating"].max()
    venue_df["price_range"] /= venue_df["price_range"].max()
    venue_df["popularity"] /= venue_df["popularity"].max()

    return venue_df
