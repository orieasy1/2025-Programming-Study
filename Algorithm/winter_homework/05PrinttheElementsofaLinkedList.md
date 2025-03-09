# Print the Elements of a Linked List

## 문제
단일 연결 리스트를 순회하면서 각 노드의 data값을 출력하는 문제

### 요구 사항
* 연결리스트의 head 노드가 주어지며 각 노드의 data값을 한 줄씩 출력
* 연결리스트가 비어있다면 head == null 아무것도 출력하지 않는다.
* 입력을 직접 읽지 말고 주어진 함수 printLinkedList내에서만 동작해야함

### 입력 형식
1. 첫번째 줄에 정수 n이 주어짐 -> 연결리스트의 노드 개수
2. 다음 n개의 줄의 각 노드의 data값이 주어짐

```java
import java.io.*;
import java.math.*;
import java.security.*;
import java.text.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.regex.*;

public class Solution {

    static class SinglyLinkedListNode {
        public int data;
        public SinglyLinkedListNode next;

        public SinglyLinkedListNode(int nodeData) {
            this.data = nodeData;
            this.next = null;
        }
    }

    static class SinglyLinkedList {
        public SinglyLinkedListNode head;
        public SinglyLinkedListNode tail;

        public SinglyLinkedList() {
            this.head = null;
            this.tail = null;
        }

        public void insertNode(int nodeData) {
            SinglyLinkedListNode node = new SinglyLinkedListNode(nodeData);

            if (this.head == null) {
                this.head = node;
            } else {
                this.tail.next = node;
            }

            this.tail = node;
        }
    }

    // 내가 채워야하는 답
    static void printLinkedList(SinglyLinkedListNode head) {
        SinglyLinkedListNode current = head;

        while(current != null) {
            System.out.println(current.data);
            current = current.next;
        }
    }

    private static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        SinglyLinkedList llist = new SinglyLinkedList();

        int llistCount = scanner.nextInt();
        scanner.skip("(\r\n|[\n\r\u2028\u2029\u0085])?");

        for (int i = 0; i < llistCount; i++) {
            int llistItem = scanner.nextInt();
            scanner.skip("(\r\n|[\n\r\u2028\u2029\u0085])?");

            llist.insertNode(llistItem);
        }

        printLinkedList(llist.head);

        scanner.close();
    }
}
    