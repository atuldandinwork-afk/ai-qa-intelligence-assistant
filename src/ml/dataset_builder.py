import pandas as pd

from src.ml.features import (
    build_execution_features,
    build_automation_features,
)


def build_ml_dataset() -> pd.DataFrame:
    """
    Builds the final ML-ready dataset by combining
    execution (sprint-level) and automation (module-level) features.
    """

    # Execution features (Module + Sprint granularity)
    df_exec = build_execution_features()

    # Automation features (Module-level)
    df_auto = build_automation_features()

    # Merge automation features into execution timeline
    df_ml = df_exec.merge(
        df_auto,
        on="Module",
        how="left",
    )
    df_ml["unstable"] = (df_ml["pass_rate"] < 0.7).astype(int)
    return df_ml

    



if __name__ == "__main__":
    df_ml = build_ml_dataset()
    # print(df_ml[["Module", "Sprint_Number", "pass_rate", "unstable"]].head())
    # print("\nLabel distribution:")
    # print(df_ml["unstable"].value_counts())

