wc 统计文件信息：

```bash
#显示文件内容信息,输出信息依次是:行数,字数,字节数,文件名称  
wc filename  
  
#显示一个文件的行数  
wc -l filename  
  
#显示一个文件的字节数  
wc -c filename  
  
#显示一个文件的字符数  
wc -m filename  
  
#显示一个文件中的最长行的长度  
wc -L filename  
  
#注意：每行结尾的换行符也算一个字符，空格也算一个字符  
#采用UTF-8编码，所以一个汉字在这里被转换为3字节  
#当使用-m选项时，一个汉字就作为一个字符计算  
```

如统计这个项目的行数和我写了多少字了：

```bash
$ find . -name "*.md" -print0|xargs -0 wc -l
...
8947 total

$ find . -name '*.md' -print0 |xargs -0 wc -m
...
207922 total
```

看来我写了不少了。。。


