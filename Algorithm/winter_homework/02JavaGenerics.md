# Java Generics

## 문제

* printArray 메서드를 작성: 정수 배열(Integer[])과 문자열 배열(String[])을 처리할 수 있어야 합니다.
* 제네릭(Generic)을 사용해야 하며, 메서드 오버로딩(Overloading)은 사용할 수 없습니다.
* printArray 메서드는 배열의 모든 요소를 한 줄씩 출력해야 합니다.

<br>

## 답

```java
import java.lang.reflect.Method;

class Printer {
    // 답
    public <T> void printArray(T[] array) {
        for (T element : array) {
            System.out.println(element);
        }
    }
}

public class Solution {
    public static void main(String args[]) {
        Printer myPrinter = new Printer();
        Integer[] intArray = {1, 2, 3};     
        String[] stringArray = {"Hello", "World"};  

        myPrinter.printArray(intArray);   
        myPrinter.printArray(stringArray);  

        // 메서드 오버로딩 여부 검사
        int count = 0;
        for (Method method : Printer.class.getDeclaredMethods()) {
            String name = method.getName();
            if (name.equals("printArray")) {
                count++;
            }
        }
        if (count > 1) {
            System.out.println("Method overloading is not allowed!");
        }
    }
}

```