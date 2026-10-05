# Authentic Adventure Travel Concierge AI

A conversational travel assistant designed for budget-conscious adventurers seeking local culture, authentic human interactions, and walking tours capped at 4 hours maximum duration.

---

## 🌟 What This Agent Does

The **Authentic Adventure Travel Concierge AI** helps travelers plan, discover, and visualize local walking tours and cultural experiences. Based on the implemented codebase, the agent provides:

- **Memory & Personalization**: Automatically tracks user travel preferences, favorite cities, and past trips across sessions using Vertex AI Memory Bank.
- **Walking Tour Catalog**: Searches, details, and creates walking tours capped at 4 hours duration stored in Google Cloud Firestore.
- **Visual Travel Postcards**: Generates visual travel postcard images for suggested destinations using `gemini-3.1-flash-lite-image`.
- **Short Tour Preview Videos**: Generates short video clips for walking tour items or scenic spots using Google's Omni model (`gemini-omni-flash-preview`).
- **Location & Map Lookups**: Geocodes locations and discovers nearby places using Google Maps APIs.
- **Weather & Walking Conditions**: Provides real-time weather forecasts to ensure ideal walking conditions.
- **Currency Conversion**: Converts travel budgets and tour prices across multiple currencies.
- **Code Execution Sandbox**: Runs Python code in a secure sandbox to calculate walking pace, route durations, and budget math.
- **Structured A2UI Cards**: Renders response surfaces dynamically as structured A2UI cards (Cards, Columns, Rows, Text, and Images).

---

## 🛠️ Integrated Google Cloud Services & Tools

This repository implements and wires up the following Google Cloud services and custom tools:

| Service / Tool | Implementation File | Description |
| :--- | :--- | :--- |
| **Vertex AI Memory Bank** | [app/agent.py](file:///config/Desktop/Session1/simple-agent/app/agent.py) | Long-term memory persistence using `PreloadMemoryTool` & `generate_memories_callback`. |
| **Google Cloud Firestore** | [app/firestore_tools.py](file:///config/Desktop/Session1/simple-agent/app/firestore_tools.py) | Tour database operations (`list_walking_tours`, `get_walking_tour_details`, `add_walking_tour`). |
| **Google Cloud Storage** | [app/image_tool.py](file:///config/Desktop/Session1/simple-agent/app/image_tool.py), [app/video_tool.py](file:///config/Desktop/Session1/simple-agent/app/video_tool.py) | Assets bucket storing generated postcards and video previews with public HTTPS access. |
| **Image Generation** | [app/image_tool.py](file:///config/Desktop/Session1/simple-agent/app/image_tool.py) | Generates travel postcards using `gemini-3.1-flash-lite-image` in `global` region. |
| **Video Generation** | [app/video_tool.py](file:///config/Desktop/Session1/simple-agent/app/video_tool.py) | Generates preview videos using `gemini-omni-flash-preview` in `global` region via Interactions API. |
| **Google Maps API** | [app/maps_tools.py](file:///config/Desktop/Session1/simple-agent/app/maps_tools.py) | `geocode_address` & `find_nearby_places` for place discovery and location coordinates. |
| **Weather Forecast** | [app/weather_tool.py](file:///config/Desktop/Session1/simple-agent/app/weather_tool.py) | `get_city_weather_forecast` fetching current weather conditions for outdoor tours. |
| **Currency Exchange** | [app/currency_tool.py](file:///config/Desktop/Session1/simple-agent/app/currency_tool.py) | `get_currency_exchange_rates` for real-time currency conversion. |
| **Code Sandbox** | [app/agent.py](file:///config/Desktop/Session1/simple-agent/app/agent.py) | `AgentEngineSandboxCodeExecutor` for walking duration, distance, and budget calculations. |
| **A2UI Rendering** | [app/a2ui_utils.py](file:///config/Desktop/Session1/simple-agent/app/a2ui_utils.py) | Intercepts agent responses to format and render native A2UI component cards. |

> 📌 **Note on Planned Features**: Local community event search mentioned in early project planning is *planned, not yet implemented*.

---

## 🚀 Setup & Run Instructions

### Prerequisites
- Python 3.11+
- `uv` package manager (`pip install uv`)
- `google-agents-cli` (`uv tool install google-agents-cli`)
- Google Cloud SDK authenticated with Application Default Credentials (`gcloud auth application-default login`)

### Installation

1. Clone the repository and navigate to the project folder:
   ```bash
   cd simple-agent
   ```

2. Install dependencies:
   ```bash
   agents-cli install
   ```

### Running Locally

Launch the local development environment and interactive chat UI:

```bash
agents-cli playground
```

To run the custom chat frontend proxy:

```bash
cd frontend
pip install -r requirements.txt
python main.py
```

### Testing

Run unit and integration test suites:

```bash
uv run pytest tests/unit tests/integration
```

---

## 📁 Repository Structure

```
simple-agent/
├── app/
│   ├── agent.py               # Main ADK Agent setup and instruction schema
│   ├── a2ui_utils.py          # A2UI callback and schema manager
│   ├── firestore_tools.py     # Firestore database tools for walking tours
│   ├── image_tool.py          # Image generation tool (gemini-3.1-flash-lite-image)
│   ├── video_tool.py          # Video generation tool (gemini-omni-flash-preview)
│   ├── maps_tools.py           # Google Maps geocoding and nearby search
│   ├── weather_tool.py        # Weather forecast lookup
│   └── currency_tool.py       # Currency exchange rate conversion
├── frontend/                  # FastAPI proxy & A2UI chat web interface
├── tests/                     # Unit and integration test suites
├── agents-cli-manifest.yaml   # Agents CLI deployment manifest
└── pyproject.toml             # Project dependencies and environment configuration
```
