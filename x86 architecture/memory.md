# SRAM DRAM

SRAM 採用正反器（flip-flop）構造儲存，DRAM 則是採用電容儲存



Banks

To reduce access latency, memory is split into multiple equal-sized units called banks.
 
 It’s a “bank” of chips that responds to a
single command and returns data


bank 里就是一个个存储单元 分为 row column，每个column 有一个row buffer 单元

typical DRAM bank sizes are 512 bytes, 1 kB or 2 kB.