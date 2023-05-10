import sys
import csv
import json
import gzip
import os


def main(args):
    """main() will be run if you run this script directly"""
    dynamodb_jsons_to_csv()

def dynamodb_jsons_to_csv(input_dir='./download', output_file='unmarshalled_dynamodb.csv'):
    # Get a list of all the .json.gz files in the input directory
    files = [f for f in os.listdir(input_dir) if f.endswith('.json.gz')]
    if not files:
        print('No .json.gz files found in the input directory.')
        return

    # Extract headers from all the JSON objects
    headers = set()
    for filename in files:
        with gzip.open(os.path.join(input_dir, filename), 'rb') as f:
            for line in f:
                data = json.loads(line.decode('utf-8'))
                headers.update(data.get('Item', {}).keys())

    # Write the extracted headers to CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        # Write the data to CSV file
        for filename in files:
            with gzip.open(os.path.join(input_dir, filename), 'rb') as g:
                for line in g:
                    data = json.loads(line.decode('utf-8'))
                    row = []
                    for header in headers:
                        value = ''
                        if 'Item' in data and header in data['Item']:
                            header_data = data['Item'][header]
                            if isinstance(header_data, dict):
                                value = header_data.get(list(header_data.keys())[0], '')
                        row.append(value)
                    writer.writerow(row)
                    #row = [data.get('Item', {}).get(header, {}).get(list(data['Item'][header].keys())[0], '') for header in headers]
                    #writer.writerow(row)

    print(f'{len(files)} files converted to CSV format.')


def dynamodb_jsons_to_json():
    # Set the directory path where your .json.gz files are located
    directory_path = "./download"

    # Set the output file path
    output_file_path = "unmarshalled_dynamodb.json"

    not_first = False

    # Create or overwrite the output file
    with open(output_file_path, "w") as output_file:
        output_file.write("[")
        # Loop through all .json.gz files in the directory
        for filename in os.listdir(directory_path):
            if filename.endswith(".json.gz"):

                # Open the .json.gz file and read its contents line by line
                with gzip.open(os.path.join(directory_path, filename), "rb") as f:
                    for line in f:
                        # Decode the line and parse it as a JSON object
                        data = json.loads(line.decode("utf-8"))

                        # Extract the item object from the DynamoDB JSON format
                        item = data["Item"]

                        if not_first:
                            output_file.write(",\n")
                        not_first = True
                        # Convert the DynamoDB JSON format to the desired output format
                        output_data = {}
                        for key, value in item.items():
                            for data_type, data_value in value.items():
                                if data_type in ("S", "N"):
                                    try:
                                        output_data[key] = int(data_value)
                                    except ValueError:
                                        try:
                                            output_data[key] = float(data_value)
                                        except ValueError:
                                            output_data[key] = data_value
                                elif data_type == "B":
                                    output_data[key] = data_value
                                elif data_type == "NS":
                                    output_data[key] = [int(x) for x in data_value]
                                elif data_type == "SS":
                                    output_data[key] = [x for x in data_value]
                                elif data_type == "BS":
                                    output_data[key] = [x for x in data_value]

                        # Write the output data as a single line to the output file
                        json.dump(output_data, output_file)
        output_file.write("]")

def run():
    """Entry point for the runnable script."""
    sys.exit(main(sys.argv[1:]))


if __name__ == "__main__":
    """main calls run()."""
    run()


