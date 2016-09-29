https://blog.nelhage.com/2009/12/a-brief-introduction-to-termios/

https://blog.nelhage.com/2009/12/a-brief-introduction-to-termios-termios3-and-stty/

https://blog.nelhage.com/2010/01/a-brief-introduction-to-termios-signaling-and-job-control/

# A Brief Introduction to Termios
如果你是一个 UNIX 终端用户，会很多你认为理所当然，但却没有认真的思考过的行为。
比如按下 `^C` 和 `^Z` 可以 kill 掉程序 和 stop 前台程序 - 
 当你 ssh 到 一台远程主机
 
 
 
## The terminal device
Unix 中终端抽象成为 'terminal' 设备，简写为 `tty`。在今天你是不会和一个物理终端交互的，一般都是和"伪终端"(pseudo-terminal)交互，
简称'pty'，伪终端是一个纯虚拟结构，一个伪终端简单来说是一对端点(实现为 /dev 下的字符设备)，它们提供了一个双向的通信通道。
无论从哪一端写入，都可以从另一端读出，反之亦然。这对儿端点通常叫做 "master" 端和 "slave" 端，
与管道和 socket 不同，它们并不是直接传递数据，终端设备特别之处是在 master 和 slave 之间，有一个中间层可以用来过滤，转发，回应两段的数据流。

通常 master 是连接你的终端模拟器(如 xterm)的一端，而 slave 是连接程序(例如 shell)的一端。
"输入"会从用户到 master 再到 slave，"输出"则从 程序 到 slave 再到 master，基本的过程如下所示:

![](img/termios.png)

这幅图简化了许多过程，但表达主要的过程。

## What happens in the middle?
中间的方块我标记为 "termios"，就是第一段里提到中间层，主要行为如下:
* Line buffering – 当字符从左侧进入,它会保存直到收到换行,同时把整行一次性发送出去。
* Echo – 当字符从左侧进入, 除了Line buffering,它会把字符返回到左侧，这就是为什么你会看到你打的字。
* Line editing – 当 ERASE 字符 (^?, ASCII 默认为 0x7f)从左侧进入，假设输入缓冲有内容，最后一个字符会被删除，
 并且序列 "\b \b" 发送到左侧。"\b" (ASCII 0x08) 是告诉你的终端把游标往左移动一格(删除键)，具体是先往左移动一格，
 将光标所在字符替换为空格，再把光标移动回去。
* Newline translation – 如果换行("\n", ASCII 0x0A) 进入右侧，一个 carriage-return/line-feed  (CRLF, "\r\n", ASCII 0x0D 0x0A)
发送到左侧，大多 UNIX 程序接受 "\n" 为换行，你的终端将需要两种 - "\r" 把游标移动到行首，"\n" 把游标移动到下一行。
* Signal generation - 生成信号，如果 `INTR` (^C, ASCII 0x3) 进入左侧，信号被丢弃，然后 `SIGINT` 发送到右侧的程序，
同样的，`SUSP` (^Z, ASCII 0x1A) 进入左侧，一个 `SIGTSTP` 会到右侧的程序(SIGTSTP 默认是停止一个进程，它和 SIGSTOP 的主要区别是
它可以被程序捕获和处理，而 SIGSTOP 是无条件的)。 

除了图中的还有2种特殊情况：

"termios" 并不是严格地在中间，它也知道右侧的程序，也可以和程序交互而不仅仅是把字符发给 slave。
    
salve 可以连接多个程序，但是哪个才允从中去读？应该把 SIGINT 或 SIGTSTP 发个谁？这个答案非常复杂，我并不是完全了解，
但我知道一些基本原则。这在下篇文章里会讲。

## Termios(3) and Stty
这一节我们看看  "termios" 控制行为的接口，如果右侧程序使用了 curses (如vim or emacs)，或者仅仅用了 readline(如 bash)，
就可以自定义一些行为了。

termios 主要的编程接口是 `struct termios`  和 2个函数:
```c
int tcgetattr(int fd, struct termios *termios_p);
int tcsetattr(int fd, int optional_actions,
             const struct termios *termios_p);
```
他们检索和设置 `struct termios` 所关联的终端设备。这些东西都文档化在 `termios(3)`。

关于 `struct termios` POSIX 规定了这个结构至少包含如下成员:
```c
tcflag_t c_iflag;      /* input modes */
tcflag_t c_oflag;      /* output modes */
tcflag_t c_cflag;      /* control modes */
tcflag_t c_lflag;      /* local modes */
```
每个 "flag" 成员都包含一组标志位(bitmask 实现)，每个标志位可以单独的开启或关闭。
c_iflag 和 c_oflag 包含的标志位们影响输入和输出的处理，c_cflag 我们通常会忽略，
他的设置和一些过时的东西如串行线路，modem 的控制有关。c_lflag 也需是最有趣的，
它控制 tty 的 board-scale 行为，我们来看看几个有趣的 bit 位:

### local mode
* ICANON - 它也许是 c_lflag 最重要的标志位，开启它会打开 "canonical" 模式 - 也就是行编辑模式，
关闭它，输入会立刻对程序可用(也就是 cbreak 模式)
* c_lflag 的 ECHO 控制了输入是否立刻回显到屏幕，它和 ICANON 是独立的，虽然他们经常一起关闭或开启。
当 passwd 提示你输入密码时，你的终端进入 "canonical" 模式 但 ECHO 是关闭的。
* ISIG 控制了 ^C 和 ^Z 等等是否产生信号，关闭后直接传递字符串而不是用信号代替。 

### input and output modes
c_iflag 和 c_oflag 也有值得一看的:
* c_iflag IXON 开启  "flow control"， 由 ^S 和 ^Q (默认)。开启 IXON，当 master 收到 ^S，
slave 将不接受任何输出(写入它会卡住)，直到 ^Q 被 master 接收。
* c_iflag IUTF8 在 canonical 模式，退格键需要删除之前的缓冲区字符，非 ASCII 编码的情况，
一个字符会有多个字节，但终端只会看到流中的一个字节，没有关于编码信息或字符边界。IUTF8 会告诉终端
字符是 utf-8 编码的，这样就可以正确的删除字符了。如果 IUTF8 关闭，键入多字节的字符，当你使用退格键，
仅会删除最后一个字节，留下的是损坏的utf-8字节流。
* c_oflag OLCUC 映射输出的小写到大写。这仅仅是为了当你需要字母看起都都是大写时准备的。

还有很多标志位，例如控制换行和字符删除，这些内容都在 termios(3)。

### c_cc
c_cc 成员里有许多和终端交互的控制字符。例如 ^C and ^Z and `delete`，它们对 termios 的含义并不是硬编码的，
而是定义在 c_cc 数组。

c_cc 以索引来控制，索引所对应的值是字符，
* VINTR – 生成一个 SIGINT (^C by default).
* VSUSP – 生成一个 SIGTSTP (stop the program) (^Z by default).
* VERASE – 删除之前字符. 应该是 ^H and ^? (ASCII 0x7f) by default – 如果你不按 "backspace" 而是由 ^H 来代替，
 你的终端和你的 `struct termios` 不同意 VERASE的值.

VEOF – End of file. Sends the current line to the program without waiting for 


