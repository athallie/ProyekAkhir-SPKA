from data_loader import load_firestore
import json


db = load_firestore()

def export_collection_to_json(collection_name, output_file):
    print(f"Fetching data from collection: {collection_name}...")
    
    # 2. Get all documents from the collection
    docs = db.collection(collection_name).stream()
    
    # 3. Store data in a dictionary
    data = {}
    for doc in docs:
        data[doc.id] = doc.to_dict()
    
    # 4. Save to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, default=str) # default=str handles dates/timestamps
    
    print(f"Successfully exported {len(data)} documents to {output_file}")

# Usage
export_collection_to_json("product", "product.json")