import boto3, json, uuid, random, os
from decimal import Decimal
from datetime import datetime

TABLE_NAME = "Movies" #"Customfields"
KEY_SCHEMA = [
        {
            'AttributeName': 'year',
            'KeyType': 'HASH'  # Partition key
        },
        {
            'AttributeName': 'title',
            'KeyType': 'RANGE'  # Sort key
        }
    ]

ATTR_DEFS =[
        {
            'AttributeName': 'year',
            'AttributeType': 'N'
        },
        {
            'AttributeName': 'title',
            'AttributeType': 'S'
        },
    ]
        
PROV_TP = {
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }

#initialize db client
def initialize_dbclient():
    ddb = boto3.resource('dynamodb',
                            aws_access_key_id="anything",
                            aws_secret_access_key="anything",
                            region_name="us-west-2",
                            endpoint_url="http://localhost:8000")
    return ddb

#create a table if it does not exist
def create_table_if_not_exists(db, tablename, keys, attributes, provision_info):
    print("Creating Table: " + tablename)
    try:
        table = db.create_table(
            TableName=tablename,
            KeySchema=keys,
            AttributeDefinitions=attributes,
            ProvisionedThroughput=provision_info
        )

        print("Table: " + tablename + " created successfully!")

        return table 
    except Exception as e:
        print("Table: " + tablename + " already exists!")
    finally:
        print("Done creating Table: " + tablename + "!")

def delete_table(db, tablename):
    print("Deleting Table: " + tablename)
    try:
        table = db.Table(tablename)
        table.delete()
    except Exception as e:
        print("Error: " + e)
    finally:
        print("Done deleting Table: " + tablename)

#load dataset to db
def load_dataset(db, tablename, data, transformation=None):
    
    if transformation != None:
        print("Transforming data...")
        data = map(data, transformation)
        print("Data transformation done!")
    
    table = db.Table(tablename)

    data_length = len(data)
    step_size = int(data_length/20)
    steps = [i*step_size for i in range(1, 21)]

    print("Inserting data into: " + tablename)
    for i, d in enumerate(data):
        table.put_item(Item=d)
        if i in steps:
            print("Insertion: " + str((steps.index(i) + 1) * 5) + "% done (" + str(i) + " of " + str(data_length) + ")")
    print("Done inserting data into: " + tablename)

def generate_value_options(length):
    def gvo(i):
        return {
          "id": str(uuid.uuid4()),
          "order": i + 1,
          "text": "Option" + str(i + 1),
          "value": "Value" + str(i + 1)
        }
    return [ gvo(i) for i in range(length)]

def generate_customfield_metadata():
    return {
      "dataType": "list",
      "dependencyFieldId": str(uuid.uuid5(uuid.uuid4(), "concur")),
      "dependencyType": "is",
      "dependencyValues": [
        "2"
      ],
      "displayAtEnd": random.choice([True, False]),
      "displayAtStart": random.choice([True, False]),
      "displayTitle": "Reason",
      "uuid": str(uuid.uuid5(uuid.uuid4(), "concur")),
      "maxLength": 1,
      "minLength": 100,
      "name": "TestTrip2",
      "required": random.choice([True, False]),
      "totalValues": 4,
      "attributeType": "trip",
      "displayForRegularTrips": random.choice([True, False])
    }

def generate_customfield_dataset(number_of_entries, vo_lower_bound, vo_upper_bound):
    dataset = []

    for i in range(number_of_entries):
        d = generate_customfield_metadata()
        d["customFieldValues"] = generate_value_options(random.randint(vo_lower_bound, vo_upper_bound))
        dataset.append(d)

    return dataset

def create_customfield_dataset(filename, number_of_entries, vo_lower_bound, vo_upper_bound):
    dataset = generate_customfield_dataset(number_of_entries, vo_lower_bound, vo_upper_bound)
    dir = os.path.dirname(filename)
    if not os.path.exists(dir):
        os.mkdir(dir)
    f = filename.split("\\")[-1]
    with open(filename, "w") as fobj:
        fobj.write(json.dumps(dataset, indent=4))

def get_prefix():
    return "./" + datetime.now().strftime("%d-%m-%Y_%H-%M-%S-%f")

def create_dataset(numberOfEntries):
    prefix = get_prefix()
    create_customfield_dataset(prefix + "/dataset_low.json", numberOfEntries, 1, 10)
    create_customfield_dataset(prefix + "/dataset_mid.json", numberOfEntries, 10, 100)
    create_customfield_dataset(prefix + "/dataset_high.json", numberOfEntries, 100, 1000)
    create_customfield_dataset(prefix + "/dataset_veryhigh.json", numberOfEntries, 1000, 5000)
    create_customfield_dataset(prefix + "/dataset_veryveryhigh.json", numberOfEntries, 5000, 10000)
    return prefix

def load_dataset_from_folder(folder):
    files = [ folder + "\\dataset_low.json", folder + "\\dataset_mid.json", folder + "\\dataset_high.json", folder + "\\dataset_veryhigh.json", folder + "\\dataset_veryveryhigh.json" ]
    data = []
    for f in files:
        with open(f) as fobj:
            data.append(json.load(fobj))
    return data

def _main():
    client = initialize_dbclient()
    create_table_if_not_exists(client, TABLE_NAME, KEY_SCHEMA, ATTR_DEFS, PROV_TP)
    with open("moviedata.json") as json_file:
        movie_list = json.load(json_file, parse_float=Decimal)

    load_dataset(client, TABLE_NAME, movie_list)
    #delete_table(client, TABLE_NAME)

if __name__ == "__main__":
    #_main()
    create_dataset(3000)
