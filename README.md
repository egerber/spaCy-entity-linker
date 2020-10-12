# Spacy Entity Linker

## Introduction
Spacy Entity Linker is a pipeline for spaCy that performs Linked Entity Extraction with Wikidata on 
a given Document.
The Entity Linking System operates by matching potential candidates from each sentence
 (subject, object, prepositional phrase, compounds, etc.) to aliases 
from Wikidata. The package allows to easily find the category behind each entity (e.g. "banana" is type "food" OR "Microsoft" is type "company"). It can 
is therefore useful for information extraction tasks and labeling tasks.

The package was written before a working Linked Entity Solution existed inside spaCy. In comparison to spaCy's linked entity system, it has the following examples
- no extensive training required (string-matching is done on a database)
- knowledge base can be dynamically updated without retraining
- entity categories can be easily resolved
- grouping entities by category

It also comes along with a number of disadvantages:
- it is slower than the spaCy implementation due to the use of a database for finding entities
- no context sensitivity due to the implementation of the "max-prior method" for entitiy disambiguation


## Use
```python
import spacy
from SpacyEntityLinker import EntityLinker

#Initialize Entity Linker
entityLinker = EntityLinker()

#initialize language model
nlp = spacy.load("en_core_web_sm")

#add pipeline
nlp.add_pipe(entityLinker, last=True, name="entityLinker")

doc = nlp("I watched the Pirates of the Carribean last silvester")


#returns all entities in the whole document
all_linked_entities=doc._.linkedEntities
#iterates over sentences and prints linked entities
for sent in doc.sents:
    sent._.linkedEntities.pretty_print()

'''
https://www.wikidata.org/wiki/Q194318     194318     Pirates of the Caribbean        Series of fantasy adventure films                                                                   
https://www.wikidata.org/wiki/Q12525597   12525597   Silvester                       the day celebrated on 31 December (Roman Catholic Church) or 2 January (Eastern Orthodox Churches)  

'''
```

## Example
In the following example we will use SpacyEntityLinker to extract all 


### Entity Linking Policy
Currently the only method for choosing an entity given different possible matches (e.g. Paris - city vs Paris - firstname) is max-prior. This method achieves around 70% accuracy on predicting
the correct entities behind link descriptions on wikipedia.

## Note
The Entity Linker at the current state is still experimental and should not be used in production mode.

## Performance
The current implementation supports only Sqlite. This is advantageous for development because 
it does not requirement any special setup and configuration. However, for more performance critical usecases, a different
database with in-memory access (e.g. Redis) should be used. This may be implemented in the future.

## Installation

To install the package run: <code>pip install spacy-entity-linker</code>

Afterwards, the knowledge base (Wikidata) must be downloaded. This can be done by calling 

<code>python -m spacyEntityLinker download_knowledge_base</code>

This will download and extract a ~500mb file that contains a preprocessed version of Wikidata

## TODO
- [ ] implement Entity Classifier based on sentence embeddings for improved accuracy 
- [ ] implement get_picture_urls() on EntityElement
- [ ] retrieve statements for each EntityElement (inlinks + outlinks)