from data_fetcher import DataFetcher

def main():
    # File paths
    input_file = '../data/input.csv'   # Path to your input CSV file
    output_file = '../data/output.xlsx' # Path to save the output Excel file
    
    # Keepa API key (replace with the actual API key)
    keepa_api_key = 'ftl9rmbprserlkqios5sv3md5bfrf5jpu2uahr7k6r854i78o56h939i2pcpv8r0'

    # Create an instance of DataFetcher and fetch data
    fetcher = DataFetcher(input_file, output_file, keepa_api_key)
    fetcher.fetch_and_save_data()

if __name__ == "__main__":
    main()
