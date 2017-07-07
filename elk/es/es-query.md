先过一遍文档：[**QUERY DSL**](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)

HTTP Method:

- GET 检索文档
- DELETE方法删除文档
- HEAD方法检查某文档是否存在。
- PUT更新已存在的文档。


# 简单查找

## 查询字符串(query string)搜索

```bash
$ curl -XGET 'localhost:9200/megacorp/employee/_search?q=last_name:Smith&pretty'
```

## DSL语句查询

DSL(Domain Specific Language特定领域语言)以JSON请求体的形式出现。

注意很多老的中文文档，有`filtered`这个玩意，在5.0版本已经废弃了，用[`bool/must/filter`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html)来替代

老版本：

```bash
GET /megacorp/employee/_search
{
    "query" : {
        "filtered" : {
            "filter" : {
                "range" : {
                    "age" : { "gt" : 30 }
                }
            },
            "query" : {
                "match" : {
                    "last_name" : "smith"
                }
            }
        }
    }
}
```

新版本：

```bash
GET megacorp/employee/_search
{
  "query": {
    "bool": {
      "filter": {
        "range": {
          "age": {"gt": 30}
        }
      },
      "must": {
        "match": {
          "last_name": "smith"
        }
      }
    }
  }
}
```

**全文检索：**

```bash
GET megacorp/employee/_search
{
  "query": {
    "match": {
      "about": "rock climbing"
    }
  },
  "_source": ["about", "first_name", "last_name"]
}
```

返回：

![](http://beginman.qiniudn.com/2017-07-07-14994326087224.jpg)

Elasticsearch根据结果相关性评分来对结果集进行排序

**短语搜索**

比如查询同时包含"rock"和"climbing"（并且是相邻的）则上面的`match`就要换成`match_phrase`

# 精准查询

`term`: 这个过滤器旨在处理数字，布尔值，日期，和文本。

# 模糊查询

term 和 terms 是包含操作，而不是相等操作

# 组合查询

数据源：

```bash
POST /my_store/products/_bulk
{ "index": { "_id": 1 }}
{ "price" : 10, "productID" : "XHDK-A-1293-#fJ3" }
{ "index": { "_id": 2 }}
{ "price" : 20, "productID" : "KDKE-B-9947-#kL5" }
{ "index": { "_id": 3 }}
{ "price" : 30, "productID" : "JODL-X-1937-#pV7" }
{ "index": { "_id": 4 }}
{ "price" : 30, "productID" : "QQPX-R-3956-#aD8" }
```

如下SQL查询：

```sql
SELECT product
  FROM   products
  WHERE  (price = 20 OR productID = "XHDK-A-1293-#fJ3")
    AND  (price != 30)
```

在ES中需要 bool 过滤器。

bool 过滤器由三部分组成：

```json
{
   "bool" : {
      "must" :     [],
      "should" :   [],
      "must_not" : [],
   }
}
```

- must：所有分句都必须匹配，与 AND 相同。
- must_not：所有分句都必须不匹配，与 NOT 相同。
- should：至少有一个分句匹配，与 OR 相同。

上面的SQL语句在ES查询：

```bash
GET /my_store/products/_search
{
  "query": {
    "bool": {
      "should": [
        {"term": {"price": 20}},
        {"term": {"productID": "XHDK-A-1293-#fJ3"}}
      ],
      "must_not": {
        "term": {"price": 30}
      }
    }
  }
}
```

如下SQL：

```sql
SELECT document FROM products WHERE  productID  = "KDKE-B-9947-#kL5" 
OR (productID = "JODL-X-1937-#pV7" AND price = 30 )
```

ES来表示：

```bash
GET /my_store/products/_search
{
  "query": {
    "bool": {
      "should": [
        {"match": {"productID": "XHDK-A-1293-#fJ3"}},
        {
          "bool": {
            "must": [
              {"match": {"productID": "JODL-X-1937-#pV7"}},
              {"term": {"price": 30}}
            ]
          }
        }
      ]
    }
  }
}
```

注意；这里productID是未经分析的，所以如果用`term`则匹配不到，所以用了`match`。



