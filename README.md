# Warehouse Management System (WMS) - SKU Mapper Web App

## Overview

This project is a Minimum Viable Product (MVP) for a Warehouse Management System (WMS) designed to preprocess sales data, map localized Stock Keeping Units (SKUs) to Master SKUs (MSKUs), and update inventory across warehouses. Built using Streamlit, the web application provides an intuitive interface for uploading CSV files, mapping SKUs, and managing inventory. The system supports fuzzy matching for automatic SKU-to-MSKU mapping, manual mapping for unmapped SKUs, and inventory updates, with plans for integration with a relational database (e.g., Baserow) and AI-driven querying.

## Features

* **SKU Mapping**: Automatically maps localized SKUs to MSKUs using fuzzy matching (80% similarity threshold), with manual mapping for unmapped SKUs.
* **Inventory Management**: Subtracts sales quantities from inventory based on MSKU mappings, accounting for warehouse locations (e.g., main and FBA).
* **Web Interface**: Streamlit-based UI for uploading CSV files, viewing unmapped SKUs, assigning MSKUs, and displaying updated inventory.
* **Logging**: Records mapping activities and errors in `sku_mapping.log` for debugging.
* **Output Files**: Saves SKU mappings to `sku_mappings.csv` and updated inventory to `updated_inventory.csv`.
* **Extensibility**: Designed for future integration with Baserow for relational database management and text-to-SQL querying.

## Prerequisites

* Python 3.8+
* Python Libraries:

  ```bash
  pip install streamlit pandas fuzzywuzzy python-Levenshtein
  ```
* CSV Files:

  * `file1` (Master SKUs): Expected columns include `MSKU`, `Quantity`, `Fulfillment Center`
  * `order.csv` (Sales Data): Expected columns include `SKU`, `Quantity`, `Order Date`
  * `Gl FK.csv` (Sales Data): Expected columns include `SKU`, `Quantity`, `Product`
* GitHub Account: For deploying to Streamlit Community Cloud
* Baserow Account (Optional): For future database integration ([https://baserow.io](https://baserow.io))

## Project Structure

```
wms-sku-mapper/
├── app.py                # Main Streamlit app with SKUMapper class and UI
├── requirements.txt      # Python dependencies
├── sku_mappings.csv      # Output: SKU to MSKU mappings
├── updated_inventory.csv # Output: Updated inventory after sales
├── sku_mapping.log       # Log file for mapping activities
└── README.md             # This file
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd wms-sku-mapper
```

### 2. Install Dependencies

Create a `requirements.txt` file with:

```
streamlit
pandas
fuzzywuzzy
python-Levenshtein
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Prepare Data

* Place `file1`, `order.csv`, and `Gl FK.csv` in a local directory or ensure they are accessible for upload.
* Verify CSV files have the expected columns (`MSKU`, `SKU`, `Quantity`). Adjust column names in `app.py` if needed.

### 4. Run Locally

```bash
streamlit run app.py
```

Access the app at: [http://localhost:8501](http://localhost:8501)

### 5. Deploy to Streamlit Community Cloud

#### Push to GitHub

```bash
git init
git add app.py requirements.txt README.md
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

#### Deploy

* Sign up at [Streamlit Community Cloud](https://streamlit.io/cloud)
* Connect your GitHub account
* Click "New App", select your repository, branch (`main`), and file (`app.py`)
* Deploy the app and access it via the provided URL (e.g., [https://your-app-name.streamlit.app](https://your-app-name.streamlit.app))

## Usage

### Upload Files

* Use the **"Master SKU File"** uploader to select `file1` (CSV with MSKUs)
* Use the **"Sales Data Files"** uploader to select `order.csv` and `Gl FK.csv` (supports multiple files)
* Click **"Load Files"** to process the CSVs

### Map SKUs

* Click **"Map SKUs"** to run automatic fuzzy matching
* Unmapped SKUs appear in a dropdown. Select an SKU, enter an MSKU, and click **"Assign MSKU"** to map manually
* Mappings are saved to `sku_mappings.csv`

### Update Inventory

* Click **"Update Inventory"** to subtract sales quantities from the master inventory
* View the updated inventory in the app and download `updated_inventory.csv`

### View Logs

* Check `sku_mapping.log` for mapping activities and errors (local only, not on Streamlit Cloud unless integrated with external storage)

## Example Data

**Input:**

* `file1`: `MSKU: APPLE_GOLD`, `Quantity: 100`, `Fulfillment Center: FBA`
* `order.csv`: `SKU: GLD`, `Quantity: 20`
* `Gl FK.csv`: `SKU: Golden_Apple`, `Quantity: 30`
* Mapping: `GLD` → `APPLE_GOLD`, `Golden_Apple` → `APPLE_GOLD`

**Output:**

* `sku_mappings.csv`:

  ```
  SKU,MSKU
  GLD,APPLE_GOLD
  Golden_Apple,APPLE_GOLD
  ```
* `updated_inventory.csv`:

  ```
  MSKU,Available Quantity,Fulfillment Center
  APPLE_GOLD,50,FBA
  ```

## Future Enhancements

* **Baserow Integration**: Sync `sku_mappings.csv` and `updated_inventory.csv` with Baserow tables using its API
* **Text-to-SQL**: Implement LlamaIndex or LangChain for AI-driven queries (e.g., "Show sales for MSKU X in June 2025")
* **Visualizations**: Add Plotly or Chart.js charts for sales and inventory metrics
* **Combo Products**: Extend SKUMapper to support multiple SKUs per MSKU
* **Persistent Storage**: Integrate with cloud storage (e.g., Google Drive) for saving output files on Streamlit Cloud

## Troubleshooting

* **CSV Errors**: Ensure CSV files have required columns (`MSKU`, `SKU`, `Quantity`). Update `app.py` if column names differ
* **Fuzzy Matching**: Adjust the similarity threshold (default: 80) in `map_skus` if too many SKUs are unmapped
* **File Persistence**: Output files (`sku_mappings.csv`, `updated_inventory.csv`) are temporary on Streamlit Cloud. Use Baserow or cloud storage for persistence
* **Deployment Issues**: Check Streamlit Cloud logs for dependency or file path errors
* **Logging**: `sku_mapping.log` is available locally but not on Streamlit Cloud unless redirected to external storage

## Notes

* **Streamlit Cloud Limitations**: File uploads and outputs are session-based. For persistent data, integrate with Baserow or a cloud storage service
* **Column Names**: The app assumes specific column names (`MSKU`, `SKU`, `Quantity`). Modify `app.py` to match your CSV structure
* **Security**: For production use, add authentication to restrict access to the app

## Contact

For support, open an issue on the GitHub repository or contact the developer at \[[surajtamatta8379911589@gmail.com](mailto:surajtamatta8379911589@gmail.com)].
