from common import load_dataset_from_folder, create_table_if_not_exists, initialize_dbclient, load_dataset

#metadata
TABLE_NAME_META = "CustomfieldMetadata"
KEY_SCHEMA_META = [
        {
            'AttributeName': 'uuid',
            'KeyType': 'HASH'  # Partition key
        }
    ]

ATTR_DEFS_META =[
        {
            'AttributeName': 'uuid',
            'AttributeType': 'S'
        }
    ]

#valueoptions
TABLE_NAME_VO = "CustomfieldValueoptions"
KEY_SCHEMA_VO = [,
        {
            'AttributeName': 'metadata',
            'KeyType': 'HASH' # Parition key
        },
        {
            'AttributeName': 'id',
            'KeyType': 'RANGE' #Sort key
        }
    ]

ATTR_DEFS_VO =[
        {
            'AttributeName': 'id',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'metadata',
            'AttributeType': 'S'
        }
    ]
        
PROV_TP = {
        'ReadCapacityUnits': 3000,
        'WriteCapacityUnits': 1000
    }

if __name__ == "__main__":
    client = initialize_dbclient()
    create_table_if_not_exists(client, TABLE_NAME_META, KEY_SCHEMA_META, ATTR_DEFS_META, PROV_TP)
    create_table_if_not_exists(client, TABLE_NAME_VO, KEY_SCHEMA_VO, ATTR_DEFS_VO, PROV_TP)
    l, m, h, vh, vvh = load_dataset_from_folder("17-01-2022_09-59-33-913650")
    dataset_meta = []
    dataset_vo = []

    for d in l:
        vo_final = []
        for v in d["customFieldValues"]:
            v["metadata"] = d["uuid"]
            vo_final.append(v)

        dataset_vo.extend(vo_final)
        del d["customFieldValues"]
        dataset_meta.append(d)
    
    load_dataset(client, TABLE_NAME_META, dataset_meta)
    load_dataset(client, TABLE_NAME_VO, dataset_vo)
