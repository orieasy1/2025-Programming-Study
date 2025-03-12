# Insert a node at a specific position in a linked list

## 문제
* 주어진 연결 리스트의 head 포인터와 정수 data, 그리고 position을 이요하여 새 노드를 삽입


```java
import java.io.*;
import java.util.*;

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

    public static void printSinglyLinkedList(SinglyLinkedListNode node, String sep, BufferedWriter bufferedWriter) throws IOException {
        while (node != null) {
            bufferedWriter.write(String.valueOf(node.data));
            node = node.next;

            if (node != null) {
                bufferedWriter.write(sep);
            }
        }
    }

    static class Result {
        /*
         * Function to insert a node at a specific position in a linked list.
         */
        public static SinglyLinkedListNode insertNodeAtPosition(SinglyLinkedListNode llist, int data, int position) {
            // 새 노드 생성
            SinglyLinkedListNode newNode = new SinglyLinkedListNode(data);

            // 리스트가 비어있거나, 맨 앞에 삽입하는 경우
            if (position == 0) {
                newNode.next = llist;
                return newNode;
            }

            // 현재 노드를 리스트의 head로 설정
            SinglyLinkedListNode current = llist;
            int index = 0;

            // 삽입할 위치 직전까지 이동
            while (current != null && index < position - 1) {
                current = current.next;
                index++;
            }

            // 유효한 위치라면 삽입 수행
            if (current != null) {
                newNode.next = current.next;
                current.next = newNode;
            }

            return llist; // 기존 head 반환
        }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(System.in));
        BufferedWriter bufferedWriter = new BufferedWriter(new OutputStreamWriter(System.out));

        SinglyLinkedList llist = new SinglyLinkedList();

        int llistCount = Integer.parseInt(bufferedReader.readLine().trim());

        for (int i = 0; i < llistCount; i++) {
            int llistItem = Integer.parseInt(bufferedReader.readLine().trim());
            llist.insertNode(llistItem);
        }

        int data = Integer.parseInt(bufferedReader.readLine().trim());
        int position = Integer.parseInt(bufferedReader.readLine().trim());

        // 새 노드를 삽입 후 head 업데이트
        llist.head = Result.insertNodeAtPosition(llist.head, data, position);

        // 결과 출력
        printSinglyLinkedList(llist.head, " ", bufferedWriter);
        bufferedWriter.newLine();

        bufferedReader.close();
        bufferedWriter.close();
    }
}
```