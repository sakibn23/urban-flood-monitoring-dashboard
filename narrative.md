# Urban Flood Risk & Rainfall Monitoring Analytics
## Project Narrative

### 1. Purpose
This project demonstrates a cloud-based environmental monitoring and analytics dashboard designed to explore rainfall patterns, water-level observations, and potential flood-risk indicators across monitoring zones in a fictional urban area. It illustrates how environmental sensor data could be stored in a document database and analyzed to support municipal planning and situational awareness. All data and locations in this prototype are synthetic.

### 2. Context and problem
Urban flooding can disrupt transportation, infrastructure, housing, and public services. Monitoring rainfall and water levels at multiple locations can help environmental teams identify patterns, prioritize inspections, and understand where additional monitoring or drainage assessment may be warranted. This prototype explores those use cases using simulated sensor records.

### 3. Database and document model
The dataset is stored in Azure Cosmos DB using the MongoDB-compatible API. The database is `FloodMonitoring`, with a collection named `observations`. Each document contains an observation identifier, sensor identifier, timestamp, nested location information, nested environmental measurements, sensor status, and an illustrative risk label. The nested structure represents a flexible document model for sensor observations and metadata.

The Streamlit application runs locally and connects to the cloud database through PyMongo. Connection details are stored in environment variables rather than embedded in the source code. The dataset contains 2,600 synthetic observation records.

### 4. Dashboard metrics and visualizations
The dashboard displays the number of observations, average rainfall, peak recorded water level, and count of observations labelled high risk. Interactive filters allow users to select monitoring zones, risk levels, and a date range. Visualizations include daily rainfall and water-level trends, average rainfall by zone, high-risk observation counts by zone, a map of the latest selected sensor observations, and a scatter plot exploring rainfall and water-level relationships. A table lists high-risk observations and the dashboard allows filtered records to be downloaded as CSV.

### 5. Analytical value and decision support
Rainfall and water-level trends may help users identify periods of increased environmental activity. Zone-level comparisons can highlight areas warranting further inspection or monitoring. The rainfall-versus-water-level plot can support exploratory investigation of how measurements co-vary. Sensor status helps distinguish available monitoring devices from those reported offline or under maintenance.

In a realistic municipal or environmental-management context, these indicators could inform field inspections, drainage maintenance planning, monitoring-site placement, resource coordination, and communication planning. The dashboard is exploratory: it does not issue real flood warnings, predict flooding, or establish causation.

### 6. Risk-label methodology and limitations
For demonstration purposes, observations are labelled Low, Moderate, or High using simple rules based on rainfall and water-level readings. These illustrative thresholds are not calibrated to a real river, drainage system, city, or hydrological model. The synthetic observations are not actual weather or sensor readings, and the geographic points are fictionalized. A real deployment would require verified sensors, calibrated thresholds, data validation, hydrological expertise, reliable timestamps, security controls, and integration with authorized emergency-management procedures.

### 7. Conclusion
This project demonstrates an end-to-end cloud analytics workflow involving synthetic IoT-style environmental data, a MongoDB-compatible database hosted on Azure, and an interactive local Streamlit dashboard. It illustrates how document-oriented storage and visual analytics can support exploratory environmental monitoring and help organizations investigate potential risks and resource needs.
