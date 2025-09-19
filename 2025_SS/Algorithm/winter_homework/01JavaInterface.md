# Java Interface

## 문제

* MyCalculator 클래스는 AdvancedArithmetic 인터페이스를 구현해야함
* divisor_sum(int n) 메서드를 구현하여 입력된 정수 n의 모든 약수의 합을 반환해야함
* n의 값은 최대 1000까지 주어짐

<br>

## 답

```java
interface AdvancedArithmetic {
    int divisor_sum(int n);
}

// 답 부분
class MyCalculator implements AdvancedArithmetic {

    public int divisor_sum(int n) {
        int sum = 0;
        for (int i = 1; i <= n; i++) {
            if (n % i == 0) {
                sum += i;
            }
        }
        return sum;
    }
}

// 테스트용 Main 클래스
public class Solution {
    public static void main(String[] args) {
        MyCalculator myCalculator = new MyCalculator();
        int n = 6; 

        System.out.println("I implemented: AdvancedArithmetic");
        System.out.println(myCalculator.divisor_sum(n)); 
    }
}
```