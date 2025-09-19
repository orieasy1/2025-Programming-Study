```java
public static SinglyLinkedListNode deleteNode(SinglyLinkedListNode llist, int position) {
    // 리스트가 비어있다면 그대로 반환
    if (llist == null) {
        return null;
    }

    // 첫 번째 노드를 삭제해야 하는 경우
    if (position == 0) {
        return llist.next;
    }

    // 현재 노드를 리스트의 head로 설정
    SinglyLinkedListNode current = llist;
    int index = 0;

    // 삭제할 노드의 이전 노드까지 이동
    while (current != null && index < position - 1) {
        current = current.next;
        index++;
    }

    // 유효한 위치인지 확인 후 삭제 수행
    if (current != null && current.next != null) {
        current.next = current.next.next;
    }

    return llist; // 기존 head 반환
}
```