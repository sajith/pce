import json

with open('/Users/yifeiwang/Desktop/5.3code/pce/test/data/connection.json') as f:
    connection = json.load(f)

if len(connection) > 20:
    connection.sort(key=lambda x: x[2])

splitted_list = [connection[x:x+5] for x in range(0, len(connection),5)]

with open('/Users/yifeiwang/Desktop/5.3code/pce/test/data/splittedconnection.json', 'w') as json_file:
    data = splitted_list
    json.dump(data, json_file, indent=4)

print(splitted_list)