import psycopg2
from common import load_dataset_from_folder

if __name__ == "__main__":
   l, m, h, vh, vvh = load_dataset_from_folder("14-01-2022_14-18-08-215806")
   dataset_meta = []
   dataset_vo = []

   for d in h:
      vo_final = []
      for v in d["customFieldValues"]:
         v["metadata"] = d["uuid"]
         vo_final.append(v)

      dataset_vo.extend(vo_final)
      del d["customFieldValues"]
      dataset_meta.append(d)

   #establishing the connection
   conn = psycopg2.connect(
      database="default_database", user='username', password='password', host='localhost', port=5432
   )
   #Creating a cursor object using the cursor() method
   cursor = conn.cursor()

   cursor.execute(
       """
         CREATE TABLE IF NOT EXISTS Valueoptions(
            id CHAR(36) PRIMARY KEY    NOT NULL,
            metadata    CHAR(36)       NOT NULL,
            text        TEXT           NOT NULL,
            value       TEXT           NOT NULL,
            vo_order    INT            NOT NULL
         )
      """
   )

   print("Creating Index")

   cursor.execute(
      """
         CREATE INDEX metadata_key
            ON Valueoptions (metadata)
      """
   )

   print("Done Creating Index")
   

   #Executing an MYSQL function using the execute() method
   cursor.execute("select version()")

   data = cursor.fetchone()
   print("Connection established to: ", data)

   data_length = len(dataset_vo) 
   step_size = int(data_length/20)
   steps = [i*step_size for i in range(1, 21)]

   print("Inserting data into Valueoptions")

   for i, d in enumerate(dataset_vo):
      cursor.execute(
         """
            INSERT INTO Valueoptions (id, metadata, text, value, vo_order) VALUES ('{}', '{}', '{}', '{}', {});
         """.format(d['id'], d['metadata'], d['text'], d['value'], d['order'])
      )
      if i in steps:
            print("Insertion: " + str((steps.index(i) + 1) * 5) + "% done (" + str(i) + " of " + str(data_length) + ")")
   print("Done inserting data into: Valueoptions")

   cursor.execute(
       """
         SELECT * FROM Valueoptions
      """
   )

   cursor.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
   print(cursor.fetchall())

   conn.commit()

   cursor.close()

   #Closing the connection
   conn.close()