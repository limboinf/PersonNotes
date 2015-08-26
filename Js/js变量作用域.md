
# NO1: Js 作用域链

作用域链：JavaScript需要查询一个变量x时，首先会查找作用域链的第一个对象，如果以第一个对象没有定义x变量，JavaScript会继续查找有没有定义x变量，如果第二个对象没有定义则会继续查找，以此类推。

下面的代码涉及到了三个作用域链对象，依次是：first,second,thrid。

**局部变量优先级 > 全局变量**


	var arr = 1;
	function first () {
		arrs=1000;
		function second () {
			arrs=100;
			function third () {
				var arrs = 10;
				console.log(arr);
			}
			third()		// 调用
		}
		second();		// 调用
	}

	first();		// 1


# NO2: JavaScript没有块级作用域。
变量i、j、k作用域是相同的，他们在整个rain函数体内都是全局的


	function rain() {
		// 函数体内存在三个局部变量 i j k
		var i=0;
		if (1) {
			var j = 0;
			for (var k=0; k<3; k++) {
				console.log(k);		// 0,1,2
			}
			console.log(k)			// 3 (k++), 调用未声明变量
		}
		console.log(j);				// 0
	}

	rain();


# NO3.函数中声明的变量(var xxx)在整个函数中都有定义。


	function ts() {
		var m = 0;
		function tts() {
			console.log(m);		// 0
			m = 1000
		}
		tts();
		console.log(m);			// 1000
	}

	ts();


在函数ts2内局部变量x在整个函数体内都有定义（ var x= 'rain-man'，进行了声明），
所以在整个ts2函数体内隐藏了同名的全局变量x。这里之所以会弹出'undefined'是因为，第一个执行console.log(x)时，局部变量x仍未被初始化。
等效于：
	
	function rain(){
	    var x;
	    alert( x );		// undefined
	    x = 'beginman';
	    alert( x );		// beginman
	}

如下：

	function ts2() {
		var m = 0;
		function tts() {
			console.log(m);			// undefined
			var m = "good";
		}
		tts();
		console.log(m);				// 0
	}

	ts2();

# No4. 未使用var 的变量属于全局变量


	function test1() {
		function chlid() {
			function child_2 () {
				// 未使用var
				x = 'beginman';
			}
			child_2();
		}
		chlid();

		console.log(x);		// beginman
	}
	// 调用
	test1();
	console.log(x);			// beginman


# NO5. 全局变量都是window对象的属性

	<script type="text/javascript">
	    var x = 100 ;
	    alert( window.x );//弹出100
	    alert(x);
	</script>
	等同于下面的代码

	<script type="text/javascript">
	    window.x = 100;
	    alert( window.x );
	    alert(x)
	</script>
	
## NO6.避免使用过多全局变量


避免使用全局变量。努力减少使用全局变量的方法：在应用程序中创建唯一一个全局变量，并定义该变量为当前应用的容器。


	var ARRS = {};  // 变量集

	ARRS.name = {
		"first_name": "方",
		"last_name": "朋",
	};

	ARRS.work = {
		number: 1001,
		one: {
			name: "one",
			time: "2014-2015",
			job: "web"
		},
		two: {
			name: "wto",
			time: "2015-2016",
			job: "python"
		}
	};

	console.log(ARRS.work.one.job);



