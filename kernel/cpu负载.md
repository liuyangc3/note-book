CPU负载可以通过 /proc/loadavg 查看

```
cat /proc/loadavg
0.00 0.00 0.00 1/139 9244
```
为了理解每个列到底什么意思，我们来看下代码：

```c
// fs/proc/loadavg.c 2.6.32

#define LOAD_INT(x) ((x) >> FSHIFT)
#define LOAD_FRAC(x) LOAD_INT(((x) & (FIXED_1-1)) * 100)

static int loadavg_proc_show(struct seq_file *m, void *v)
{
	unsigned long avnrun[3];

	get_avenrun(avnrun, FIXED_1/200, 0);

	seq_printf(m, "%lu.%02lu %lu.%02lu %lu.%02lu %ld/%d %d\n",
		LOAD_INT(avnrun[0]), LOAD_FRAC(avnrun[0]),
		LOAD_INT(avnrun[1]), LOAD_FRAC(avnrun[1]),
		LOAD_INT(avnrun[2]), LOAD_FRAC(avnrun[2]),
		nr_running(), nr_threads,
		task_active_pid_ns(current)->last_pid);
	return 0;
}
```
可以看到前3个列的格式是 xx.xx xx.xx xx.xx 对应的代码是
```
LOAD_INT(avnrun[n]).LOAD_FRAC(avnrun[n])
```
因为Linux内核是不允许浮点运算的，所以这里有个trick，用一个整数来表示小数，
通过宏LOAD_INT计算整数部分，而LOAD_FRAC计算小数部分。

第四列 1/139 是 这两个值 nr_running()/nr_threads，所以1表示正在运行的task数量，而139表示总task数量。这里统计的是所有cpu的和

第五列 9244 task_active_pid_ns(current)->last_pid， 最后一个task的pid

我们可以验证一下，写个脚本 t.sh
```
seleep 1000
```
然后运行 sh t.sh &,用过ps得到该进程的pid是9272
```
root      9272  9271  0 11:39 pts/0    00:00:00 sleep 1000
root      9277  9229  0 11:41 pts/0    00:00:00 ps -ef
```
然后运行 cat /proc/loadavg
```
[root@web ~]# cat /proc/loadavg
0.00 0.00 0.00 1/141 9278
[root@web ~]# cat /proc/loadavg
0.00 0.00 0.00 1/141 9279
[root@web ~]# cat /proc/loadavg
0.00 0.00 0.00 1/141 9280
```
可以看到 pid 不断增加， 因为cat 命令也是进程，所以cat 时会产生一个进程，last_pid会加1

下面具体看看load是如何计算的

首先计算中多次出现FIXED_1/FSHITF，这些个宏的定义在
```c
// linux/sched.h 2.6.32

/*
 * These are the constant used to fake the fixed-point load-average
 * counting. Some notes:
 *  - 11 bit fractions expand to 22 bits by the multiplies: this gives
 *    a load-average precision of 10 bits integer + 11 bits fractional
 *  - if you want to count load-averages more often, you need more
 *    precision, or rounding will get you. With 2-second counting freq,
 *    the EXP_n values would be 1981, 2034 and 2043 if still using only
 *    11 bit fractions.
 */
extern unsigned long avenrun[];		/* Load averages */
extern void get_avenrun(unsigned long *loads, unsigned long offset, int shift);

#define FSHIFT		11		/* nr of bits of precision */
#define FIXED_1		(1<<FSHIFT)	/* 1.0 as fixed-point */
#define LOAD_FREQ	(5*HZ+1)	/* 5 sec intervals */
#define EXP_1		1884		/* 1/exp(5sec/1min) as fixed-point */
#define EXP_5		2014		/* 1/exp(5sec/5min) */
#define EXP_15		2037		/* 1/exp(5sec/15min) */

#define CALC_LOAD(load,exp,n) \
	load *= exp; \
	load += n*(FIXED_1-exp); \
	load >>= FSHIFT;
```

首先 采样计算load时间间隔为5秒，宏 LOAD_FREQ

这里面有2个问题

* CALC_LOAD 的作用
* magic numbers : EXP_1,EXP_5,EXP_15 , 1884, 2014, 2037 是什么

Exponential smoothing
------
Exponential smoothing,指数平滑

通常情况下计算一个集合{X1,X2...Xn}所有元素的平均值s，需要所有元素的和sum(X)和集合元素的个数n
```
s = sum(Xn) / n
```
当我们有一个基于时间序列的数据集时，![{Xt}](img/ES01.png),开始的时间是t=0，

![xt](img/ES01.png)



1/139 ， 1表示

https://luv.asn.au/overheads/NJG_LUV_2002/luvSlides.html

https://www.teamquest.com/import/pdfs/whitepaper/ldavg1.pdf
https://www.teamquest.com/import/pdfs/whitepaper/ldavg2.pdf

http://www.makelinux.net/books/lkd2/ch04lev1sec2