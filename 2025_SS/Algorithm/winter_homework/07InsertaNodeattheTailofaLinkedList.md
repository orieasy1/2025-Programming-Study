# Insert a Node at the Tail of a Linked List

## 문제
* 주어진 연결리스트의 head 포인터와 정수 값을 사용하여 새로운 노드를 추가해야 한다.
* 새로운 노드를 연결리스트 tail에 삽입해야 한다.
* 새로운 연결리스트의 head를 반환해야 한다.
* 초기 head가 null일 수도 있으며, 이 경우 새로운 노드가 첫 번째 노드가 된다.

매개 변수
* head: 연결리스트의 head
* data: 새롭게 추가할 노드 

출력
* 연결 리스트의 새로운 포인터를 반환

입력 형식
1. 첫 번째 줄: 정수 n (연결리스트의 노드 개수)
2. 다음 n개의 줄: 삽입할 노드의 data 값


```java
public class Solution {

    static class SinglyLinkedListNode {
        public int data;     //노드가 저장하는 정수 값
        public SinglyLinkedListNode next; //다음 노드를 가리키는 포인터

        // 초기값 설정
        public SinglyLinkedListNode(int nodeData) {
            this.data = nodeData;
            this.next = null;
        }
    }

    static class SinglyLinkedList {
        public SinglyLinkedListNode head;

        public SinglyLinkedList() {
            this.head = null;
        }
      
    }

    public static void printSinglyLinkedList(SinglyLinkedListNode node, String sep, BufferedWriter bufferedWriter) throws IOException {
        while (node != null) {
            bufferedWriter.write(String.valueOf(node.data));

            node = node.next;

            if (node != null) {
                bufferedWriter.write(sep);
            }
        }
    }

    static SinglyLinkedListNode insertNodeAtTail(SinglyLinkedListNode head, int data) {

        SinglyLinkedListNode newNode = new SinglyLinkedListNode(data);

        //리스트가 비어있는 경우, 새노드를 head로 반환
        if(head = null) {
            return newNode;
        }

        //마지막 노드를 찾기 위해 순회
        SinglyLinkedListNode current = head;
        while (current.next != null) {
            current = current.next;
        }

        //마지막 모드의 next를 새노드로 설정
        current.next = newNode;

        return head;
    }

    private static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) throws IOException {
        BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter(System.getenv("OUTPUT_PATH")));

        SinglyLinkedList llist = new SinglyLinkedList();

        int llistCount = scanner.nextInt();
        scanner.skip("(\r\n|[\n\r\u2028\u2029\u0085])?");

        for (int i = 0; i < llistCount; i++) {
          
            int llistItem = scanner.nextInt();
            scanner.skip("(\r\n|[\n\r\u2028\u2029\u0085])?");

          SinglyLinkedListNode llist_head = insertNodeAtTail(llist.head, llistItem);
          llist.head = llist_head;
          
        }



        printSinglyLinkedList(llist.head, "\n", bufferedWriter);
        bufferedWriter.newLine();

        bufferedWriter.close();

        scanner.close();
    }
}
```