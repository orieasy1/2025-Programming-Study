public class Itm {

    public boolean searchTST(TSTree tree, String word) {
        return search(tree.root, word);
    }

    private boolean search(Node node, String word) {
        if (node == null || word == null || word.length() == 0) {
            return false;
        }

        if (word.charAt(0) < node.data) {
            return search(node.left, word);
        } else if (word.charAt(0) > node.data) {
            return search(node.right, word);
        } else {
            if (word.length() == 1) {
                return node.isEndOfString;
            }
            return search(node.eq, word.substring(1));
        }
    }
}
