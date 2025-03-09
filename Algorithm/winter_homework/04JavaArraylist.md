# Java Arraylist

## 문제
* n개의 줄이 주어짐
* 각 줄에는 0개 이상의 정수가 포함됨
* q개의 질문에 대해 특정 위치의 숫자를 출력

<br>

### 입력 형식
* 첫 번재 줄에는 정수 n이 주어짐
* 다음 n개의 줄에서는 가 줄마다 정수 d가 주어지며 이는 해당 줄에 포함된 정수의 개수를 나타냄.
* 그 후 d개의 정수가 공백으로 그분 되어 주어짐

* 그 다음 줄에는 정수 q가 주어지며 이는 질문 개수를 의미
* 이후 q개의 줄에는 두 개의 정수 x와 y가 주어짐: x번째 줄의 y번째 숫자

### 제약 조건
* 1 <= n <= 20000
* 

### 출력 형식
각 질의에 대해 x번째 줄의 y번째 숫자를 출력
해당 위치에 숫자가 존재하지 않으면 ERROR! 를 출력

<br>

## 답

```java
public class Main {
    public static void main (String[] args) {
        Scanner scanner = new Scanner(System.in);

        // 줄 개수 입력 받기 n
        int n = scanner.nextInt();
        ArrayList<ArrayList<Integer>> data = new ArrayList<>();

        // n개의 줄 입력 받기: d 받은 후 숫자들 받기
        for (int i = 0; i < n; i++) {
            int d = scanner.nextInt();
            ArrayList<Integer> row = new ArrayList<>();
            for (int j = 0; j < d; j++) {
                row.add(scanner.nextInt());
            }
            data.add(row);
        }

        // 질문 개수 입력받기
        int q = scanner.nextInt();

        // 질문 처리 
        for (int i = 0; i < q; i++) {
            int x = scanner.nextint();
            int y = scanner.nextInt();

            // 유효한 인덱스 인지 확인 및 출력
            if(x >= 1 && x <= n && y >= data.get(x-1).size()) {
                System.out.println(data.get(x - 1).get(y - 1));
            }else {
                System.out.println("ERROR!");
            }
        }

        scanner.close();
    }
}