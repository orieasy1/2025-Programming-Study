package Ternary;

public class TSTree {
	Node root = new Node(' ');
	public Node insert(String word)    {
		return insert(root, word);
	}
	private Node insert(Node node, String word)    {		
        if (node == null) { 
            node = new Node(word.charAt(0)); 
        } 
        if (word.charAt(0) < node.data) { 
            node.left = insert(node.left, word); 
        } 
        else if (word.charAt(0) > node.data) { 
            node.right = insert(node.right, word); 
        } 
        else { 
            if (word.length() > 1) { 
                node.eq 
                    = insert(node.eq, word.substring(1)); 
            } 
            else { 
                node.isEndOfString = true; 
            } 
        } 
        return node; 
    } 
	
	
  
    private void traverseTSTUtil(Node node, char[] buffer, int depth) 
    { 
        if (node != null) { 
            traverseTSTUtil(node.left, buffer, depth); 
            buffer[depth] = node.data; 
            if (node.isEndOfString) { 
                System.out.println( 
                    new String(buffer, 0, depth + 1)); 
            } 
            traverseTSTUtil(node.eq, buffer, depth + 1); 
            traverseTSTUtil(node.right, buffer, depth); 
        } 
    }   
    public void traverseTST() 
    { 
        char[] buffer = new char[50]; 
        traverseTSTUtil( root, buffer, 0); 
    }      
}
