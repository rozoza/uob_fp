import csv

case_ids = []
with open("./uob_fp/complete_sum.csv", "r") as infile:
    reader = csv.DictReader(infile)

    for row in reader:
        if row["case_id"] not in case_ids:
            if row["case_id"] == "N/A":
                case_ids.append("NA")
            else:
                case_ids.append(row["case_id"])

for v in range(len(case_ids)):
    filename = case_ids[v]
    with open("./uob_fp/comsum_corpus/comsum_" + filename + ".csv", "r") as infile:
        reader = csv.DictReader(infile)

        f = open("./uob_fp/68txt_corpus/" + filename + ".txt", "w", encoding="utf-8")
        for row in reader:
            f.writelines(row["text"] +"\n")
        f.close()