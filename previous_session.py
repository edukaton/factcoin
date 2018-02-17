# coding: utf-8
from pyelasticsearch import ElasticSearch
es = ElasticSearch('elasticsearch:9200')
es = ElasticSearch('http://elasticsearch:9200')
es
es.index('contacts',
          'person',
          {'name': 'Joe Tester', 'age': 25, 'title': 'QA Master'},
           id=1)
docs = [{'id': 2, 'name': 'Jessica Coder', 'age': 32, 'title': 'Programmer'},
        {'id': 3, 'name': 'Freddy Tester', 'age': 29, 'title': 'Office Assistant'}]
es.bulk((es.index_op(doc, id=doc.pop('id')) for doc in docs),
        index='contacts',
        doc_type='person')	
es.refresh('contacts')
es.search('name:joe OR name:freddy', index='contacts')
es.detele()
es.delete()
es.delete('contacts')
es.indices.delete(index='test-index', ignore=[400, 404])
es.delete(index='contacts', ignore=[400, 404])
es.delete(index='contacts')
es.delete_all()
es.delete_all("contacts")
es.delete_all("contacts", doc_type="*")
es.delete_all_indexes()
es.search('name:joe OR name:freddy', index='contacts')
es.index('documents', 'document',ds
         {'name': 'Joe Tester', 'age': 25, 'title': 'QA Master'},
          id=1)
import json
open("./shared/results.jsonl").read().split('\n')
raw = open("./shared/results.jsonl").read().split('\n')
data = [json.loads(row) for row in raw]
data = [json.loads(row) for row in raw[:-1]]
data
for doc in data:
    es.index('documents', 'doc', doc)
    
data[0]
data[0]['text']
text = data[0]['text']
es.search(text, index='documents')
es.search(text, index='documents', hits=3)
es.search(text, index='documents')
es.search(text, index='documents')[0]
results = es.search(text, index='documents')
for r in results:
    print (r)
    break
results = es.search(text, index='documents')
results
results.keys()
results['hits']
results['hits'][0]
results['hits'].keys()
results['hits']['hits']
results['hits']['hits'][0]
results['hits']['hits'][1]
text
results['hits']['hits'][4]
results['hits']['hits'][6]
results['hits']['hits'][6]
es.search(text, index='haystack')
es.indices.get_alias("*")
es.indices.get_alias("*")
es.aliases
es.aliases.all()
es.aliases()
