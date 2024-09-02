# **Magazine Data Elasticsearch Project**

## **Overview**

This project demonstrates how to create and populate an Elasticsearch index with magazine data, including titles, authors, publication dates, categories, and content sections with vector representations. The project also includes a custom search function using Reciprocal Rank Fusion (RRF) to combine keyword and vector-based search results.

## **Features**

- **Elasticsearch Indexing**: Creates an Elasticsearch index with nested documents, including dense vectors for content sections.
- **Data Generation**: Uses `Faker` to generate synthetic data, including 1 million records with vector representations.
- **RRF Search**: Implements a custom search function using the RRF technique to combine standard keyword search with k-Nearest Neighbors (kNN) vector search.

## **Prerequisites**

Before you begin, ensure you have the following installed on your system:

- Python 3.7+
- Elasticsearch instance (local or cloud-based)
- Required Python packages:
  - `elasticsearch`
  - `faker`

## **Installation**

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/magazine-data-elasticsearch.git
   cd magazine-data-elasticsearch
   ```
2. **Install the Required Packages**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Elasticsearchs**
   ```bash
   es = Elasticsearch(
    "your_elasticsearch_node_url",
    api_key="your_api_key",
    timeout=120,
   )   ```
Replace "your_elasticsearch_node_url" and "your_api_key" with your actual Elasticsearch instance details.

3. **Install the Required Packages**
   ```bash
   pip install -r requirements.txt
   ```

## **Usage**

   1. **Create mappings and fake data**
      Run the functions create_index() and generate_fake_data()
      ```
      create_index()
      generate_fake_data()
      ```
   
   2. **Run a Sample Search**
      ```
      keyword_query = "Example search keyword"
      vector_query = [fake.random_number(digits=3) / 1000.0 for _ in range(1536)]
      results = rrf_search(keyword_query, vector_query)
      for result in results:
        print(result['_source'])
      ```


