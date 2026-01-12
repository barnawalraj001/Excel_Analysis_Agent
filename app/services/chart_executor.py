import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import uuid
import os
import base64
from datetime import datetime
from ..config import settings
from ..schemas.chart_schema import ChartRequest
from ..utils.helpers import logger

# Use non-interactive backend for servers
plt.switch_backend("Agg")


def execute_charts(df: pd.DataFrame, charts: list[ChartRequest]) -> list[dict]:
    """
    Executes chart plans safely using seaborn/matplotlib
    and returns base64-encoded images.
    """
    results = []

    # Ensure output directory exists (safe for deploy)
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)

    for chart in charts:
        try:
            plt.figure(figsize=(10, 6))
            sns.set_theme(style="whitegrid")

            filename = f"{chart.type}_{uuid.uuid4().hex[:8]}.png"
            output_path = os.path.join(settings.OUTPUT_DIR, filename)

            plot_df = df.copy()

            # ----------------------------
            # Aggregation (if requested)
            # ----------------------------
            if chart.aggregation != "none" and chart.y:
                if not pd.api.types.is_numeric_dtype(plot_df[chart.y]):
                    raise ValueError("Aggregation requires numeric y column")

                plot_df = (
                    plot_df
                    .groupby(chart.x, as_index=False)[chart.y]
                    .agg(chart.aggregation)
                )

            # ----------------------------
            # FINAL DATETIME NORMALIZATION
            # ----------------------------
            for col in [chart.x, chart.y]:
                if col and col in plot_df.columns:
                    # pandas datetime64
                    if pd.api.types.is_datetime64_any_dtype(plot_df[col]):
                        plot_df[col] = plot_df[col].dt.strftime("%Y-%m")
                    # python datetime in object column
                    elif plot_df[col].dtype == "object":
                        if plot_df[col].dropna().apply(
                            lambda v: isinstance(v, datetime)
                        ).any():
                            plot_df[col] = plot_df[col].astype(str)

            # ----------------------------
            # Plotting logic
            # ----------------------------
            if chart.type == "bar":
                sns.barplot(data=plot_df, x=chart.x, y=chart.y)

            elif chart.type == "line":
                plot_df = plot_df.sort_values(chart.x)
                sns.lineplot(data=plot_df, x=chart.x, y=chart.y)

            elif chart.type == "scatter":
                sns.scatterplot(data=plot_df, x=chart.x, y=chart.y)

            elif chart.type == "heatmap":
                corr = df.select_dtypes(include="number").corr()
                sns.heatmap(corr, annot=True, cmap="coolwarm")

            elif chart.type == "pie":
                if plot_df[chart.y].sum() == 0:
                    raise ValueError("Pie chart values sum to zero")
                plt.pie(
                    plot_df[chart.y],
                    labels=plot_df[chart.x],
                    autopct="%1.1f%%"
                )

            # ----------------------------
            # Finalize chart
            # ----------------------------
            title = f"{chart.type.title()} Chart"
            title += f": {chart.x}" if not chart.y else f": {chart.x} vs {chart.y}"
            plt.title(title)
            plt.xticks(rotation=45)
            plt.tight_layout()

            plt.savefig(output_path)
            plt.close()

            # ----------------------------
            # Convert image to Base64
            # ----------------------------
            with open(output_path, "rb") as img:
                image_base64 = base64.b64encode(img.read()).decode("utf-8")

            # Optional: cleanup file to keep service stateless
            os.remove(output_path)

            results.append({
                "type": chart.type,
                "reason": chart.reason,
                "image_src": f"data:image/png;base64,{image_base64}"
            })

        except Exception as e:
            logger.error(f"Failed to generate chart {chart}: {e}")
            plt.close()

    return results
