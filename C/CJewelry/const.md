`const`:常量修饰符，意即其所修饰的对象为常量(immutable)。

# 1、函数体内修饰局部变量

	int main() {
	    const int a=100;
	    a=3000;		// 报错
	    return 0;
	}

const作为一个类型限定词，和int有相同的地位。

	const int a;
	int const a;

两者等价

**要明白：const修饰的对象是谁，这里是a 和 int没关系， const 要求他所修饰的对象为常量，不可被改变，不可被赋值，不可作为左值（l-value)。**

这样的写法也是错误的。

	const int a;
	a=0;

这是一个很常见的使用方式：

	const double pi=3.14;

在程序的后面如果企图对pi再次赋值或者修改就会出错。

# 2.配合指针的使用

	const int* p;

还是先去掉const 修饰符号。注意，下面两个是等价的。

	int* p;
	int *p;

其实我们想要说的是，*p是int类型。那么显然，p就是指向int的指针,其实等价于:

	const int (*p);
	int const (*p);

即，*p是常量。也就是说，p指向的数据是常量。

于是

	p+=8; //合法
	*p=3; //非法，p指向的数据是常量。

那么如何声明一个自身是常量指针呢？方法是让const尽可能的靠近p;

	int* const p;

const右面只有p,显然，它修饰的是p,说明p不可被更改。然后把const去掉，可以看出p是一个指向 int形式变量的指针。

于是

	p+=8; //非法
	*p=3; //合法

**const 还有一个作用就是用于修饰常量静态字符串。**

例如：

	const char* name=David;

如果没有const,我们可能会在后面有意无意的写name[4]='x'这样的语句，这样会导致对只读内存区域的赋值，然后程序会立刻异常终止。有了 const,这个错误就能在程序被编译的时候就立即检查出来，这就是const的好处。让逻辑错误在编译期被发现。

**const 还可以用来修饰数组**

	const char s[]=David;

与上面有类似的作用。


