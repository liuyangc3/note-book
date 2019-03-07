# Pre Order Traverse 
mid , lelf child, right child
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode(int x) { val = x; }
 * }
 */
 
public preOrder(TreeNode root) {
    if(root == null) return;
    System.out.println(root.val);
    preOrder(root.left);
    preOrder(root.right);
}

/**
 * 得到一个node 后, 我们只能访问自己, 左和右三个方向
 * 因为访问顺序是中左右, 所以先打印自己
 * 子节点的入栈的顺序应该是右左
 */
 
public preOrder(TreeNode root) {
    if(root == null) return;
    
    Stack<TreeNode> stack = new Stack<>();
    stack.push(root);
    
    while(!stack.isEmpty()) {
        TreeNode node = stack.pop();
        System.out.println(root.val);
        if(node.right != null) stack.push(node.right);
        if(node.left != null) stack.push(node.left);
    }

}
```

# In Order Traverse 
left, mid, right

```java
public inOrder(TreeNode root) {
    if(root == null) return;
    inOrder(root.left);
    System.out.println(root.val);
    inOrder(root.right);
}
```

```  
      3
    /  \
  1     2 
   \   /  \
    7 4     5
 
打印循序是 1 7 3 4 2 5



  3
 / \
1  2
  /
1  
```

```
public inOrder(TreeNode root) {
    if(root == null) return;
    Stack<TreeNode> stack = new Stack<>();
    
    TreeNode node = root;
    while(node != null && !stack.isEmpty()) {
        // push most left to stack
        // until node is leaf node
        while(node != null) {
            stack.push(node);
            node = node.left;
        }
        node = stack.pop(); // pop this most left leaf node
        System.out.print(node.val); // visit this most left leaf node

        // if node has right child, in next loop
        // will get the most left leaf of this child
        node = node.right;
    }
}
```
