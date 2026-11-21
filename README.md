# Urban Flood Risk & Rainfall Monitoring Analytics

## Files
- `flood_observations.json`: 2,600 synthetic environmental sensor observations
- `app.py`: Streamlit dashboard connecting to Azure Cosmos DB MongoDB API
- `requirements.txt`: dependencies
- `narrative.md`: written project narrative

## 1. Azure setup
Create an Azure Cosmos DB account using the MongoDB-compatible API. Create database `FloodMonitoring` and collection `observations`. Configure network access to permit your machine (avoid unrestricted access where possible). Retrieve your MongoDB connection string and keep it secret.

## 2. Import JSON
Use a MongoDB-compatible import tool such as `mongoimport`:
```bash
mongoimport --uri "YOUR_MONGODB_URI" --db FloodMonitoring --collection observations --file flood_observations.json --jsonArray
```
Check that the JSON import tool and URI syntax match your Cosmos DB account configuration.

## 3. Run locally
Python 3.9+ recommended:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Set environment variables:
```bash
export MONGODB_URI='YOUR_MONGODB_URI'
export MONGODB_DATABASE='FloodMonitoring'
export MONGODB_COLLECTION='observations'
streamlit run app.py
```
Windows PowerShell:
```powershell
$env:MONGODB_URI='YOUR_MONGODB_URI'
$env:MONGODB_DATABASE='FloodMonitoring'
$env:MONGODB_COLLECTION='observations'
streamlit run app.py
```

## 4. Notes
This project is educational and uses synthetic readings and fictionalized location points. Risk labels are simple demonstration rules, not validated flood thresholds or actual warnings. Protect credentials and restrict database network access.
