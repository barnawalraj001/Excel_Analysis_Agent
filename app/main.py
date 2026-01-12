from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .services import file_loader, profiler, llm_agent, chart_executor
from .utils.helpers import logger
import traceback
import os

app = FastAPI(
    title="Excel Analysis Agent",
    version="1.0.0",
    description="Upload Excel/CSV and receive AI-generated charts"
)

# ------------------------------------
# CORS (important for Varticas / web)
# ------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------
# Health Check (optional but useful)
# ------------------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}

# ------------------------------------
# Main Analysis Endpoint
# ------------------------------------
@app.post("/analyze")
async def analyze_data(file: UploadFile = File(...)):
    logger.info(f"Received file: {file.filename}")

    try:
        # 1️⃣ Load file into DataFrame
        df = await file_loader.load_file(file)
        logger.info("File loaded successfully")

        if df.empty:
            raise ValueError("Uploaded file contains no data")

        # 2️⃣ Profile dataset (NO raw data to LLM)
        profile = profiler.profile_dataframe(df)
        logger.info("Data profiling complete")

        # 3️⃣ LLM decides chart plan
        chart_plan = await llm_agent.decide_charts(profile)
        logger.info(f"LLM suggested {len(chart_plan.charts)} charts")

        if not chart_plan.charts:
            return {
                "status": "success",
                "charts": [],
                "message": "No meaningful charts could be generated"
            }

        # 4️⃣ Execute charts (returns BASE64 images)
        generated_charts = chart_executor.execute_charts(
            df, chart_plan.charts
        )
        logger.info("Charts generated successfully")

        return {
            "status": "success",
            "charts": generated_charts
        }

    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail="Failed to analyze uploaded file"
        )
