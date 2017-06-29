步骤：

- 新建index
- 创建mapping
- 新增字段

```bash
# 以 POST 创建index 失败...
$ curl -XPOST "http://127.0.0.1:9200/productindex"
No handler found for uri [/productindex] and method [POST]%                                                        

# 改成PUT
$ curl -XPUT "http://127.0.0.1:9200/productindex"
{"acknowledged":true,"shards_acknowledged":true}%                                                                  

# 新index 空mapping
$ curl -XGET "http://127.0.0.1:9200/productindex/_mapping?pretty"
{
  "productindex" : {
    "mappings" : { }
  }
}

# 创建一个type并设置mapping
$ curl -XPOST "http://127.0.0.1:9200/productindex/product/_mapping" -d '
quote> {
quote>   "product": {
quote>     "properties": {
quote>       "title": {"type":"string", "store": "yes"},
quote>       "desc": {"type":"string", "index": "not_analyzed"},
quote>       "price": {"type": "double"},
quote>       "onSale": {"type": "boolean"},
quote>       "type": {"type": "integer"},
quote>       "createDate": {"type": "date"}
quote>     }
quote>   }
quote> }'
{"acknowledged":true}%                                                                                             
# 查看mapping
$ curl -XGET "http://127.0.0.1:9200/productindex/_mapping?pretty"
{
  "productindex" : {
    "mappings" : {
      "product" : {
        "properties" : {
          "createDate" : {
            "type" : "date"
          },
          "desc" : {
            "type" : "keyword"
          },
          "onSale" : {
            "type" : "boolean"
          },
          "price" : {
            "type" : "double"
          },
          "title" : {
            "type" : "text",
            "store" : true
          },
          "type" : {
            "type" : "integer"
          }
        }
      }
    }
  }
}

# 新增一个字段，那么需要修改mapping
$ curl -XPOST "http://127.0.0.1:9200/productindex/product/_mapping" -d '
quote> {
quote>   "product": {
quote>     "properties": {
quote>       "amount": {"type": "integer"}
quote>     }
quote>   }
quote> }'
{"acknowledged":true}%
```

注意：不能修改一个字段的type？原因是一个字段的类型修改以后，那么该字段的所有数据都需要重新索引。Elasticsearch底层使用的是lucene库，字段类型修改以后索引和搜索要涉及分词方式等操作。





