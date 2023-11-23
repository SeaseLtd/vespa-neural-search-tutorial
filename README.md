# README #
This is the repository for all the material of the Vespa Neural Search Tutorial.
Here you can find everything you need to deploy a simple Vespa system to do neural queries.

For a step-by-step description read our blog post.

## Requirements ##
To directly use the existing material, without generating documents and models by yourself, you only need:
- vespa-cli 8.263.7

To create documents and models by yourself you also need:
- python 3.11
- torch 2.0.1
- transformers 4.32.0
- onnx 1.14.1

## Repository content ##
- **[documents](documents)**: contains convert_msmarco_data_to_vespa_format.py python script to generate Vespa documents from MS Marco data.
  - **[msmarco_documents](documents/msmarco_documents)**: contains the MS Marco data
  - **[vespa_documents](documents/vespa_documents)**: contains the Vespa documents
- **[model](model)**: contains the export_hf_model_from_hf.py python script to export the all-MiniLM-L6-v2 sentence transformer from HuggingFace in an ONNX format.
  - **[files](model/files)**: contains the all-MiniLM-L6-v2 model (minilm-l6-v2.onnx) and its vocabulary (vocab.txt)
- **[schemas](schemas)**: contains the documents schema
- **[services-xml](services.xml)**: is the Vespa configuration file that defines the services that make up the application
- **[vespa-feed-client-cli](vespa-feed-client-cli)**: is the folder containing the vespa-feed-client library

## Installation ##
To install Vespa:
````
brew install vespa-cli
````
### To generate the documents and models ###
**You can skip this step if you want to use the already provided material.**

To generate documents:
````
python convert_msmarco_data_to_vespa_format.py
````
To export the neural model:
````
python export_hf_model_from_hf.py --hf_model sentence-transformers/all-MiniLM-L6-v2 --output_dir files
````
### To start Vespa ###
To start Vespa:
````
vespa config set target local
docker run --detach --name vespa --hostname vespa-container --publish 8080:8080 --publish 19071:19071 vespaengine/vespa
vespa deploy --wait 300
````
To index documents:
````
./vespa-feed-client-cli/vespa-feed-client --file ./documents/vespa_documents/collection_for_feeding.json --endpoint http://localhost:8080
````
To remove Vespa container:
````
docker rm -f vespa
````

## Usage ##
### Exact Nearest Neighbor Search ###
````
vespa query "yql=select * from doc where {approximate:false,targetHits: 100}nearestNeighbor(embedding, first_query)" "input.query(first_query)=embed(#of calories to eat to lose weight)" "ranking=pure_neural_rank"
````
### Approximate Nearest Neighbor Search ###
````
vespa query "yql=select * from doc where {targetHits: 100}nearestNeighbor(embedding, first_query)" "input.query(first_query)=embed(#of calories to eat to lose weight)" "ranking=pure_neural_rank"
````
### Approximate Nearest Neighbor with Filters ###
````
vespa query "yql=select * from doc where {targetHits: 100}nearestNeighbor(embedding, first_query) AND color contains 'yellow'" "input.query(first_query)=embed(#of calories to eat to lose weight)" "ranking=pure_neural_rank"
````
Adding a distanceThreshold:
````
vespa query "yql=select * from doc where {distanceThreshold: 5.2, targetHits: 100}nearestNeighbor(embedding, first_query) AND color contains 'yellow'" "input.query(first_query)=embed(#of calories to eat to lose weight)" "ranking=pure_neural_rank"
````
### Approximate Nearest Neighbor with Multiple Vectors ###
````
vespa query "yql=select * from doc where {targetHits: 100}nearestNeighbor(multiple_embeddings, first_query)" "input.query(first_query)=embed(#of calories to eat to lose weight)" "ranking=multiple_pure_neural_rank"
````
### Multiple Nearest Neighbor Search Operators in the Same Query ###
````
vespa query "yql=select * from doc where ({label:'first_query', targetHits:100}nearestNeighbor(embedding, first_query)) OR ({label:'second_query', targetHits:100}nearestNeighbor(embedding, second_query))" "ranking=pure_neural_rank" "input.query(first_query)=embed(#of calories to eat to lose weight)" "input.query(second_query)=embed(diet zone strategy)"
````
With the sum of closenesses as relevance:
````
vespa query "yql=select * from doc where ({label:'first_query', targetHits:100}nearestNeighbor(embedding, first_query)) OR ({label:'second_query', targetHits:100}nearestNeighbor(embedding, second_query))" "ranking=neural_rank_sum_closeness" "input.query(first_query)=embed(#of calories to eat to lose weight)" "input.query(second_query)=embed(diet zone strategy)"
````
### Hybrid Sparse and Dense Retrieval ###
````
vespa query "yql=select * from doc where {targetHits: 100}nearestNeighbor(embedding, first_query) OR text contains 'exercise'" "type=weakAnd" "ranking=hybrid_rank" "input.query(first_query)=embed(#of calories to eat to lose weight)"
````
Passing weights:
````
vespa query "yql=select * from doc where {targetHits: 100}nearestNeighbor(embedding, first_query) OR text contains 'exercise'" "type=weakAnd" "ranking=hybrid_rank" "input.query(first_query)=embed(#of calories to eat to lose weight)" "ranking.features.query(textWeight)=0.5" "ranking.features.query(vectorWeight)=30"
````
### Normalized hybrid Sparse and Dense Retrieval ###
````
vespa query "yql=select * from doc where {targetHits: 100}nearestNeighbor(embedding, first_query) OR text contains 'exercise'" "type=weakAnd" "ranking=normalized_hybrid_rank" "input.query(first_query)=embed(#of calories to eat to lose weight)"
````
### Re-ranking with neural search ###
````
vespa query "yql=select * from doc where {targetHits: 100}nearestNeighbor(embedding, first_query) OR text contains 'exercise'" "type=weakAnd" "ranking=neural_rerank_profile" "input.query(first_query)=embed(#of calories to eat to lose weight)"
````