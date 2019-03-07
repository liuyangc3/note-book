# pre order
mid , lelf child, right child
```
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
