허프만 코딩은 그리디 알고리즘 기반의 압축 기법

문자마다 다른 길이의 비트코드를 부여하여 압축 효율을 높임

입력 파일 문자 빈도수를 가지고 최소힙을 이용하여 파일을 압축하는 과정


### 고정 길이 코드 (fixed length code) vs 접두어 코드(prefix code)

대표적인 고정 길이 코드로 아스키 코드가 있다: 항상 8비트를 가질 수 있음.

저장 공간 활용에 있어 제한이 있다는 문제점을 해결하기 위해 가변 길이 코드가 존재한다.

가변 길이 코드 중 prefix code는 앞서 나온 문자가 다음 나올 문자의 접두어가 안되는 특징을 가진 코드다.

a: 01

b: 101

c: 010

이 경우 a의 코드인  01이 c의 코드 010의 접두어이기 때문에 prefix code가 아니다.

a: 01

b: 101

c: 010

반대로 위 경우에서는 어느 코드도 다른 코드의 prefix(접두어)가 아니므로 안전하게 압축 & 해독이 가능하다.

저장 공간은 절약하는 것이 목적

### 원리

허프만 트리를 만들어서 압축을 하기 위해서는 다음과 같은 원리로 수행된다.

1. 압축할 파일을 스캔하여 각 문자의 빈도 수를 게산
   <img width="385" alt="1" src="https://github.com/user-attachments/assets/70f963d5-27cf-4fb9-b7aa-b12bbdafedd6" />

    
2. 빈도 수를 우선순위로 최소 힙을 구성한다.
    <img width="592" alt="2" src="https://github.com/user-attachments/assets/d7ab2f5a-d4d6-432f-981a-1885227c3b90" />

3. 빈도 수가 가장 작은 두노드를 삭제한다.
4. 삭제한 두노드 중에 작은 것을 왼쪽 자식 노드, 큰 것을 오른 쪽 자식 노드로 하는 노드를 삽입
   <img width="692" alt="3" src="https://github.com/user-attachments/assets/12b4eaf6-967a-4b20-ba53-a1d53912cb02" />

6. 노드가 하나 남을 때까지 반복
   <img width="695" alt="4" src="https://github.com/user-attachments/assets/f8c15726-4921-48b9-b3a7-faf6316df379" />
   <img width="557" alt="5" src="https://github.com/user-attachments/assets/fa4803a8-fc7b-4edd-81fa-b0810176b4dd" />
   <img width="696" alt="6" src="https://github.com/user-attachments/assets/a9306aa4-903c-461e-b6ff-0737e8f9fe1b" />
   <img width="812" alt="7" src="https://github.com/user-attachments/assets/55e05bd2-e0a4-472d-b936-e596001be49c" />

7. 마지막 노드가 루트 노드가 됨
   <img width="463" alt="8" src="https://github.com/user-attachments/assets/54e49c06-f5c1-437c-adb8-e639705f75c9" />

    

### 코드로 구현

**HuffmanNode: 허프만 트리의 노드 클래스**

```java
public class HuffamanNode implements Comarable<HuffmanNode> {
	char ch;
	int frequency;
	HuffmanNode left;
	HuffmanNode right;
	
	public HuffmanNode(char ch, int frequency) {
		 this.ch = ch;
		 this.frequency = frequency;
	}
	
	@Override
	public int compareTo(HuffmanNode other) {
		return this.frequency - other.frequency;
	}
	
	public boolean isLeaf() {
		return(this.left == null && this.right == null);
	}
}
```

**HuffmanCoding: 전체 허프만 알고리즘 로직 (트리 생성 + 코드 생성 등)**

```java
import java.util.*;

public class HuffmanCoding {
		// 문자의 빈도 수를 계산해 매핑
    private Map<Character, String> huffmanCodes = new HashMap<>();
		
		//허프만 트리 생성, 루트 노드 반환
    public HuffmanNode buildTree(Map<Character, Integer> freqMap) {
        // 최소 힙 역할을 하는 우선 순위 큐 생성
				// 빈도수가 작은 HuffmanNode가 먼저 나옴
        PriorityQueue<HuffmanNode> pq = new PriorityQueue<>();
				
				// 각 문자와 빈도를 기반으로 리프 노드를 만들어 힙에 삽입
        for (Map.Entry<Character, Integer> entry : freqMap.entrySet()) {
            pq.add(new HuffmanNode(entry.getKey(), entry.getValue()));
        }
				
				// 트리노드가 하나만 남을 때 까지 반복
        while (pq.size() > 1) {
		        //빈도수가 가장 낮은 두 노드를 꺼냄
            HuffmanNode left = pq.poll();
            HuffmanNode right = pq.poll();
						
						// 두 노드를 합쳐서 새로운 내부 노드를 생성
						// 문자값은 내부 노드이므로 \0' (null character)
            HuffmanNode merged = new HuffmanNode('\0', left.freq + right.freq);
            merged.left = left;
            merged.right = right;
						
						// 병합된 노드를 다시 큐에 추가
            pq.add(merged);
        }
				
				// 마지막 하나 남은 노드가 루트 노드
        return pq.poll();
    }
		
		// 허프만 트리를 순회하면서 각 문자에 대한 이진 코드를 생성하는 메서드
    public void generateCodes(HuffmanNode root, String code) {
        if (root == null) return;
				
				// 리프노드라면 콤드 매핑 저장
        if (root.isLeaf()) {
            huffmanCodes.put(root.ch, code);
            return;
        }
				
				// 왼쪽으로 가면 코드에 0코드 추가
        generateCodes(root.left, code + "0");
        // 오른족으로 가면 코드에 1추가
        generateCodes(root.right, code + "1");
    }
		
		// 코드 맵 반환
    public Map<Character, String> getCodes() {
        return huffmanCodes;
    }

		//입력 문자열을 허프만 코드로 인코딩하는 메서드
    public String encode(String text) {
        StringBuilder encoded = new StringBuilder();
        for (char ch : text.toCharArray()) {
		        // 각 문자를 대응되는 허프만 코드로 변환하여 이어 붙임
            encoded.append(huffmanCodes.get(ch));
        }
        return encoded.toString();
    }
		// 현재까지 생성된 허프만 코드를 콘솔에 출력하는 메서드
    public void printCodes() {
        for (Map.Entry<Character, String> entry : huffmanCodes.entrySet()) {
            System.out.println(entry.getKey() + ": " + entry.getValue());
        }
    }
}

```

main: 실행 테스트 용

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        String text = "ABRACADABRA";

        // 1. 문자 빈도수 계산
        Map<Character, Integer> freqMap = new HashMap<>();
        for (char ch : text.toCharArray()) {
            freqMap.put(ch, freqMap.getOrDefault(ch, 0) + 1);
        }

        // 2. 허프만 트리 생성 및 코드 생성
        HuffmanCoding hc = new HuffmanCoding();
        HuffmanNode root = hc.buildTree(freqMap);
        hc.generateCodes(root, "");

        // 3. 결과 출력
        System.out.println("Huffman Codes:");
        hc.printCodes();

        // 4. 인코딩
        String encoded = hc.encode(text);
        System.out.println("\nOriginal Text: " + text);
        System.out.println("Encoded Text: " + encoded);
    }
}

```
