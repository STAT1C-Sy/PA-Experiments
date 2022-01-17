import matplotlib.pyplot as plt

DATASET = "performance_data_legit_low.txt"
POSTGRES_ID = "POSTGRES"
DDBTWOTABLES_ID = "DDB_TWO"
DDBONETABLE_ID = "DDB_SINGLE"

postgres_data = []
ddb_two_data = []
ddb_one_data = []

with open("performance_data\\" + DATASET, "r") as fobj:
    for line in fobj.readlines():
        splt_line = line.split(";")
        
        start = int(splt_line[0].replace("start:", ""))
        end = int(splt_line[1].replace("end:", ""))
        diff = (end - start)/1000000

        if diff < 20:
            method = splt_line[2].replace("method:", "").strip()

            if method == POSTGRES_ID:
                postgres_data.append(diff)
            elif method == DDBTWOTABLES_ID:
                ddb_two_data.append(diff)
            elif method == DDBONETABLE_ID:
                ddb_one_data.append(diff)

print(sum(postgres_data)/len(postgres_data))
print(sum(ddb_two_data)/len(ddb_two_data))
print(sum(ddb_one_data)/len(ddb_one_data))

columns = [postgres_data, ddb_one_data, ddb_two_data]
fig, ax = plt.subplots()
ax.boxplot(columns, showmeans=True, meanline=True)
ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
               alpha=0.5)
plt.xticks([1, 2, 3] , ["PostgresSQL", "DynamoDB one Table", "DynamoDB two Tables"])
plt.show()
