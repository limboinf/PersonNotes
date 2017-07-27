## Tips

### 1.bash script loop through mysql query result:

```bash
$ mysql -uroot -p'!qaz2wsx' -Dmydb -e"select class_id, classroom, finish_type from my_record limit 10" | while read class_id classroom finish_type;do
    echo "$class_id, $classroom, $finish_type"
done

datas: class_id, classroom, finish_type
datas: 20974285, jz3be20fa01d894b0bbd95a029fa78b21c, ABC
datas: 20992096, jzd4cadcbf214b407e885bb8eb9dc7e555, ABC
datas: 20974287, jzda2941c582784f89ac4805d7a456a105, ABC
datas: 20992102, jzfcf2fb96b65f45c3a035d3db810aa364, ABC
```

or

```bash
$ mysql -uroot -p'!qaz2wsx' -Dmydb -e"select class_id, classroom, finish_type from my_record limit 10" | awk '{print "class_id: " $1  " classroom: " $2 " finish_type: " $3}'

class_id: class_id classroom: classroom finish_type: finish_type
class_id: 20974285 classroom: jz3be20fa01d894b0bbd95a029fa78b21c finish_type: ABC
class_id: 20992096 classroom: jzd4cadcbf214b407e885bb8eb9dc7e555 finish_type: ABC
class_id: 20974287 classroom: jzda2941c582784f89ac4805d7a456a105 finish_type: ABC
class_id: 20992102 classroom: jzfcf2fb96b65f45c3a035d3db810aa364 finish_type: ABC
```

### 2.批量插入：

```bash
$ yes "insert into my_finish_classid_reason(class_id,reason_id) values (1000, 3);"|head -n 10000 | mysql -uroot -p'!qaz2wsx' -Dmydb

$ echo "select count(1) from my_finish_classid_reason" | mysql -uroot -p'!qaz2wsx' -Dmydb
count(1)
10000
```

上述会多次连接mysql, 下面或许更好些：

```bash
$ var="insert into my_finish_classid_reason(class_id,reason_id) values "
$ for i in `seq 10`;do var+="($i, 10)," done
$ cmd=$(echo "$var" | sed 's/,$//g')
$ echo $cmd
insert into my_finish_classid_reason(class_id,reason_id) values (1, 10),(2, 10),(3, 10),(4, 10),(5, 10),(6, 10),(7, 10),(8, 10),(9, 10),(10, 10)
$ echo $cmd|mysql -uroot -p'!qaz2wsx' -Dmydb
```

## Notes

### 1. not in or in 优化方法

```sql
-- in
select A.id from A where A.id in (select B.id from B)

-- better:
select a.id from A a left join B b on b.id = a.id where b.id is not null 

-- not in
select A.id from A where A.id not in (select B.id from B)

--better:
select a.id from A a left join B b on b.id = a.id where b.id is null 
```

ref: [NOT IN vs. NOT EXISTS vs. LEFT JOIN / IS NULL: MySQL](https://explainextended.com/2009/09/18/not-in-vs-not-exists-vs-left-join-is-null-mysql/)




