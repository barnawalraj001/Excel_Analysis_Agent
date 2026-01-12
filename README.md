# Excel Analysis Agent MVP

This project is an MVP for an intelligent agent that analyzes Excel/CSV files, extracts metadata, and uses an LLM to recommend and generate meaningful charts using Seaborn/Matplotlib.

## Features

- **Data Profiling**: Extracts column metadata and statistics without sending raw data to the LLM (privacy-first).
- **LLM Reasoning**: Uses OpenAI to decide which charts are most useful based on metadata.
- **Safe Execution**: Generates charts using pre-defined plotting functions (Seaborn/Matplotlib), ensuring no arbitrary code execution by the LLM.
- **FastAPI Backend**: Exposes a clean REST API for file upload and analysis.

## Architecture

1.  **File Loader**: Reads `.xlsx` or `.csv` files into Pandas.
2.  **Profiler**: Analyze the dataframe to produce a metadata summary (column types, missing values, stats).
3.  **LLM Agent**: Sends metadata to OpenAI with a structured output schema to request specific charts.
4.  **Chart Executor**: Receives the chart instructions and executes the corresponding Seaborn/Matplotlib code to save images locally.

## Setup Instructions

1.  **Clone the repository**.
2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure Environment**:
    - Copy `.env.example` to `.env`.
    - Add your OpenAI API Key: `OPENAI_API_KEY=sk-...`

## Running the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

## API Usage

**Endpoint**: `POST /analyze`

**Request**: Multipart form-data with `file` field.

**Example using Curl**:

```bash
curl -X POST -F "file=@your_data.csv" http://localhost:8000/analyze
```

**Response**:

```json
{
  "charts": [
    {
      "image_path": "outputs/charts/bar_chart_category_sales.png",
      "reason": "Shows comparison of sales across different categories."
    }
  ]
}
```

## Future Roadmap

- Interactive frontend.
- Caching of LLM results.
- Support for more chart types and customization.
- Docker support.
# Excel_Analysis_Agent
