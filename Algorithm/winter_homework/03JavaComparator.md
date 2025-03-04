# Java Comparator

## 문제

**정렬 기준**

* 점수(score)를 기준으로 내림차순 정렬 (높은 점수가 먼저 나오도록)
* 점수가 같은 경우에는 이름(name)을 기준으로 알파벳 순서로 오름차순 정렬

<br>

**구현사항**

* Checker라는 클래스를 생성합니다.
* Checker 클래스는 Comparator<Player> 인터페이스를 구현해야 합니다.
compare(Player a, Player b) 메서드를 오버라이드하여 두 플레이어를 위의 정렬 기준에 따라 비교하도록 구현합니다.

<br>

## 답

```java
import java.util.*;

// Player 클래스: 이름(name)과 점수(score) 필드를 가짐
class Player {
    String name;
    int score;

    Player(String name, int score) {
        this.name = name;
        this.score = score;
    }
}

// Checker 클래스: Comparator<Player> 구현
class Checker implements Comparator<Player> {
    @Override
    public int compare(Player a, Player b) {
        // 1. 점수(score)를 기준으로 내림차순 정렬
        if (a.score != b.score) {
            return b.score - a.score;  // 높은 점수가 먼저 나오도록
        } else {
            // 2. 점수가 같으면 이름(name)을 알파벳순으로 오름차순 정렬
            return a.name.compareTo(b.name);
        }
    }
}

// Solution 클래스: 메인 메서드 포함
public class Solution {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();  // 플레이어 수 입력
        Player[] players = new Player[n];

        // 플레이어 정보 입력 받기
        for (int i = 0; i < n; i++) {
            String name = scanner.next();
            int score = scanner.nextInt();
            players[i] = new Player(name, score);
        }
        scanner.close();

        // Checker 객체를 사용하여 정렬
        Arrays.sort(players, new Checker());

        // 정렬된 결과 출력
        for (Player player : players) {
            System.out.println(player.name + " " + player.score);
        }
    }
}
```