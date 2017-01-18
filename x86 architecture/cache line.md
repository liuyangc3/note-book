#

# Memory Type 
Memory Types and Their Properties

Memory Type and Mnemonic |Cacheable|Writeback Cacheable|Allows Speculative Reads|Memory Ordering Model
-------------------------|-----------------------------|------------------------|----------------------
Strong Uncacheable(UC)| No | No | No | Strong Ordering
Uncacheable (UC-) | No | No | No | Strong Ordering. Can only be selected through the PAT. Can be overridden by WC in MTRRs.
 
 
 
# Write Combining
Intel® 64 and IA-32 Architectures Software Developer Manual: Vol 3
