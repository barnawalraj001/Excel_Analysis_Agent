from openai import AsyncOpenAI
import json
from ..config import settings
from ..schemas.chart_schema import ChartResponse

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def decide_charts(profile: dict) -> ChartResponse:
    """
    Uses an LLM to decide the most meaningful charts
    based strictly on dataset metadata.
    The LLM returns a JSON object that matches ChartResponse.
    """

    system_prompt = (
        "You are a senior data visualization expert.\n"
        "You must analyze dataset metadata and recommend up to 3 meaningful charts.\n\n"
        "IMPORTANT RULES:\n"
        "- Respond ONLY in valid JSON format.\n"
        "- Do NOT include any explanation outside JSON.\n"
        "- Use only the allowed chart types .\n"
        "- Avoid meaningless combinations.\n"
        "- Ensure x and y columns exist.\n"
        "- If data is insufficient, return an empty charts list.\n"
    )

    user_prompt = (
        "Given the following dataset profile, recommend charts.\n\n"
        "Return the response strictly as a JSON object matching this schema:\n"
        "{\n"
        '  "charts": [\n'
        "    {\n"
        '      "type": "bar | line | pie | scatter | heatmap",\n'
        '      "x": "column_name",\n'
        '      "y": "column_name (optional for some charts)",\n'
        '      "aggregation": "sum | mean | count | none",\n'
        '      "reason": "why this chart is useful"\n'
        "    }\n"
        "  ]\n"
        "}\n\n"
        f"DATASET PROFILE:\n{json.dumps(profile, indent=2)}"
    )

    response = await client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0,
        timeout=30
    )

    # Parse JSON safely
    try:
        content = response.choices[0].message.content
        parsed = json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM returned invalid JSON: {e}")

    return ChartResponse(**parsed)
