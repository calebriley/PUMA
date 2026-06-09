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

def apply_evolved_forms(input_filename: str, output_filename: str):
    vocab = {}
    with open(input_filename, mode="r") as input_file:
        for line in input_file:
            if not line or line.strip() == "":
                continue
            proto, evolved = line.split("=>")
            proto = proto.strip()
            evolved = evolved.strip()
            vocab[proto] = evolved
    decoded = None
    with open(output_filename, mode="r") as output_file:
        decoded = json.load(output_file)

    for entry in decoded:
        if entry["protoForm"] in vocab:
            entry["evolvedForm"] = vocab[entry["protoForm"]]
            if entry["modernForm"] is None:
                entry["modernForm"] = vocab[entry["protoForm"]]
    
    with open(output_filename, mode="w") as output_file:
        output_file.writelines(json.dumps(decoded, indent=4))

def romanise_form(form: str) -> str:
    form = form.replace("ʷa", "ä")
    form = form.replace("ʲa", "á")
    form = form.replace("ʷi", "ï")
    form = form.replace("ʲu", "ú")
    form = form.replace("ʃ", "sh")
    return form

def romanise_json(filename: str):
    decoded = None
    with open(filename, mode="r") as file:
        decoded = json.load(file)

    for entry in decoded:
        if entry["modernForm"]:
            entry["romanisation"] = romanise_form(entry["modernForm"])
    
    with open(filename, mode="w") as file:
        file.writelines(json.dumps(decoded, indent=4))


def help(command: str):
    COMMANDS = [
       "convert_csv_to_json", 
       "convert_json_to_flat_list",
       "apply_evolved_forms",
       "romanise_json",
    ]
    print(f"Command '{command}' not recognised")
    print("The following commands are available:")
    for available_command in COMMANDS:
        print("\t" + available_command)


if __name__ == "__main__":
  command = str(sys.argv[1]).lower()
  match command:
    case "convert_csv_to_json":
        input_filename = str(sys.argv[2])
        output_filename = str(sys.argv[3])
        convert_csv_to_json(input_filename, output_filename)
    case "convert_json_to_flat_list":
        input_filename = str(sys.argv[2])
        output_filename = str(sys.argv[3])
        convert_json_to_flat_list(input_filename, output_filename)
    case "apply_evolved_forms":
        input_filename = str(sys.argv[2])
        output_filename = str(sys.argv[3])
        apply_evolved_forms(input_filename, output_filename)
    case "romanise_json":
        filename = str(sys.argv[2])
        romanise_json(filename)
    case _:
        help(command)