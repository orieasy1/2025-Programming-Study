public class Node {
	char data; 
    boolean isEndOfString; 
    Node left, eq, right; 

    public Node(char data) 
    { 
        this.data = data; 
        this.isEndOfString = false; 
        this.left = null; 
        this.eq = null; 
        this.right = null; 
    } 
}
