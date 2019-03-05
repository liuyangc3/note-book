Medians 中位数

数组是有序的, 若数组长度是奇数,中间的那个数, 若数组长度是偶数, 中间的两个数的平均值

4. Median of Two Sorted Arrays


#　295. Find Median from Data Stream

A algorithm that can guarantee output of i-elements after processing i-th element, is said to be `online algorithm`.
```java
class MedianFinder {
    private ArrayList<Integer> list = new ArrayList<>();
    
    public void addNum(int num) {
        list.add(num);
        Collections.sort(list);
    }
    
    public double findMedian() {
        int size = list.size();
        if(size % 2 == 0) {
            int a = list.get(size / 2);
            int b = list.get(size / 2 - 1);
            return (double) (a+b) / 2; 
        } else {
            return (double) list.get(size / 2);
        }
    }
}
```

中位数 左边用大顶堆, 右边用小顶堆, 如果两个堆size和是偶数, 中位数就是两个堆顶和除以2,
若size和是奇数,我们从左边取, 奇数都放到大顶堆.

```java
class MedianFinder {
    private  Queue<Integer> max = new PriorityQueue<>((a, b) -> b - a);
    private  Queue<Integer> min = new PriorityQueue<>();
    
    public void addNum(int num) {
        max.add(num);
        min.add(max.poll());
        if(min.size() > max.size()) {
            max.add(min.poll());
        }    
    }
    
    public double findMedian() {
        if(max.size() == min.size()) {
            return (double) (max.peek() + min.peek()) / 2; 
        } else {
            return (double) max.peek();
        }
    }
}
```
