## 1.Overview

avro是RPC和数据序列化系统(data serialization system)，使用JSON定义数据类型及通信协议，使用**压缩二进制**来序列化数据，是Hadoop**持久化**数据的一种序列化格式。

<!-- more -->


### 2.1 maven 配置

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.datalimbo.qos</groupId>
    <artifactId>AvroEgg</artifactId>
    <version>1.0-SNAPSHOT</version>

    <dependencies>
        <dependency>
            <groupId>org.apache.avro</groupId>
            <artifactId>avro</artifactId>
            <version>1.8.2</version>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <!--avro代码生成-->
            <plugin>
                <groupId>org.apache.avro</groupId>
                <artifactId>avro-maven-plugin</artifactId>
                <version>1.8.2</version>
                <executions>
                    <execution>
                        <phase>generate-sources</phase>
                        <goals>
                            <goal>schema</goal>
                        </goals>
                        <configuration>
                            <sourceDirectory>${project.basedir}/src/main/resources/avro/</sourceDirectory>
                            <outputDirectory>${project.basedir}/src/main/java/</outputDirectory>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <source>1.6</source>
                    <target>1.6</target>
                </configuration>
            </plugin>
        </plugins>
    </build>

</project>
```

avro可以以代码生成的方式和非代码生成方式进行，关于maven avro build可参考：[https://cwiki.apache.org/confluence/display/AVRO/Build+Documentation]([Build Documentation](https://cwiki.apache.org/confluence/display/AVRO/Build+Documentation))



### 2.2 定义Avro schema

基于json, 关于数据结构可参考：[Apache Avro™ 1.8.2 Specification](https://avro.apache.org/docs/current/spec.html#schema_primitive)，如下`user.avsc`（schema文件是avsc文件注意后缀是`avsc`)

```json
{"namespace": "com.datalimbo.qos.avro",
 "type": "record",
 "name": "User",
 "fields": [
     {"name": "name", "type": "string"},
     {"name": "favorite_number",  "type": ["int", "null"]},
     {"name": "favorite_color", "type": ["string", "null"]}
 ]
}
```

在模式定义中，必须包含它的类型("type": "record")、一个名字("name": "User")以及fields

### 2.3 代码生成方式的序列化和反序列化

```java
package com.datalimbo.qos;

import com.datalimbo.qos.avro.User;

import org.apache.avro.file.DataFileReader;
import org.apache.avro.file.DataFileWriter;
import org.apache.avro.io.DatumReader;
import org.apache.avro.io.DatumWriter;
import org.apache.avro.specific.SpecificDatumReader;
import org.apache.avro.specific.SpecificDatumWriter;

import java.io.File;
import java.io.IOException;

/**
 * 方式1：指定生成代码形式的序列化和反序列化
 * Usage:
 *  $ mvn compile # includes code generation via Avro Maven plugin
 *  $ mvn -q exec:java -Dexec.mainClass=example.SpecificMain
 *
 * created by fangpeng 2018-10-15 15:00
 **/
public class SpecificMain {

    public static void main(String[] args) {
        // 创建用户
        User user1 = new User();
        user1.setName("Lucy");
        user1.setFavoriteNumber(256);
        // Leave favorite color null

        User user2 = new User("Ben", 7, "red");

        User user3 = User.newBuilder()
                .setName("Jack")
                .setFavoriteNumber(null)
                .setFavoriteColor("green")
                .build();

        System.out.println(user1.toString());
        System.out.println(user2.toString());
        System.out.println(user3.toString());

//         output:
//        {"name": "Lucy", "favorite_number": 256, "favorite_color": null}
//        {"name": "Ben", "favorite_number": 7, "favorite_color": "red"}
//        {"name": "Jack", "favorite_number": null, "favorite_color": "green"}

        String avrofile = "users.avro";
        // 序列化user1,2,3到磁盘
        serializing(user1, user2, user3, avrofile);
        // 反序列化
        Deserializing(avrofile);
    }

    private static void serializing(User user1, User user2, User user3, String avrofile) {
        // Serialize user1, user2 and user3 to disk
        // DatumWriter 将Java对象转换成内存序列化格式(in-memory serialized format)
        // SpecificDatumWriter 用于生成的类并从指定的生成类型中提取模式
        DatumWriter<User> userDatumWriter = new SpecificDatumWriter<User>(User.class);
        // DataFileWriter 写入序列化记录以及模式到dataFileWriter.create调用中指定的文件
        DataFileWriter<User> dataFileWriter = new DataFileWriter<User>(userDatumWriter);

        try {
            dataFileWriter.create(user1.getSchema(), new File(avrofile));
            // append方法写入user对象
            dataFileWriter.append(user1);
            dataFileWriter.append(user2);
            dataFileWriter.append(user3);
            // 写入完成后关闭文件
            dataFileWriter.close();
            System.out.println("写入users.avro成功");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void Deserializing(String avrofile) {
        // 反序列化
        // SpecificDatumReader converts in-memory serialized items into instances of our generated class, in this case User.
        DatumReader<User> datumReader = new SpecificDatumReader<User>(User.class);
        try {
            // DataFileReader 从磁盘中读取avro文件
            DataFileReader<User> dataFileReader = new DataFileReader<User>(new File(avrofile), datumReader);

            // 创建单个User对象用于存储迭代中的反序列化user
            User user = null;
            while (dataFileReader.hasNext()) {
                // 传递user对象给next方法，这是一种性能优化，允许DataFileReader重用相同的User对象，而不是为每次迭代分配新用户
                // 如果我们反序列化大型数据文件，这在对象分配和垃圾收集方面可能非常昂贵
                user = dataFileReader.next(user);
                System.out.println("读取 > " + user.toString());
            }
            dataFileReader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

编译schema, 在非maven build 下的命令行模式可以

```bash
# java -jar /path/to/avro-tools-1.8.2.jar compile schema <schema file> <destination>
$ java -jar /path/to/avro-tools-1.8.2.jar compile schema user.avsc .
```

如果配置了上面maven build项，可直接

```bash
$ mvn compile # includes code generation via Avro Maven plugin
```

然后执行：

```bash
$ mvn -q exec:java -Dexec.mainClass=com.datalimbo.qos.SpecificMain 

"name": "Lucy", "favorite_number": 256, "favorite_color": null}
{"name": "Ben", "favorite_number": 7, "favorite_color": "red"}
{"name": "Jack", "favorite_number": null, "favorite_color": "green"}
写入users.avro成功
读取 > {"name": "Lucy", "favorite_number": 256, "favorite_color": null}
读取 > {"name": "Ben", "favorite_number": 7, "favorite_color": "red"}
读取 > {"name": "Jack", "favorite_number": null, "favorite_color": "green"}
```



### 2.4 非代码生成方式的序列化和反序列化

```java
package com.datalimbo.qos;

import org.apache.avro.Schema;
import org.apache.avro.file.DataFileReader;
import org.apache.avro.file.DataFileWriter;
import org.apache.avro.generic.GenericData;
import org.apache.avro.generic.GenericDatumReader;
import org.apache.avro.generic.GenericDatumWriter;
import org.apache.avro.generic.GenericRecord;
import org.apache.avro.io.DatumReader;
import org.apache.avro.io.DatumWriter;

import java.io.File;
import java.io.IOException;

/**
 * created by fangpeng 2018-10-15 16:32
 **/
public class GenericMain {

    public static void main(String[] args) {
        withoutCodeGenerationVersion();
    }

    // 方式2：非生成代码方式的序列化和反序列化
    private static void withoutCodeGenerationVersion() {
        try {
            ClassLoader classLoader = SpecificMain.class.getClassLoader();
            File file = new File(classLoader.getResource("avro/user.avsc").getFile());
            // Parse读取schema
            Schema schema = new Schema.Parser().parse(file);
            // 使用GenericRecord从schema中创建用户
            GenericRecord user1 = new GenericData.Record(schema);
            user1.put("name", "张三");
            user1.put("favorite_number", 256);
            System.out.println(user1);

            // 序列化
            DatumWriter<GenericRecord> datumWriter = new GenericDatumWriter<GenericRecord>(schema);
            DataFileWriter<GenericRecord> dataFileWriter = new DataFileWriter<GenericRecord>(datumWriter);
            dataFileWriter.create(schema, new File("users-v2.avro"));
            dataFileWriter.append(user1);
            dataFileWriter.close();


            // 反序列化
            DatumReader<GenericRecord> datumReader = new GenericDatumReader<GenericRecord>(schema);
            DataFileReader<GenericRecord> dataFileReader = new DataFileReader<GenericRecord>(new File("users-v2.avro"), datumReader);
            GenericRecord user = null;
            while (dataFileReader.hasNext()) {
                user = dataFileReader.next(user);
                System.out.println("Read: " + user);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
```

执行：

```bash
$ mvn compile
$ mvn -q exec:java -Dexec.mainClass=com.datalimbo.qos.GenericMain 

{"name": "张三", "favorite_number": 256, "favorite_color": null}
Read: {"name": "张三", "favorite_number": 256, "favorite_color": null}
```



## 3 Avro工具

使用Avro工具检查Avro数据文件

![image-20181015170048735](https://ws1.sinaimg.cn/large/006tNbRwly1fw90ka7gdkj30ha066adx.jpg)

如果是jar包可以

```bash
$ java -jar avro-tools-1.8.2.jar tojson AvroEgg/users.avro  
```



## 4.使用场景

avro与Hadoop生态系统结合最好

Hive表定义可以直接用avro schema来声明，Hive里用它来序列化日志文件，优点是可以直接用avro schema替代Hive本身表结构定义，这样能比较方便的解决schema evolution问题

在kafka和Flume 中也有很多使用avro的. flume主要的RPC source就是Avro source, 与 Avro sink, FlumeSDK等构成Flume内部通信

## 5.参考

- [Apache Avro](https://zh.wikipedia.org/wiki/Apache_Avro)
- [Apache Avro™ 1.8.2 Documentation](https://avro.apache.org/docs/current/index.html)
- [Apache Avro™ 1.8.2 Getting Started (Java)](https://avro.apache.org/docs/current/gettingstartedjava.html)
- [Avro schema,序列化框架的金领](https://zhuanlan.zhihu.com/p/24803426)
- [在Hive中使用Avro](https://www.iteblog.com/archives/1007.html)

