## 3.3.5 match 查询

`match {“field”: “xx yy cc”}`, 匹配field字段含有xx,xx词条（注意是词条）的文档,默认是`or`操作，如

```bash
$ curl 'localhost:9200/library/_search?pretty' -d '{"query": {"match": {"title": "crime and jack"}}, "_source": ["title"]}'
{
  "took" : 2,
  "timed_out" : false,
  "_shards" : {
    "total" : 5,
    "successful" : 5,
    "failed" : 0
  },
  "hits" : {
    "total" : 2,
    "max_score" : 1.113083,
    "hits" : [
      {
        "_index" : "library",
        "_type" : "book",
        "_id" : "4",
        "_score" : 1.113083,
        "_source" : {
          "title" : "Crime and Punishment"
        }
      },
      {
        "_index" : "library",
        "_type" : "book",
        "_id" : "AV3QLWO8rymwwQlmv5TR",
        "_score" : 0.7594807,
        "_source" : {
          "title" : "crime and jack"
        }
      }
    ]
  }
}
```

它把 crime, and ,jack 词条给查出来了，默认是or操作，包含这三者任何一个都会被检索出来。

可加入`opeartor`参数，选择`and`

```bash
$ curl 'localhost:9200/library/_search?pretty' -d '{"query": {"match": {"title": {"query": "crime and jack", "operator": "and"}}}, "_source": ["title"]}'
{
  "took" : 19,
  "timed_out" : false,
  "_shards" : {
    "total" : 5,
    "successful" : 5,
    "failed" : 0
  },
  "hits" : {
    "total" : 1,
    "max_score" : 0.7594807,
    "hits" : [
      {
        "_index" : "library",
        "_type" : "book",
        "_id" : "AV3QLWO8rymwwQlmv5TR",
        "_score" : 0.7594807,
        "_source" : {
          "title" : "crime and jack"
        }
      }
    ]
  }
}
```

### match_phrase 短语查询

短语查询是从分析后的文本中构建短语查询。比如短语查询"crime jack" 中间去掉了'and'

```bash
$ curl 'localhost:9200/library/_search?pretty' -d '{"query": {"match_phrase": {"title": "crime jack"}}, "_source": ["title"]}'
{
  "took" : 10,
  "timed_out" : false,
  "_shards" : {
    "total" : 5,
    "successful" : 5,
    "failed" : 0
  },
  "hits" : {
    "total" : 0,
    "max_score" : null,
    "hits" : [ ]
  }
}
```

没有查到值，这里要用到`match_phrase`的`slop`参数了。`slop`整数，表示词条直接允许有多少个未知词条，比如"i * you", 允许i和you之间有1个未知词条，那么这个未知词条可以是"love", 或 "hate"。如果slop为0则表示不允许有额外词条，接下来用`slop`允许crime jack 之间有1个未知词条来查询下：

```bash
$ curl 'localhost:9200/library/_search?pretty' -d '{"query": {"match_phrase": {"title": {"query": "crime jack", "slop": 1}}}, "_source": ["title"]}'
{
  "took" : 2,
  "timed_out" : false,
  "_shards" : {
    "total" : 5,
    "successful" : 5,
    "failed" : 0
  },
  "hits" : {
    "total" : 1,
    "max_score" : 0.3164503,
    "hits" : [
      {
        "_index" : "library",
        "_type" : "book",
        "_id" : "AV3QLWO8rymwwQlmv5TR",
        "_score" : 0.3164503,
        "_source" : {
          "title" : "crime and jack"
        }
      }
    ]
  }
}
```

### 通过id进行查询

最简单就是 /index/type/id?pretty, 在这本书上的查询多个id的例子是：

```json
{"query": {"ids": {"values": [2, 4]}}}
```

但在[最新的文档中是这样的](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-id-field.html)

```json
{
  "query": {
    "terms": {
      "_id": [ "1", "2" ] 
    }
  }
}
```

第一种更加简洁，第二种更加一致性吧。

可加上type做关联

![](http://beginman.qiniudn.com/2017-08-11-15024570243388.jpg)

### 前缀后缀查询

SQL里的 like操作

```json
{"query": {"prefix": {"title": "cri"}}}
```


