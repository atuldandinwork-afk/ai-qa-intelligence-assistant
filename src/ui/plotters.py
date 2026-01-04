import matplotlib.pyplot as plt

def render_execution_trend(trend_df):
    fig, ax = plt.subplots()

    ax.plot(
        trend_df["Sprint_Number"],
        trend_df["Pass_Rate"] * 100,
        marker="o",
        linewidth=2
    )

    ax.set_title("Execution Pass Rate Trend")
    ax.set_xlabel("Sprint")
    ax.set_ylabel("Pass Rate (%)")
    ax.set_ylim(0, 100)
    ax.grid(True)

    return fig

def render_automation_coverage(df):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    ax.bar(
        df["Module"],
        df["Automation_Coverage_%"],
    )

    ax.set_title("Automation Coverage by Module")
    ax.set_ylabel("Coverage (%)")
    ax.set_ylim(0, 100)
    ax.set_xticklabels(df["Module"], rotation=45, ha="right")
    ax.grid(axis="y")

    return fig

def render_defect_distribution(df, by="Severity"):
    import matplotlib.pyplot as plt

    counts = df[by].value_counts()

    fig, ax = plt.subplots()
    ax.bar(counts.index, counts.values)

    ax.set_title(f"Defect Distribution by {by}")
    ax.set_ylabel("Count")
    ax.grid(axis="y")

    return fig

