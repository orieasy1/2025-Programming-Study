# Insert a node at the head of a linked list

* 주어진 연결리스트의 head 앞에 새로운 노드를 삽입
* 새로운 노드의 next가 기존 head를 가리키도록 해야함
* 새로운 노드의 data값은 주어진 값으로 설정함
* 최종적으로 새로운 head를 반환해야 함
* 초기 head가 null일 수도 있으며 이 경우 새로운 노드가 첫번째 노드가 됨

<br>

매개 변수
- list: 기존 연결 리스트의 head 노드
- data: 새롭게 추가할 노드의 data 값

츨력
- 새로운 노드를 반환

### 입력 형식
1. 첫 번째 줄: 정수 n (삽입할 노드의 개수)
2. 다음 nrodml 줄: 삽입할 노드의 data값


```java
import java.io.*;
import java.math.*;
import java.security.*;
import java.text.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.regex.*;

public class Solution {

    //노드 구조정의
    static class SinglyLinkedListNode {
        public int data;
        public SinglyLinkedListNode next;

        public SinglyLinkedListNode(int nodeData) {
            this.data = nodeData;
            this.next = null;
        }
    }

    // 연결리스트 구조 정의
    static class SinglyLinkedList {
        public SinglyLinkedListNode head;
        public SinglyLinkedListNode tail;

        public SinglyLinkedList() {
            this.head = null;
            this.tail = null;
        }
      
    }

    //연결 리스트 출력
    public static void printSinglyLinkedList(SinglyLinkedListNode node, String sep, BufferedWriter bufferedWriter) throws IOException {
        while (node != null) {
            bufferedWriter.write(String.valueOf(node.data));

            node = node.next;

            if (node != null) {
                bufferedWriter.write(sep);
            }
        }
    }

    static SinglyLinkedListNode insertNodeAtHead(SinglyLinkedListNode llist, int data) {
        SinglyLinkedListNode newNode = new SinglyLinkedListNode(data);

        newNode.next = llist;

        return newNode;
    }

    private static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) throws IOException {
        BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter(System.getenv("OUTPUT_PATH")));

        SinglyLinkedList llist = new SinglyLinkedList();

        //노드 개수 입력 받기
        int llistCount = scanner.nextInt();
        //줄바꿈 문자를 제거하는 역할
        scanner.skip("(\r\n|[\n\r\u2028\u2029\u0085])?");

        for (int i = 0; i < llistCount; i++) {
            // 정수 입력 받기
            int llistItem = scanner.nextInt();
            scanner.skip("(\r\n|[\n\r\u2028\u2029\u0085])?");
        
            SinglyLinkedListNode llist_head = insertNodeAtHead(llist.head, llistItem);
            llist.head = llist_head;
        }



        printSinglyLinkedList(llist.head, "\n", bufferedWriter);
        bufferedWriter.newLine();

        bufferedWriter.close();

        scanner.close();
    }
}