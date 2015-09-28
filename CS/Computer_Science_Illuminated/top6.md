第六章是**问题求解和算法设计**， 主要将分析问题求解的方法和伪代码的运用。总结如下：

- 计算机领域的问题求解过程三个阶段：分析和说明阶段、算法开发阶段、实现阶段和维护阶段
- 开发算法实现：自顶向下设计(又称功能分解)和面向对象设计(OOD)
- 伪代码(pseudocode):的一些概念
	1. 变量：名字，引用的是存储值的位置
	2. 赋值：Set param to 1, 或 param <— 1; 赋值语句则：Set param to decimalNumber DIV newBase, 或 param <— decimalNumber DIV newBase
	3. 当变量用于to或者<—的右边，就能访问存储它的值；反之则存入如2
	4. 输入/输出：注意write输出，read输入，输入(Read/Get/Input param), 输出(Write/Display/print param)
	5. 算术表达式可以使用通常的算术运算符（+，-，*，/，以及表示幂的^）。逻辑表达式可以使用关系运算符=,≠,<,>,≤和≥，以及逻辑运算符与(and),或（or），非（not）。
	6. 若a和b都是变量、数组项，那么记号a<->b 表示a和b的内容进行交换。
	7. goto语句具有形式 goto label（goto标号）
	8. 条件语句有以下两种形式：`if c then s`或者 `if c then s else b`
	9. while: `while c do  s end`
	10. for: `for var init to limit by incr do s end`
	11. 算法中的注释被括在/* */之中。诸如read和output之类的各种输入或者输出也在需要时被用到



如下伪代码实例：

	Set param to 7
	param2 <- 10
	while(param > param2)
		/*缩进*/
		Read param2
		Print param2
		Write "good!"

ref:[伪代码的写法](http://www.cnblogs.com/huipengkankan/archive/2011/07/28/2120416.html)

Over~


