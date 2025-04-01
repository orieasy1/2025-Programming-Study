public class MainTST {
	public static void main(String[] args) {
		TSTree t = new TSTree();
		Itm itm = new Itm();
        t.insert("hello"); 
        t.insert("world"); 
        t.insert("her"); 
        t.insert("hero"); 
  
        System.out.println( 
            "Following is traversal of ternary search tree:"); 
        t.traverseTST(); 
  
        System.out.println( 
            "\nFollowing are search results"); 
        System.out.println("her: "+ (itm.searchTST(t, "her")? "Found": "Not Found")); 
        System.out.println("hell: "+ (itm.searchTST(t, "hell")? "Found": "Not Found")); 
	}
}
