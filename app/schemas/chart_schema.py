from pydantic import BaseModel, Field
from typing import List, Literal, Optional

class ChartRequest(BaseModel):
    type: Literal["bar", "line", "pie", "scatter", "heatmap"] = Field(..., description="The type of chart to generate.")
    x: str = Field(..., description="The column name for the x-axis.")
    y: Optional[str] = Field(None, description="The column name for the y-axis (optional for some counts).")
    aggregation: Literal["sum", "mean", "count", "none"] = Field("none", description="Aggregation method to apply.")
    reason: str = Field(..., description="Explanation of why this chart is useful.")

class ChartResponse(BaseModel):
    charts: List[ChartRequest] = Field(..., description="List of recommended charts (max 3).")
