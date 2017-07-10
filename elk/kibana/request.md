在输入框输入: hello world, 其实是 or 操作，hello OR world, 可加双引号来匹配整个短语。

指明字段： `line_id:86169`

用 `AND/OR` 来组合复杂的搜索, 如`("played upon" OR "every man") AND stage`

数值类型的数据可以直接搜索范围：

```bash
line_id:[30000 TO 80000] AND havoc
```


