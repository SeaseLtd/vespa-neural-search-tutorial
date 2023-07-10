import random
from ftfy import fix_text

if __name__ == "__main__":
    fields_list = ["id", "text", "color"]
    categorical_list = ["yellow", "red", "blue", "green", "white", "black", "pink", "orange"]

    input_file = open("./msmarco_documents/documents_10k.tsv", "r")
    output_file = open("./vespa_documents/collection_for_feeding.json", "w")
    document = ""
    count = 1
    for line in input_file.readlines():
        text = line.split("\t")[1]
        text_cleaned = fix_text(text.replace("\\d", "d").replace("\\", "")[:-1]).replace('"', '\\"')
        paragraphs = text_cleaned.split(".")
        paragraphs.pop()
        categorical_value = random.randint(0, 7)
        document = document + "{\"put\": \"id:doc:doc::" + str(count) + "\","
        document = document + "\"fields\": {\"text\": \"" + text_cleaned + "\","
        if len(paragraphs) == 0:
            paragraphs.append(text_cleaned)
        document = document + "\"paragraphs\": ["
        for paragraph in paragraphs:
            document = document + "\"" + paragraph + ".\","
        document = document[:-1] + "],"
        document = document + "\"color\": \"" + categorical_list[categorical_value] + "\"}"
        document = document + "}\n"
        count = count + 1
    output_file.write(document)
    output_file.close()
    input_file.close()
