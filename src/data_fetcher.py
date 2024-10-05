import requests
import csv
import os
import pandas as pd

class DataFetcher:
    def __init__(self, input_file, output_file, keepa_api_key):
        self.keepa_api_key = keepa_api_key
        self.input_file = input_file
        self.output_file = output_file

    def fetch_product_data(self, asin):
        """Fetch product data for a given ASIN using the Keepa API."""
        url = f"https://api.keepa.com/product?key={self.keepa_api_key}&domain=1&asin={asin}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # Check if data is available for the ASIN
            if 'products' in data and len(data['products']) > 0:
                product = data['products'][0]  # Fetch first product in the response

                # Ensure that product is a valid dictionary
                if isinstance(product, dict):
                    # Check if imagesCSV is present and not None
                    imagesCSV = product.get('imagesCSV')
                    images = imagesCSV.split(',') if imagesCSV else []  # Safe splitting

                    stats = product.get('stats', {})  # Store stats safely

                    return {
                        'ASIN': asin,
                        'Title': product.get('title', ''),
                        'Image': images[0] if images else '',  # Main product image
                        'Weight (grams)': product.get('itemWeight', product.get('packageWeight', None)),
                        'Buy Box Current': product.get('buyBoxPrice', None),
                        'Sales Rank (30 Days Drop %)': stats.get('salesRankDrops30', None) if stats else None,
                        'Historic FBA Sellers': product.get('historical', {}).get('FBA', None),
                        'Referral Fee %': product.get('referralFeePercentage', None),
                        '# FBA Sellers Live': product.get('fbaCount', None),
                        'Saturation Score': product.get('saturationScore', None),
                        'FBA Fees': product.get('fbaFees', {}).get('total', None) if product.get('fbaFees') else None,
                        'Total FBA Stock': product.get('totalFBAStock', None),
                        'Purchasable Units': product.get('purchasableUnits', None),
                        'buyBoxUsedHistory': product.get('buyBoxUsedHistory', None),  # Buy Box used history
                        'Product Type': product.get('productType', None),
                        'Domain ID': product.get('domainId', None),
                        'Brand': product.get('brand', ''),
                        'Manufacturer': product.get('manufacturer', ''),
                        'Product Group': product.get('productGroup', ''),
                        'Description': product.get('description', ''),
                        'Features': product.get('features', []),  # List of features
                        'Categories': product.get('categories', []),  # Categories list
                        'Release Date': product.get('releaseDate', None),
                        'Publication Date': product.get('publicationDate', None),
                        'Binding': product.get('binding', ''),
                        'Color': product.get('color', ''),
                        'Size': product.get('size', ''),
                        'Part Number': product.get('partNumber', ''),
                        'Images': images,  # Full list of images
                        'Reviews': product.get('reviews', None),  # Reviews object
                        'Offers': product.get('offers', []),  # List of offers
                    }
                else:
                    print(f"Product data for ASIN {asin} is not valid.")
                    return {}
            else:
                print(f"No product data found for ASIN: {asin}")
                return {}
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for ASIN: {asin} - {e}")
            return {}

    def fetch_and_save_data(self):
        """Fetch product data for all ASINs and save to Excel."""
        product_data_list = []
        with open(self.input_file, newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            next(reader)  # Skip header row
            for row in reader:
                asin = row[0]
                print(f"Fetching data for ASIN: {asin}")
                product_data = self.fetch_product_data(asin)
                if product_data:
                    product_data_list.append(product_data)

        # Save to output Excel
        self.save_to_excel(product_data_list)

    def save_to_excel(self, product_data_list):
        """Save the product data to an Excel file."""
        if not product_data_list:
            print("No product data to save.")
            return
        
        df = pd.DataFrame(product_data_list)
        df.to_excel(self.output_file, index=False)

