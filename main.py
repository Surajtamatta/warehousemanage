import pandas as pd
import streamlit as st
from fuzzywuzzy import process
import logging
import os
import re

# Set up logging
logging.basicConfig(filename='sku_mapping.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class SKUMapper:
    def __init__(self):
        self.msku_data = None
        self.sales_data = []
        self.mappings = {}  # SKU to MSKU mappings
        self.unmapped_skus = []

    def load_master_data(self, file):
        """Load master SKU data from uploaded file."""
        try:
            self.msku_data = pd.read_csv(file)
            logging.info(f"Loaded master SKU data from {file.name}")
        except Exception as e:
            logging.error(f"Error loading master data: {e}")
            raise

    def load_sales_data(self, files):
        """Load sales data from uploaded files."""
        self.sales_data = []
        for file in files:
            try:
                df = pd.read_csv(file)
                self.sales_data.append(df)
                logging.info(f"Loaded sales data from {file.name}")
            except Exception as e:
                logging.error(f"Error loading sales data from {file.name}: {e}")
                raise

    def validate_sku(self, sku):
        """Validate SKU format (e.g., alphanumeric, specific length)."""
        pattern = r'^[A-Za-z0-9_-]+$'
        return bool(re.match(pattern, str(sku)))

    def map_skus(self):
        """Map localized SKUs to MSKUs using fuzzy matching."""
        if self.msku_data is not None and not self.msku_data.empty:
            msku_list = self.msku_data['MSKU'].dropna().unique()
            for df in self.sales_data:
                skus = df['SKU'].dropna().unique()
                for sku in skus:
                    if not self.validate_sku(sku):
                        logging.warning(f"Invalid SKU format: {sku}")
                        self.unmapped_skus.append(sku)
                        continue
                    if sku not in self.mappings:
                        match, score = process.extractOne(sku, msku_list)
                        if score > 80:  # Threshold for auto-mapping
                            self.mappings[sku] = match
                            logging.info(f"Auto-mapped SKU {sku} to MSKU {match}")
                        else:
                            self.unmapped_skus.append(sku)
                            logging.info(f"SKU {sku} unmapped, requires manual mapping")

    def update_inventory(self):
        """Subtract sales quantities from inventory based on MSKU mappings."""
        inventory = self.msku_data.copy()
        inventory['Available Quantity'] = inventory['Quantity']

        for df in self.sales_data:
            for _, row in df.iterrows():
                sku = row['SKU']
                quantity = row['Quantity']
                msku = self.mappings.get(sku)
                if msku:
                    mask = inventory['MSKU'] == msku
                    if inventory[mask].empty:
                        logging.warning(f"No inventory found for MSKU {msku}")
                        continue
                    inventory.loc[mask, 'Available Quantity'] -= quantity
                    logging.info(f"Subtracted {quantity} from MSKU {msku}")

        return inventory

    def save_mappings(self, file_path):
        """Save SKU to MSKU mappings to a CSV file."""
        mappings_df = pd.DataFrame(list(self.mappings.items()), columns=['SKU', 'MSKU'])
        mappings_df.to_csv(file_path, index=False)
        logging.info(f"Saved mappings to {file_path}")

# Streamlit app
def main():
    st.title("SKU to MSKU Mapper")
    
    # Initialize session state
    if 'mapper' not in st.session_state:
        st.session_state.mapper = SKUMapper()
    if 'unmapped_skus' not in st.session_state:
        st.session_state.unmapped_skus = []
    
    # File uploaders
    st.header("Upload Files")
    master_file = st.file_uploader("Master SKU File (CSV)", type="csv")
    sales_files = st.file_uploader("Sales Data Files (CSV)", type="csv", accept_multiple_files=True)

    # Load files
    if st.button("Load Files") and master_file and sales_files:
        try:
            st.session_state.mapper.load_master_data(master_file)
            st.session_state.mapper.load_sales_data(sales_files)
            st.success("Files loaded successfully!")
        except Exception as e:
            st.error(f"Error loading files: {e}")

    # Map SKUs
    if st.button("Map SKUs"):
        st.session_state.mapper.map_skus()
        st.session_state.unmapped_skus = st.session_state.mapper.unmapped_skus
        if st.session_state.unmapped_skus:
            st.warning("Some SKUs require manual mapping. See below.")
        else:
            st.success("All SKUs mapped successfully!")

    # Display and map unmapped SKUs
    if st.session_state.unmapped_skus:
        st.header("Unmapped SKUs")
        selected_sku = st.selectbox("Select SKU to Map", st.session_state.unmapped_skus)
        msku = st.text_input("Enter MSKU")
        if st.button("Assign MSKU") and selected_sku and msku:
            st.session_state.mapper.mappings[selected_sku] = msku
            st.session_state.unmapped_skus.remove(selected_sku)
            st.session_state.mapper.save_mappings("sku_mappings.csv")
            st.success(f"Mapped {selected_sku} to {msku}")
            st.rerun()

    # Update inventory
    if st.button("Update Inventory"):
        inventory = st.session_state.mapper.update_inventory()
        inventory.to_csv("updated_inventory.csv", index=False)
        st.session_state.inventory = inventory
        st.success("Inventory updated and saved to updated_inventory.csv")

    # Display inventory
    if 'inventory' in st.session_state:
        st.header("Updated Inventory")
        st.dataframe(st.session_state.inventory)

if __name__ == "__main__":
    main()