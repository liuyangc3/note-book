step time server 和 adjust time server 区别

https://github.com/ntp-project/ntp/blob/1a399a03e674da08cfce2cdb847bfb65d65df237/ntpdate/ntpdate.h#L64
```
#define NTPDATE_THRESHOLD (FP_SECOND >> 1) /* 1/2 second */
```
https://github.com/ntp-project/ntp/blob/1a399a03e674da08cfce2cdb847bfb65d65df237/ntpdate/ntpdate.c#L1276
```
if (always_step) {
        dostep = 1;
    } else if (never_step) {
        dostep = 0;
    } else {
        absoffset = server->soffset;
        if (absoffset < 0)
            absoffset = -absoffset;
        dostep = (absoffset >= NTPDATE_THRESHOLD || absoffset < 0);
    }
 
 
    if (dostep) {
        if (simple_query || debug || l_step_systime(&server->offset)){
            msyslog(LOG_NOTICE, "step time server %s offset %s sec",
                stoa(&server->srcadr),
                lfptoa(&server->offset, 6));
        }
 
...
```


dostep = (absoffset >= NTPDATE_THRESHOLD || absoffset < 0) 这行说明，
dostep 是 当时间偏移量大于0.5秒 这时候会输出step time server %s offset %s sec 的日志。

所以偏移量小于5秒时 打印 adjust time server %s offset %s sec

man 手册也有提及， 超过0.5 秒调用  settimeofday() 否则 adjtime() 
