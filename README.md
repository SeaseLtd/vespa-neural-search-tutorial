# README #
This is the repository for all the material of the Vespa Neural Search Tutorial.
Here you can find everything you need to deploy a simple Vespa system to do neural queries.

For a step-by-step description read our blog post.

## Requirements ##
To directly use the existing material, without generating documents and models by yourself, you only need:
- vespa-cli 8.109.47

To create documents and models by yourself you also need:
- python 3.10
- transformers 4.25.1

## Repository content ##
- **[documents](documents)**: contains convert_msmarco_data_to_vespa_format.py python script to generate Vespa documents from MS Marco data.
  - **[msmarco_documents](documents/msmarco_documents)**: contains the MS Marco data
  - **[vespa_documents](documents/vespa_documents)**: contains the Vespa documents
- **[model](model)**: contains the export_model.py python script to export the all-MiniLM-L6-v2 sentence transformer from HuggingFace in an ONNX format.
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
python export_model.py
````
### To start Vespa ###
To start Vespa:
````
vespa config set target local
docker run --detach --name vespa --hostname vespa-container --publish 8080:8080 --publish 19071:19071 vespaengine/vespa
vespa status deploy --wait 300
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
### Approximate Nearest Neighbor with Query Filter ###
````
vespa query "yql=select * from doc where {targetHits: 100}nearestNeighbor(embedding, first_query) AND color contains 'yellow'" "input.query(first_query)=embed(#of calories to eat to lose weight)" "ranking=pure_neural_rank"
````
Adding a distanceThreshold:
````
vespa query "yql=select * from doc where {distanceThreshold: 5.0, targetHits: 100}nearestNeighbor(embedding, first_query) AND color contains 'yellow'" "input.query(first_query)=embed(#of calories to eat to lose weight)" "ranking=pure_neural_rank"
````
### Hybrid Sparse and Dense Retrieval Methods ###
````
vespa query "yql=select * from doc where {targetHits: 100}nearestNeighbor(embedding, first_query) OR text contains 'exercise'" "type=weakAnd" "ranking=hybrid_rank" "input.query(first_query)=embed(#of calories to eat to lose weight)"
````
Passing weights:
````
vespa query "yql=select * from doc where {targetHits: 100}nearestNeighbor(embedding, first_query) OR text contains 'exercise'" "type=weakAnd" "ranking=hybrid_rank" "input.query(first_query)=embed(#of calories to eat to lose weight)" "ranking.features.query(textWeight)=0.5" "ranking.features.query(vectorWeight)=30"
````
### Multiple Nearest Neighbor Search Operators in the Same Query ###
````
vespa query "yql=select * from doc where ({label:'first_query', targetHits:100}nearestNeighbor(embedding, first_query)) OR ({label:'second_query', targetHits:100}nearestNeighbor(embedding, second_query))" "ranking=pure_neural_rank" "input.query(first_query)=embed(#of calories to eat to lose weight)" "input.query(second_query)=embed(diet zone strategy)"
````
With the sum of closenesses as relevance:
````
vespa query "yql=select * from doc where ({label:'first_query', targetHits:100}nearestNeighbor(embedding, first_query)) OR ({label:'second_query', targetHits:100}nearestNeighbor(embedding, second_query))" "ranking=neural_rank_sum_closeness" "input.query(first_query)=embed(#of calories to eat to lose weight)" "input.query(second_query)=embed(diet zone strategy)"
````
