import csv
import json
import sys

def convert_csv_to_json(input_filename: str, output_filename: str):
    vocab = []
    with open(input_filename, mode="r") as input_file:
        reader = csv.reader(input_file)
        next(reader)
        for row in reader:
            vocab.append({
              "protoForm": row[0],
              "evolvedForm": None,
              "modernForm": None,
              "romanisation": None,
              "english": row[1].split("; "),
              "partOfSpeech": row[2],
              "notes": row[3],
              "createdBy": row[4],
            })
        with open(output_filename, mode="w") as output_file:
           output_file.writelines(json.dumps(vocab, indent=4))

def convert_json_to_flat_list(input_filename: str, output_filename: str):
    vocab = []
    with open(input_filename, mode="r") as input_file:
       decoded = json.load(input_file)
       for entry in decoded:
          vocab.append(entry["protoForm"]+"\n")
    with open(output_filename, mode="w") as output_file:
        output_file.writelines(vocab)

if __name__ == "__main__":
  command = str(sys.argv[1]).lower()
  input_filename = str(sys.argv[2])
  output_filename = str(sys.argv[3])
  match command:
    case "convert_csv_to_json":
        convert_csv_to_json(input_filename, output_filename)
    case "convert_json_to_flat_list":
        convert_json_to_flat_list(input_filename, output_filename)
    case _:
      print(f"Command {command} not recognised")