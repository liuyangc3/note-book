# ELF (Executable and Linkable Format)

## 1 什么是ELF
在介绍ELF前,需要先简单了解一下连接(link)的知识

我们写的程序代码,需要使用一些封装好的第三方代码(库),而把这些第三方代码载入程序代码的过程,就叫做`link`

一般有2种方式
* 静态连接

就是在编译阶段就把代码库加入到自己的代码,这样很不方便,文件体积过大

* 动态连接

和静态连接相反,代码在编译阶段并不完成跟代码库的连接,直到到目标映像运行时,才把代码库的映像也装入用户空间(并加以定位),再完成代码与库函数的连接

那么ELF就是二进制映像文件的格式规范,并且也是操作系统相对应的ABI的规范.

这些二进制映像文件包括:
* 可重定向文件
* 可执行文件 (如 shell 命令)
* object code (*.o)
* 共享库 (*.so)
* core dumps

## 2 为什么会出现ELF? 或者它的作用是什么
我们知道,任何操作系统在执行二进制文件时,都面临这相同的问题,就是
* 如何创建新的进程?
* 如何载入二进制映像到进程中?
* 如何运行二进制映像内的指令?

然而在计算机技术的发展历史中,并没有一个统一的规范来告诉操作系统来怎么做,那么进程加载程序并启动的过程就不可避免地呈现出多样性.

ELF的出现就是为了用来规范不同操作系统加载二进制文件的方式,为开发者提供相同定义的ABI,用以减少跨操作系统导致的重新编译,甚至代码重构.

最早是在Unix中出现,后来由TISC(Tool Interface Standard Committee)指定了标准


## 3 ELF文件格式

```
Link View                                Execution View
+----------------------+                 +----------------------+
|      ELF header      |                 |      ELF header      |
+----------------------+                 +----------------------+
| Program Header Table |                 | Program Header Table |
|       optional       |                 +----------------------+
+----------------------+                 |      Segment 1       |
|      Section 1       |                 +----------------------+
+----------------------+                 |      Segment 2       |
|      Section 2       |                 +----------------------+
+----------------------+                 |         ...          |
|         ...          |                 +----------------------+
+----------------------+                 |      Segment n       |
|      Section n       |                 +----------------------+
+----------------------+                 | Section Header Table |
| Section Header Table |                 |       optional       |
+----------------------+                 +----------------------+
```
对于可执行文件, 必须要有Segment

object文件(*.o),用于链接其他object文件,Section是必须的

动态链接库, 既有Section也有Segment

核心转储文件,当进程收到SIGABRT信号后生成,含有特定Segments (PT LOAD/PT NOTE)
### 3.1 ELF header
ELF header 主要描述了文件的类型,每个区域在文件内的偏移量

[ELF header](https://github.com/torvalds/linux/blob/master/include/uapi/linux/elf.h#L203)结构如下:
```
typedef struct elf32_hdr{
  ...
} Elf32_Ehdr;

typedef struct elf64_hdr {
  unsigned char	e_ident[EI_NIDENT];	/* ELF "magic number" 0x7fELF */
  Elf64_Half e_type;        /* REL,DYN,EXEC,CORE 可链接,可执行,动态库,核心转储 */
  Elf64_Half e_machine;     /* 体系结构 EM_X86_64 ... */
  Elf64_Word e_version;     /* always 1 */
  Elf64_Addr e_entry;		/* Entry point virtual address */
  Elf64_Off e_phoff;		/* Program header table file offset */
  Elf64_Off e_shoff;		/* Section header table file offset */
  Elf64_Word e_flags;       /* CPU-specific flags */
  Elf64_Half e_ehsize;      /* ELF header size */
  Elf64_Half e_phentsize;   /* size of program header enrty,consistency check */
  Elf64_Half e_phnum;       /* number of program header entries */
  Elf64_Half e_shentsize;   /* size of section header entry */
  Elf64_Half e_shnum;       /* number of section header entries */
  Elf64_Half e_shstrndx;    /* section header string table index */
} Elf64_Ehdr;
```
可以通过readelf命令查看文件的 ELF header:
```
$ readelf -Wh /lib64/ld-linux-x86-64.so.2
ELF Header:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00
  Class:                             ELF64
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
  Type:                              DYN (Shared object file)
  Machine:                           Advanced Micro Devices X86-64
  Version:                           0x1
  Entry point address:               0xb00
  Start of program headers:          64 (bytes into file)
  Start of section headers:          152704 (bytes into file)
  Flags:                             0x0
  Size of this header:               64 (bytes)
  Size of program headers:           56 (bytes)
  Number of program headers:         7
  Size of section headers:           64 (bytes)
  Number of section headers:         30
  Section header string table index: 29
```
这是一个可执行文件的`ELF Header`
```
ELF Header:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00
  Class:                             ELF64
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
  Type:                              EXEC (Executable file)
  Machine:                           Advanced Micro Devices X86-64
  Version:                           0x1
  Entry point address:               0x4003e0
  Start of program headers:          64 (bytes into file)
  Start of section headers:          2544 (bytes into file)
  Flags:                             0x0
  Size of this header:               64 (bytes)
  Size of program headers:           56 (bytes)
  Number of program headers:         8
  Size of section headers:           64 (bytes)
  Number of section headers:         30
  Section header string table index: 27
```

### 3.2 Program Header Table
`Program Header Table` 是结构体`elf64_phdr`数组,每个元素用来描述一个`segment`

`segment`包含了`section `

[Program Header](https://github.com/torvalds/linux/blob/master/include/uapi/linux/elf.h#L254) define
```
typedef struct elf64_phdr {
  Elf64_Word p_type;
  Elf64_Word p_flags;
  Elf64_Off p_offset;		/* Segment file offset */
  Elf64_Addr p_vaddr;		/* Segment virtual address */
  Elf64_Addr p_paddr;		/* Segment physical address */
  Elf64_Xword p_filesz;	  /* Segment size in file */
  Elf64_Xword p_memsz;	   /* Segment size in memory */
  Elf64_Xword p_align;	   /* Segment alignment, file & memory */
} Elf64_Phdr;
```
p_type 类型：
* PT_NULL Indicates an unused program header
* PT_LOAD 只有这个类型的segment可以被加载到内存，rtld(elf/rtld.c)负责加载, 多个PT_LOAD类型的`segment` 根据p_vaddr排序
* PT_DYNAMIC 说明`segment`保存动态链接的信息
* PT_INTERP 指向一个动态链接器
* PT_NOTE 保存一些ABI需要的信息,如内核版本号.核心转储文件里保存了进程的信息
* PT_SHLIB 保留`program header`的类型, ELF ABI一直没有实现
* PT_PHDR `segment`的地址
* PT_TLS `Thread-Local Storage template`

GNU 的对类型的扩展
* PT_GNU_EH_FRAME GCC使用这个类型查找异常的处理程序
* PT_GNU_STACK 是否需要可执行的栈, 内存栈的权限
* PT_GNU_RELRO 在动态重定向后,哪部分内存是read only的
* PT_GNU_HEAP 貌似 只有Gentoo 使用

`Program Header`的查看
```
$ readelf -Wl s
Elf file type is EXEC (Executable file)
Entry point 0x4003e0
There are 8 program headers, starting at offset 64

Program Headers:
  Type           Offset   VirtAddr           PhysAddr           FileSiz  MemSiz   Flg Align
  PHDR           0x000040 0x0000000000400040 0x0000000000400040 0x0001c0 0x0001c0 R E 0x8
  INTERP         0x000200 0x0000000000400200 0x0000000000400200 0x00001c 0x00001c R   0x1
      [Requesting program interpreter: /lib64/ld-linux-x86-64.so.2]
  LOAD           0x000000 0x0000000000400000 0x0000000000400000 0x0006d4 0x0006d4 R E 0x200000
  LOAD           0x0006d8 0x00000000006006d8 0x00000000006006d8 0x0001ec 0x000200 RW  0x200000
  DYNAMIC        0x000700 0x0000000000600700 0x0000000000600700 0x000190 0x000190 RW  0x8
  NOTE           0x00021c 0x000000000040021c 0x000000000040021c 0x000044 0x000044 R   0x4
  GNU_EH_FRAME   0x000634 0x0000000000400634 0x0000000000400634 0x000024 0x000024 R   0x4
  GNU_STACK      0x000000 0x0000000000000000 0x0000000000000000 0x000000 0x000000 RW  0x8

 Section to Segment mapping:
  Segment Sections...
   00
   01     .interp
   02     .interp .note.ABI-tag .note.gnu.build-id .gnu.hash .dynsym .dynstr .gnu.version .gnu.version_r .rela.dyn .rela.plt .init .plt .text .fini .rodata .eh_frame_hdr .eh_frame
   03     .ctors .dtors .jcr .dynamic .got .got.plt .data .bss
   04     .dynamic
   05     .note.ABI-tag .note.gnu.build-id
   06     .eh_frame_hdr
   07
```
### 3.3 Section Header Table
section 结构
```
typedef struct elf64_shdr {
  Elf64_Word sh_name;		/* Section name, index in string tbl */
  Elf64_Word sh_type;		/* Type of section */
  Elf64_Xword sh_flags;		/* Miscellaneous section attributes */
  Elf64_Addr sh_addr;		/* Section virtual addr at execution */
  Elf64_Off sh_offset;		/* Section file offset */
  Elf64_Xword sh_size;		/* Size of section in bytes */
  Elf64_Word sh_link;		/* Index of another section */
  Elf64_Word sh_info;		/* Additional section information */
  Elf64_Xword sh_addralign;	/* Section alignment */
  Elf64_Xword sh_entsize;	/* Entry size if section holds table */
} Elf64_Shdr;
```
查看section

```
readelf -WS execfile
There are 30 section headers, starting at offset 0x9f0:

Section Headers:
  [Nr] Name              Type            Address          Off    Size   ES Flg Lk Inf Al
  [ 0]                   NULL            0000000000000000 000000 000000 00      0   0  0
  [ 1] .interp           PROGBITS        0000000000400200 000200 00001c 00   A  0   0  1
  [ 2] .note.ABI-tag     NOTE            000000000040021c 00021c 000020 00   A  0   0  4
  [ 3] .note.gnu.build-id NOTE           000000000040023c 00023c 000024 00   A  0   0  4
  [ 4] .gnu.hash         GNU_HASH        0000000000400260 000260 00001c 00   A  5   0  8
  [ 5] .dynsym           DYNSYM          0000000000400280 000280 000060 18   A  6   1  8
  [ 6] .dynstr           STRTAB          00000000004002e0 0002e0 00003f 00   A  0   0  1
  [ 7] .gnu.version      VERSYM          0000000000400320 000320 000008 02   A  5   0  2
  [ 8] .gnu.version_r    VERNEED         0000000000400328 000328 000020 00   A  6   1  8
  [ 9] .rela.dyn         RELA            0000000000400348 000348 000018 18   A  5   0  8
  [10] .rela.plt         RELA            0000000000400360 000360 000030 18   A  5  12  8
  [11] .init             PROGBITS        0000000000400390 000390 000018 00  AX  0   0  4
  [12] .plt              PROGBITS        00000000004003a8 0003a8 000030 10  AX  0   0  4
  [13] .text             PROGBITS        00000000004003e0 0003e0 000228 00  AX  0   0 16
  [14] .fini             PROGBITS        0000000000400608 000608 00000e 00  AX  0   0  4
  [15] .rodata           PROGBITS        0000000000400618 000618 00001c 00   A  0   0  8
  [16] .eh_frame_hdr     PROGBITS        0000000000400634 000634 000024 00   A  0   0  4
  [17] .eh_frame         PROGBITS        0000000000400658 000658 00007c 00   A  0   0  8
  [18] .ctors            PROGBITS        00000000006006d8 0006d8 000010 00  WA  0   0  8
  [19] .dtors            PROGBITS        00000000006006e8 0006e8 000010 00  WA  0   0  8
  [20] .jcr              PROGBITS        00000000006006f8 0006f8 000008 00  WA  0   0  8
  [21] .dynamic          DYNAMIC         0000000000600700 000700 000190 10  WA  6   0  8
  [22] .got              PROGBITS        0000000000600890 000890 000008 08  WA  0   0  8
  [23] .got.plt          PROGBITS        0000000000600898 000898 000028 08  WA  0   0  8
  [24] .data             PROGBITS        00000000006008c0 0008c0 000004 00  WA  0   0  4
  [25] .bss              NOBITS          00000000006008c8 0008c4 000010 00  WA  0   0  8
  [26] .comment          PROGBITS        0000000000000000 0008c4 00002d 01  MS  0   0  1
  [27] .shstrtab         STRTAB          0000000000000000 0008f1 0000fe 00      0   0  1
  [28] .symtab           SYMTAB          0000000000000000 001170 000600 18     29  46  8
  [29] .strtab           STRTAB          0000000000000000 001770 0001ef 00      0   0  1
Key to Flags:
  W (write), A (alloc), X (execute), M (merge), S (strings)
  I (info), L (link order), G (group), x (unknown)
  O (extra OS processing required) o (OS specific), p (processor specific)

```

几个比较重要的section:

.text 存放编译后生成的机器码

.data 存放已经初始化的全局变量和局部静态变量

.bss 存放未初始化全局变量和局部静态变量。未初始化的全局变量和局部静态变量的默认值是0

如果初始化值是0的变量也放在了.bss,不占磁盘空间

全局未初始化变量只是预留一个未定义的全局变量符号，等最终链接成可执行文件的时候才放在.bss


.init 程序入口, 在main函数之前Glibc的初始化部分安排来执行这个段的代码

.fini main()返回之后的代码,一个程序的main函数正常退出时，Glibc会安排执行这个段代码

.plt `Procedure Linkage Table`的缩写,用来建立和共享库的动态连接

其他:
`.ctor` `.dotr` 特定函数的指针

`.rodata` 只读数据read-only data,比如print的常量字符串，可以放在ROM里

`.comment` 注释信息, 存放了编译器的信息

`.note` `.GNU-stack` 堆栈提示

`.debug` 调试信息

`.dynamic` 动态链接信息

`.hash` 符号哈希表 symbol hash table,新版本的glibc里是`.gnu.hash`

`.line` 调试行号

`.note` 额外编译器信息

`.strtab` 字符串,记录了symtab里面符号的名称

`.symtab` 符号表

`.shstrtab` 段名表

`.got` 动态链接的跳转表和全局入口表 Global offset table





## 4 ELF文件加载过程
这里主要说明动态链接的可执行文件的加载

当用户空间的进程调用系统调用execve()时,进程进入内核态,内核使用相应的程序处理中断

1 sys_execve
2 do_execve (do_execveat_common exec_binprm) fs/exec.c
3 search_binary_handler
4 load_elf_binary (fs/binfmt_elf.c)

5 如果文件是动态连接的,编译器通常创建一个内部的解释器(ELF 结构内的.interp),这个解释器通常是Glibc runtime linker :ld.so

load_elf_binary calls  load_elf_interp  to load interpreter

6 load_elf_binary calls start_thread (arch/x86/kernel/process_64.c)

When a userspace process calls the execve() syscall, the kernel takes control
(int $0x80), the handling code for this interruption is in
/usr/src/linux/arch/i386/kernel/entry.S for i386 architectures .

You can find a big switch statement, providing a way to launch the desired
function giving the %eax value (i.e. the syscall number) . In our case, the
function is sys_execve(), which calls do_execve() .



```
int do_execve(struct filename *filename,
	const char __user *const __user *__argv,
	const char __user *const __user *__envp)
{
	struct user_arg_ptr argv = { .ptr.native = __argv };
	struct user_arg_ptr envp = { .ptr.native = __envp };
	return do_execveat_common(AT_FDCWD, filename, argv, envp, 0);
}
```
do_execveat_common
```
static int do_execveat_common(int fd, struct filename *filename,
			      struct user_arg_ptr argv,
			      struct user_arg_ptr envp,
			      int flags)
{
	char *pathbuf = NULL;
	struct linux_binprm *bprm;
	struct file *file;
	struct files_struct *displaced;
	int retval;

	if (IS_ERR(filename))
		return PTR_ERR(filename);

	/*
	 * We move the actual failure in case of RLIMIT_NPROC excess from
	 * set*uid() to execve() because too many poorly written programs
	 * don't check setuid() return code.  Here we additionally recheck
	 * whether NPROC limit is still exceeded.
	 */
	if ((current->flags & PF_NPROC_EXCEEDED) &&
	    atomic_read(&current_user()->processes) > rlimit(RLIMIT_NPROC)) {
		retval = -EAGAIN;
		goto out_ret;
	}

	/* We're below the limit (still or again), so we don't want to make
	 * further execve() calls fail. */
	current->flags &= ~PF_NPROC_EXCEEDED;

	retval = unshare_files(&displaced);
	if (retval)
		goto out_ret;

	retval = -ENOMEM;
	bprm = kzalloc(sizeof(*bprm), GFP_KERNEL);
	if (!bprm)
		goto out_files;

	retval = prepare_bprm_creds(bprm);
	if (retval)
		goto out_free;

	check_unsafe_exec(bprm);
	current->in_execve = 1;

	file = do_open_execat(fd, filename, flags);
	retval = PTR_ERR(file);
	if (IS_ERR(file))
		goto out_unmark;

	sched_exec();

	bprm->file = file;
	if (fd == AT_FDCWD || filename->name[0] == '/') {
		bprm->filename = filename->name;
	} else {
		if (filename->name[0] == '\0')
			pathbuf = kasprintf(GFP_TEMPORARY, "/dev/fd/%d", fd);
		else
			pathbuf = kasprintf(GFP_TEMPORARY, "/dev/fd/%d/%s",
					    fd, filename->name);
		if (!pathbuf) {
			retval = -ENOMEM;
			goto out_unmark;
		}
		/*
		 * Record that a name derived from an O_CLOEXEC fd will be
		 * inaccessible after exec. Relies on having exclusive access to
		 * current->files (due to unshare_files above).
		 */
		if (close_on_exec(fd, rcu_dereference_raw(current->files->fdt)))
			bprm->interp_flags |= BINPRM_FLAGS_PATH_INACCESSIBLE;
		bprm->filename = pathbuf;
	}
	bprm->interp = bprm->filename;

	retval = bprm_mm_init(bprm);
	if (retval)
		goto out_unmark;

	bprm->argc = count(argv, MAX_ARG_STRINGS);
	if ((retval = bprm->argc) < 0)
		goto out;

	bprm->envc = count(envp, MAX_ARG_STRINGS);
	if ((retval = bprm->envc) < 0)
		goto out;

	retval = prepare_binprm(bprm);
	if (retval < 0)
		goto out;

	retval = copy_strings_kernel(1, &bprm->filename, bprm);
	if (retval < 0)
		goto out;

	bprm->exec = bprm->p;
	retval = copy_strings(bprm->envc, envp, bprm);
	if (retval < 0)
		goto out;

	retval = copy_strings(bprm->argc, argv, bprm);
	if (retval < 0)
		goto out;

	retval = exec_binprm(bprm);
	if (retval < 0)
		goto out;

	/* execve succeeded */
	current->fs->in_exec = 0;
	current->in_execve = 0;
	acct_update_integrals(current);
	task_numa_free(current);
	free_bprm(bprm);
	kfree(pathbuf);
	putname(filename);
	if (displaced)
		put_files_struct(displaced);
	return retval;

out:
	if (bprm->mm) {
		acct_arg_size(bprm, 0);
		mmput(bprm->mm);
	}

out_unmark:
	current->fs->in_exec = 0;
	current->in_execve = 0;

out_free:
	free_bprm(bprm);
	kfree(pathbuf);

out_files:
	if (displaced)
		reset_files_struct(displaced);
out_ret:
	putname(filename);
	return retval;
}

int do_execve(struct filename *filename,
	const char __user *const __user *__argv,
	const char __user *const __user *__envp)
{
	struct user_arg_ptr argv = { .ptr.native = __argv };
	struct user_arg_ptr envp = { .ptr.native = __envp };
	return do_execveat_common(AT_FDCWD, filename, argv, envp, 0);
}

int do_execveat(int fd, struct filename *filename,
		const char __user *const __user *__argv,
		const char __user *const __user *__envp,
		int flags)
{
	struct user_arg_ptr argv = { .ptr.native = __argv };
	struct user_arg_ptr envp = { .ptr.native = __envp };

	return do_execveat_common(fd, filename, argv, envp, flags);
}

```

	sys_execve() in fs/exec.c

		0) open_exec()

			File opening .

		1) prepare_binprm()

			Capabilities retreiving .

		3) copy_strings()

			Environnement and arguments retreiving from userspace
			to kernelspace . The argv[] strings are recopied .

		4) search_binary_handler()

			Executable type retreiving .



[load_elf_binary](https://github.com/torvalds/linux/blob/master/include/linux/binfmts.h#L667) 函数
```
static int load_elf_binary(struct linux_binprm *bprm){
    /* Get the exec-header */
	loc->elf_ex = *((struct elfhdr *)bprm->buf);
...
}
```
先获是获取了`elf 头部`


[linux_binprm](https://github.com/torvalds/linux/blob/master/include/linux/binfmts.h#L9)的结构
```c
#define CORENAME_MAX_SIZE 128

/*
 * This structure is used to hold the arguments that are used when loading binaries.
 */
struct linux_binprm {
	char buf[BINPRM_BUF_SIZE]; /* 前128字节是elf header*/
...
};

```




有2个LOAD
* 起始地址0x400000,长度0x06d4,计算得结束地址0x4006d4
* 起始地址0x6006d8,长度0x01ec,结束地址0x6008c4

加载了2段地址的内容到用户空间

load_elf_binary 载入`elf头部`后,做一些字段检查,通过`e_ident`检查magic number,`e_type`标识行文件还是共享库

然后通过`e_phoff`的偏移量加载`header table`,开始解析`header table`前,还需要查看ELF文件中是否指明了具体的解析器，如果是的话还需要载入解析器程序.

然后遍历`segment header table`的每个segment,只处理那些可装载的segment


可以通过readelf 命令来查看可执行文件的各个segment，例如
```
readelf -S execfile
There are 30 section headers, starting at offset 0x9f0:

Section Headers:
[Nr] Name              Type             Address           Offset   Size              EntSize          Flags  Link  Info  Align
[ 0]                   NULL             0000000000000000  00000000 0000000000000000  0000000000000000           0     0     0
...
[11] .init             PROGBITS         0000000000400390  00000390 0000000000000018  0000000000000000  AX       0     0     4
[12] .plt              PROGBITS         00000000004003a8  000003a8 0000000000000030  0000000000000010  AX       0     0     4
[13] .text             PROGBITS         00000000004003e0  000003e0 0000000000000228  0000000000000000  AX       0     0     16
[14] .fini             PROGBITS         0000000000400608  00000608 000000000000000e  0000000000000000  AX       0     0     4
...
[17] .eh_frame         PROGBITS         0000000000400658  00000658 000000000000007c  0000000000000000   A       0     0     8
[18] .ctors            PROGBITS         00000000006006d8  000006d8 0000000000000010  0000000000000000  WA       0     0     8
...
[24] .data             PROGBITS         00000000006008c0  000008c0 0000000000000004  0000000000000000  WA       0     0     4
[25] .bss              NOBITS           00000000006008c8  000008c4 0000000000000010  0000000000000000  WA       0     0     8
...
[29] .strtab           STRTAB           0000000000000000  00001770 00000000000001ef  0000000000000000           0     0     1
Key to Flags:
  W (write), A (alloc), X (execute), M (merge), S (strings)
  I (info), L (link order), G (group), x (unknown)
  O (extra OS processing required) o (OS specific), p (processor specific)
```
可以发现segment `eh_frame`的结束地址是`0x6006d4`,说明第一个LOAD 加载了0-17 segments

而`ctors`起始地址0x6006d8,`data`结束地址是0x6008c4.第二个LOAD 加载了18-25 segment

加载了诸如.text"代码段"



load_elf_binary会读取每个segment的p_vaddr字段,(在进程空间中的地址),通过[elf_map](https://github.com/torvalds/linux/blob/master/include/linux/binfmts.h#L931)函数,把文件中地址映射到了进程空间中:
```
error = elf_map(bprm->file, load_bias   vaddr, elf_ppnt,
                             elf_prot, elf_flags, 0);
```
注意这里的load_bias,偏移量将被加到所有segment 地址上,用来满足segment的位置随机化的需求.这个功能可以通过内核参数关闭.

最后计算每个区的位置，例如

* elf_bss变量记录的是BSS区的开始位置
* elf_brk变量记录的是堆(heap)的上边界

最后，为所有计算出的区起止位置加上随机化偏移量，进程空间中各区域起止位置的计算到此完成。


## 其他
在main 之前

_start 函数(sysdeps/x86_64/start.S),在编译期间,这段代码被编译成`/usr/lib64/crt1.o`,并且链接到用户二进制文件,总是放在`.text` 开始的地方.

所以入口地址`Entry point address`总是_start函数,这样变保证了它在任何代码前被执行.


```
__libc_start_main does quite a lot of work in addition to kicking off __libc_csu_init:
Set up argv and envp
Initialize the thread local storage by calling __pthread_initialize_minimal (which only calls __libc_setup_tls).
__libc_setup_tls will initialize Thread Control Block and Dynamic Thread Vector.

Set up the thread stack guard
Register the destructor (i.e. the rtld_fini argument passed to __libc_start_main) of the dynamic linker (by calling __cxa_atexit) if there is any
Initialize Glibc inself by calling __libc_init_first
Register __libc_csu_fini (i.e. the fini argument passed to __libc_start_main) using __cxa_atexit
Call __libc_csu_init (i.e. the init argument passed to __libc_start_main)
Call function pointers in .preinit_array section
Execute the code in .init section, which is usually _init function. What _init function does is compiler-specific. For GCC, _init executes user functions marked as __attribute__ ((constructor)) (in __do_global_dtors_aux)
Call function pointers in .init_array section
Set up data structures needed for thread unwinding/cancellation
Call main of user's program.
Call exit
```

参考

[Executable and Linkable Format (ELF)](https://www.cs.stevens.edu/~jschauma/631/elf.html)

[how-to-read-an-executable](http://jvns.ca/blog/2014/09/06/how-to-read-an-executable/)

[Understanding Linux ELF RTLD internals](http://s.eresi-project.org/inc/articles/elf-rtld.txt)

http://www.bottomupcs.com/elf.xhtml

[漫谈兼容内核之八: ELF映像的装入(一)](http://www.longene.org/techdoc/0328130001224576708.html)

