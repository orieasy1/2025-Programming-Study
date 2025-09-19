# Tree: Preorder Traversal

## 문제
* 주어진 이진 트리의 루트 노드를 preOrder 함수에 전달합니다.
* 이 함수를 토리의 전위 순회(Preorder Traversal) 결과를 한줄로 출력해야함.
* 출력은 공백으로 구분된 값의 형태여야 한다.

입력 형식
* 입력값은 함수 호출을 통해 제공됨
* 주어진 이진트리 루트 root가 preOrder 함수 매개변수로 주어짐


제약 조건
* 이진 트리의 노드 개수: 1 <= Nodes <= 500
* 트리는 항상 1개 이상의 노드를 포함함


```java
class Node {
    Node left;
    Node right;
    int data;
    
    Node(int data) {
        this.data = data;
        left = null;
        right = null;
    }
}

class Solution {

    public static void preOrder(Node root) {
        if (root == null) {
            return;
        }

        System.out.print(root.data + " ");
        preOrder(root.left);
        preOrder(root.right);

    }

    public static Node insert(Node root, int data) {
        if(root == null) {
            return new Node(data);
        } else {
            Node cur;
            if(data <= root.data) {
                cur = insert(root.left, data);
                root.left = cur;
            } else {
                cur = insert(root.right, data);
                root.right = cur;
            }
            return root;
        }
    }

    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        int t = scan.nextInt();
        Node root = null;
        while(t-- > 0) {
            int data = scan.nextInt();
            root = insert(root, data);
        }
        scan.close();
        preOrder(root);
    }	
}

```
