from common import load_dataset_from_folder, create_table_if_not_exists, initialize_dbclient, load_dataset

TABLE_NAME = "Customfields"
KEY_SCHEMA = [
        {
            'AttributeName': 'uuid',
            'KeyType': 'HASH'  # Partition key
        }
    ]

ATTR_DEFS =[
        {
            'AttributeName': 'uuid',
            'AttributeType': 'S'
        }
    ]
        
PROV_TP = {
        'ReadCapacityUnits': 3000,
        'WriteCapacityUnits': 1000
    }

if __name__ == "__main__":
    client = initialize_dbclient()
    create_table_if_not_exists(client, TABLE_NAME, KEY_SCHEMA, ATTR_DEFS, PROV_TP)
    l, m, h, vh, vvh = load_dataset_from_folder("17-01-2022_09-59-33-913650")
    load_dataset(client, TABLE_NAME, vvh)
