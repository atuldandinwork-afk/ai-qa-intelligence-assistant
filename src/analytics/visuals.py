import matplotlib.pyplot as plt


def plot_automation_trend(trend_df):
    """
    Returns a matplotlib figure for automation trend.
    """
    fig, ax = plt.subplots()

    ax.plot(
        trend_df["Sprint_Number"],
        trend_df["Automation_Coverage_%"],
        marker="o",
    )

    ax.set_title("Automation Coverage Trend")
    ax.set_xlabel("Sprint")
    ax.set_ylabel("Automation Coverage (%)")
    ax.grid(True)

    return fig
