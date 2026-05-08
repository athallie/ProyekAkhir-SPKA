from data_loader import *

db = load_firestore()
Storage = load_appwrite()

product_coll = get_collection(db, "product")

def upload_csv_to_firestore(csv_file_path, collection_name):
    df = pd.read_csv(csv_file_path)
    data = []

    for index, row in df.iterrows():
        data.append({
            "name": row["nama"], 
            "specification":{
                "harga": row["harga"], 
                "nama_prosesor": row["nama_prosesor"], 
                "prosesor": row["skor_prosesor"],
                "ram": row["ram"],
                "ssd": row["ssd"],
                "baterai": row["baterai"],
                "portabilitas": row["portabilitas"],
                "resolusi": row["resolusi"],
                "akurasi_warna": row["akurasi_warna"],
            }
        })

    batch = db.batch()
    count = 0
    
    for record in data:
        doc_ref = db.collection(collection_name).document() 
        batch.set(doc_ref, record)
        count += 1
        
        if count % 500 == 0:
            batch.commit()
            batch = db.batch()
            print(f"Uploaded {count} records...")

    batch.commit()
    print(f"Final total: {count} records uploaded.")

# Usage
upload_csv_to_firestore("data/data_v2.csv", "product")