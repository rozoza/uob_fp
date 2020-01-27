import csv

with open("./uob_fp/complete_sum.csv", "r") as infile:
    reader = csv.DictReader(infile)

    fact = 0
    proceedings = 0
    background = 0
    framing = 0
    disposal = 0
    textual = 0
    other = 0
    for row in reader:
        if row['role'] == 'FACT':
            if row['align'] != "NONE":
                fact += 1     
        if row['role'] == 'PROCEEDINGS':
            if row['align'] != "NONE":
                proceedings += 1       
        if row['role'] == 'BACKGROUND':
            if row['align'] != "NONE":
                background += 1         
        if row['role'] == 'FRAMING':
            if row['align'] != "NONE":
                framing += 1          
        if row['role'] == 'DISPOSAL':
            if row['align'] != "NONE":
                disposal += 1           
        if row['role'] == 'TEXTUAL':
            if row['align'] != "NONE":
                textual += 1          
        if row['role'] == 'NONE':
            if row['align'] != "NONE":
                other += 1    
    print("fact", fact)
    print("proceedings", proceedings)
    print("background", background)
    print("framing", framing)
    print("disposal", disposal)
    print("textual", textual)
    print("other", other)