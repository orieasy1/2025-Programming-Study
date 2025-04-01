// 허프만 트리ㄹ 구성하는 노드의 공ㅗ 속ㅇㅘ 동ㅏ
abstract class Node implements Comparable<Node> {
    public int frequency;
    public char data;
    public Node left, right;

    public Node(int freq) {
        frequency = freq;
    }

    public int compareTo(Node tree) {
        return frequency - tree.frequency;
    }
}
