可重入性

Wiki - [Reentrancy (computing)]()
>  a reentrant procedure can be interrupted in the middle of its execution and then safely be called again("re-entered") before its previous invocations complete.

GNU Bison [3.7.11 A Pure (Reentrant) Parser](https://www.gnu.org/software/bison/manual/html_node/Pure-Decl.html)
> A `reentrant` program is one which does not alter in the course of execution; in other words, it consists entirely of pure (read-only) code. Reentrancy is important whenever asynchronous execution is possible; for example, a nonreentrant program may not be safe to call from a signal handler. In systems with multiple threads of control, a nonreentrant program must be called only within interlocks.

简言之就是程序被打断后可以继续安全执行而不产生错误. 打断可以说 jump or call, or by an external action such as an interrupt or signal. 
