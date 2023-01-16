import random

if __name__ == "__main__":
    fields_list = ["id", "text", "color"]
    categorical_list = ["yellow", "red", "blue", "green", "white", "black", "pink", "orange"]

    input_file = open("./msmarco_documents/documents_10k.tsv", "r")
    output_file = open("./vespa_documents/collection_for_feeding.json", "w")
    document = ""
    count = 1
    for line in input_file.readlines():
        text = line.split("\t")[1]
        categorical_value = random.randint(0, 7)
        document = document + "{\"put\": \"id:doc:doc::" + str(count) + "\","
        document = document + "\"fields\": {\"text\": \"" + text.replace("\\d", "d").replace("\\", "")[:-1] + "\","
        document = document + "\"color\": \"" + categorical_list[categorical_value] + "\"}"
        document = document + "}\n"
        count = count + 1
    output_file.write(document)
    output_file.close()
    input_file.close()
