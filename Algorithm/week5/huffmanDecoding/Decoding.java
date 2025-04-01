public class Decoding {
    void decode(String s, Node root) {
        Node current = root;
        for (int i = 0; i < s.length(); i++) {
            // 0이면 왼쪽으로 이동 아니면 오른쪽
            current = (s.charAt(i) == '0') ? current.left : current.right;

            // 리프 노드에 도달하면 문자 출력
            if (current.left == null && current.right == null) {
                System.out.print(current.data);
                current = root;
            }
        }
    }
}
