from elasticsearch import Elasticsearch, helpers
from faker import Faker

# Initialize Faker and Elasticsearch
fake = Faker()
es = Elasticsearch(
  "your_node_link",
  api_key="your_api_key",
  timeout=120, 
)

index_name = "magazine_data"
vector_size = 1536
num_records = 10000  # Change to 1 million records
num_sections_per_magazine = 2  # Number of content sections per magazine

# Create index with nested documents
def create_index():
    mapping = {
        "mappings": {
            "properties": {
                "title": { "type": "text" },
                "author": { "type": "text" },
                "publication_date": { "type": "date" },
                "category": { "type": "keyword" },
                "content": {
                    "type": "nested",  # Define content as nested
                    "properties": {
                        "text": { "type": "text" },
                        "vector_representation": {
                            "type": "dense_vector", "dims": vector_size
                        }
                    }
                }
            }
        }
    }
    es.indices.create(index=index_name, body=mapping, ignore=400)

# Generate fake data
def generate_fake_data(batch_size=1000):
    documents = []
    for i in range(num_records):
        doc_id = str(i)
        title = fake.sentence(nb_words=6)
        author = fake.name()
        publication_date = fake.date()
        category = fake.word()
        
        content = []
        for j in range(num_sections_per_magazine):
            text = fake.text(max_nb_chars=500)
            vector_representation = [fake.random_number(digits=3) / 1000.0 for _ in range(vector_size)] 
            
            content.append({
                "text": text,
                "vector_representation": vector_representation
            })
        
        documents.append({
            "_index": index_name,
            "_id": doc_id,
            "_source": {
                "title": title,
                "author": author,
                "publication_date": publication_date,
                "category": category,
                "content": content
            }
        })

        # Check if we've reached the batch size
        if len(documents) >= batch_size:
            helpers.bulk(es, documents)
            print(f"Pushed {len(documents)} documents to Elasticsearch...")
            documents = []  # Clear the list for the next batch

    # Push any remaining documents after the loop ends
    if documents:
        helpers.bulk(es, documents)
        print(f"Pushed {len(documents)} documents to Elasticsearch...")

# Create the index and generate the fake data
# create_index()
# generate_fake_data()


def rrf_search(keyword_query, vector_query, rank_window_size=50, rank_constant=20):
    search_body = {
        "retriever": {
            "rrf": { 
                "retrievers": [
                    {
                        "standard": { 
                            "query": {
                                "multi_match": {
                                    "query": keyword_query,
                                    "fields": ["title", "author", "content.text"]
                                }
                            }
                        }
                    },
                    {
                        "knn": { 
                            "field": "content.vector_representation",
                            "query_vector": vector_query,
                            "k": rank_window_size,
                            "num_candidates": rank_window_size
                        }
                    }
                ],
                "rank_window_size": rank_window_size,
                "rank_constant": rank_constant
            }
        }
    }
    
    # Execute search
    response = es.search(index=index_name, body=search_body)
    return response['hits']['hits']

# Example RRF search
keyword_query = "Will theory born"
vector_query = [fake.random_number(digits=3) / 1000.0 for _ in range(1536)]

results = rrf_search(keyword_query, vector_query)
for result in results:
    print(result['_source'])