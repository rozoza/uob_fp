import csv
import xml.etree.ElementTree as ET
import random

def countlines(case, parreader):
    count = 1
    for lines in parreader:
        if int(lines["case"]) == case:
            count += 1
        if int(lines["case"]) > case:
            break
    return count

def simple_summary():
    with open("./uob_fp/Complete_Corpus.csv") as file:
        reader = csv.DictReader(file)
        current_lord = ""
        name = ""
        filename = ""
        lines = 0
        fullagr = True
        
        try:
            for row in reader:
                if int(row["case"]) == 40:
                    if int(row["line"]) == 0:
                        '''Need to know how to open different reader 
                        and countlines so we know the begining and ending of each case and lord
                        case using row[("case")]
                        maybe use new judge for the lord'''
                        #lines = countlines(int(row["case"]), reader)
                        #print(lines)
                        name = "summary_" + "case_" + row["case"] + "_ASMO"
                        filename = "./uob_fp/Summary/" + name + ".txt"
                        f = open(filename, "w+")
                        f.write(name + "\n")
                        f.write("from " + row["body"] + "\n")
                        f.write("majority opinion: " + row["mj"] + "\n")

                    if "LORD" in row["body"] or "BARONESS" in row["body"]:
                        if fullagr == False:
                            f.write(current_lord + "is assumed to fully agree only with his/her own reasonings " + "\n")                        
                        current_lord = row["body"]
                        fullagr = False
                        f.write("\n" + "--" + current_lord + "--" + "\n")

                    if row["relation"] == "fullagr":
                        fullagr = True
                        if row["to"] == "all":
                            f.write(row["from"] + " agrees with all judges" + "\n")
                        elif row["to"] == "self":  
                            f.write(row["from"] + " states the importance of his/her own reasonings" + "\n")
                        else:                  
                            f.write(row["from"] + " has a full agreement with " + row["to"] + "\n")
                    
                    if row["relation"] == "outcome" and row["to"] == "self":
                        f.write("outcome: " + "\n")
                        f.write(row["body"] + "\n")

                # if int(row["case"]) == 100:
                #     print("hello")
                #     break

        except Exception as e:
            print(e)
        finally:
            f.close()

def write_summary(respondents, appellants, majority, ukhl, lords, disposal, agree, outcome, proceedings, framing):
    print(*ukhl)
    print(" ".join(respondents))
    print(" ".join(appellants))
 
    for array in agree:
        multiple_agree = False
        for lord in lords:
            if array[0] in lord:
                print(lord, "delivered an opinion agreeing with ", end="")
                if len(array[1]) > 1:
                    for v in range(len(array[1])):
                        if multiple_agree == True:
                            print(" and ", end="")
                        if array[1][v] == "SELF":
                            print("his reasonings", end="")
                        else:
                            for ld in lords:
                                if array[1][v] in ld:
                                    print(ld, end="")
                        multiple_agree = True
                else:
                    print(array[1][0])
                print()
                
                pro_list = []
                for pro_array in proceedings:
                    index = lord.split(" ").index("LORD")+1
                    short_lord = lord.split(" ")[index]
                    if short_lord in majority:
                        if pro_array[0] in lord:
                            pro_list.append(pro_array[1])
                if len(pro_list) != 0:
                    fr = random.sample(pro_list, 2)
                    print("He said ", end="")
                    print("\"", *fr, end=" ")

                fr_list = []
                for fr_array in framing:
                    index = lord.split(" ").index("LORD")+1
                    short_lord = lord.split(" ")[index]
                    if short_lord in majority:
                        if fr_array[0] in lord:
                            fr_list.append(fr_array[1])
                if len(fr_list) != 0:
                    fr = random.sample(fr_list, 2)
                    # print("He said ", end="")
                    print(*fr, end=" ")

                dis_list = []
                for dis_array in disposal:
                    index = lord.split(" ").index("LORD")+1
                    short_lord = lord.split(" ")[index]
                    if short_lord in majority:
                        if dis_array[0] in lord:
                            dis_list.append(dis_array[1])
                if len(dis_list) != 0:
                    dis = random.sample(dis_list, 2)
                    # print("He said ", end="")
                    print(*dis, "\"")

    multiple_majority = False
    print("The majority voice has agreed to the reasonings given by ", end="")
    for lord in lords:
        for judge in majority:
            if judge in lord:
                if multiple_majority == True:
                    print(" and ", end="")
                print(lord, end="",)
                multiple_majority = True
    if multiple_majority == True:
        print(". Hence the court binding precedent is held by them.")

    # print(outcome)


def summary():
    with open("./uob_fp/comsum_corpus/comsum_2.23.csv", "r") as infile:
        reader = csv.DictReader(infile)

        respondents = []
        appellants = []
        majority = []
        ukhl = []
        lords = []
        disposal = []
        agree = []
        outcome = []
        proceedings = []
        framing = []

        sum_params = respondents, appellants, majority, ukhl, lords, disposal, agree, outcome, proceedings, framing
        tree =  ET.parse("./uob_fp/SUM_2005_corpus/2002May23burket-1.ling.xml")
        root = tree.getroot()
        for elem in root.iter("case"):
            if len(elem):
                for subelem in elem:
                    if subelem.attrib.get("subtype") == "respondent":
                        respondents.append(subelem.text.replace("\n", " "))
                    if subelem.attrib.get("subtype") == "appellant":
                        appellants.append(subelem.text.replace("\n", " "))

        for elem in root.iter("lordname"):
            lords.append(elem.text.replace("\n", " ").upper())

        for row in reader:
            if row["role"] == "<new-case>":
                mj = row["agree"].split("+")
                for v in range(len(mj)):
                    majority.append(mj[v].upper())
                ukhl.append(row["text"])

            if row["role"] != "<new-case>":
                if row["agree"] != "NONE" and row["agree"] != "no match":
                    agree.append([row["judge"].upper(), row["agree"].upper().split("+")])

            if row["judge"].upper() in majority and row["role"] == "DISPOSAL" and row["align"] != "NONE":
                disposal.append([row["judge"].upper(), row["text"]])
            if row["judge"].upper() in majority and row["role"] == "PROCEEDINGS" and row["align"] != "NONE":
                proceedings.append([row["judge"].upper(), row["text"]])
            if row["judge"].upper() in majority and row["role"] == "FRAMING" and row["align"] != "NONE":
                framing.append([row["judge"].upper(), row["text"]])
            if row["judge"].upper() in majority and row["outcome"] != "NONE" and row["outcome"] != "no match":
                outcome.append([row["judge"].upper(), row["text"]])

        for lord in majority:
            for array in disposal:
                if array[0] == lord:
                    pass
                    # print(array[1])

        write_summary(*sum_params)
        
        # infile.seek(0)
        # for row in reader:
        #     if row["case_id"] == "2.23":
        #         print(row["text"])

summary()
