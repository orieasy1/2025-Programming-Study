# 1. 자바스크립트를 위한 기본 상식

### 정적인 웹을 개발하던 시대의 자바스크립트

웹사이트를 제작하는 언어, ‘복사해서 붙여 넣으면’ 원하는 효과를 만들 수 있는 언어, 배우기 쉬운 프로그래밍 언어

**정적인 웹:** 텍스트나 이미지를 사용해서 사용자에게 정보를 보여주기만 하는 웹

정적인 웹에서 자바스크립트는 간단한 애니메이션이나 동적인 효과를 보여주는 용도로 사용됨 → 인터넷에서 널려 있는 소스를 복붙하기만 되었음

**하지만 이제 모든 정보가 인터넷으로 옮겨왔음**

인터넷 초창기부터 사용해왔던 자바스크립트 언어야말로 모든 웹 브라우저에서 사용할 수 있음

∴ 웹이 계속 발달할수록 자바스크립트이 역할은 점점 커지고 자바스크리비트에 새로운 기능도 많이 추가되고 있음

<br>

### 자바스크립트는 자바와 다르다.

**자바스크립트의 역사**

- 인터넷 초창기, 웹 브라우저 시장을 석권하고 있던 Netscape에서 웹 문서를 좀더 표시하기 위해 LiveScript 개발
    - 개발의도: 새로운 기술을 통해 HTML로는 할 수 없는 기능 추가
- 1995년에 Java를 만든 Sun Microsystems가 LiveScript 개발권을 넘겨받아 이름을 JavaScript로 변경

자바스크립트는 웹 브라우저에서 실행된느 프로그램이지만, 자바는 자체적으로 실행할 수 있다는 점이 다르다.

추가적으로 ECMAScript는 자바스크립트를 기반으로 표준화된 스크립트 언어이다. 자바스크립트는 에크마스크립트의 표준 사양을 따르는 가장 유명한 언어이다.

<br><br>

# 2. 웹 개발에서 자바스크립트의 역할

### 클라이언트와 서버

웹사이트의 범위는 웹 브라우저에 보이는 내용뿐만 아니라 눈에 보이지 않는 부분까지도 모두 포함한다.

- 클라이언트: 사용자의 눈에 보이는 부분
- 서버: 눈에 보이지 않는 부분

사용자가 웹 브라우저에서 특정 정보를 보고자 하면 클라이언트 컴퓨터에서 서버 컴퓨터로 관련 정보를 요청 → 서버에서는 해당 정보를 찾아서 다시 클라이언트 컴퓨터로 전송

웹 브라우저 창에 주소를 입력하거나 링크를 클릭할 때마다 사이트가 동작하는 것은 서버 컴퓨터와 클라이언트 컴퓨터 간에 정보를 주고받으면서 그 결과를 사용자에게 보여주기 때문이다.

<br>

### 프런트엔드 개발과 자바스크립트

Frontend: 앞에 있어서 사용자에게 보이는 부분, 웹사이트나 애플리케이션에서 내용을 작성하고 화면을 디자인하는 것부터 사용자의 동작에 반응해서 결과를 만드는 역할

최근의 웹사이트는 사용자와 실시간으로 정보를 주고받으면서 애플리케이션처럼 동작 → 프런트엔드 개발의 중요성⬆️

<br>

### 백엔드 개발과 자바스크립트

Backend: 뒤에 있어서 사용자에게 보이지 않는 부분, 클라이언트가 요청을하면 서버에서는 요청을 처리하기 위한 프로그램을 실행하는데 이때, 서버에서 실행할 프로그램을 만드는것

<br>

### 콘솔 창에서 자바스크립트 사용하기

웹 브라우저에는 자바스크립트 소스를 실행할 수 있는 자바스크립트 엔진이 포함되어있어 웹 브라우저 창의 콘솔창을 통해 간단한 자바스크립트 소스를 실행할 수 있다.

<br><br>

# 4. 간단한 스크립트부터 시작하기

웹문서는 기본적으로 HTML로 내용을 작성하고 CSS로 레이아웃이나 디자인을 결정 + 자스크립트를 이용해 동적인 효과 추가

### 웹 문서에서 스크립트 소스 작성하기

자바스크립트 처리기는 웹브라우저에 포함되어있으므로 자바스크립트 소스는 웹문서에 삽입해야한다. 이때 <script> 태그를 사용하는데 웹문서에 직접 작성할 수도 잇고 자바스크립트 소스만 따로 파일로 저장한 후 서로 연결하여 사용할 수 도 있음 

<br>

**인라인 스크립트  inline script**

HTML 태그 안에 직접 작성하는 자바스크립트

팝업 창을 열고 닫거나, 알림 메세지를 표시할 때처럼 간단한 명령을 처리할 경우 인라인 스크립트를 자주 사용

ex) 버튼을 클릭했을 때 알림 창을 표시하는 예제

```html
 <button onclick = "alert('알림 메시지가 표시됩니다.')">클릭!</button>
```

<br>

**내부 스크립트 internal script**

웹 문서에서 &lt;script&gt;태그와 &lt;/script&gt; 태그를 사용해 자바스크립트 소스만 모아두는 스크립트

&lt;script&gt; 태그는 웹 문서의 모든 곳에 위치할 수 있고 삽입된 위치에서 바로 스크립트가 실행되는데 한 문서 안에 여러 개의 &lt;script&gt; 태그를 사용할 수 있다. 

문서에 있는 버튼을 클릭했을 때 실행하는 소스이거나 웹 문서 내용을 변경하는 소스라면 웹문서가 모두 로딩된 다음에 실행해야 한다. 즉 &lt;script&gt; 소스는 웹 요소를 모두 로딩한 후 삽입되어야 한다. 그래서 대부분의 경우 웹 문서 내용이 끝나는 &lt;/body&gt; 태그 직전에 자바스크립트 소스를 삽입한다. 


ex) 새로고침할 때마다 무작위로 배경색을 바꾸는 예제

```html
<body>
  <p>새로 고침해 보세요</p>
  
  <script>
    function random(number) {
      return Math.floor(Math.random() * number);
    }

    function bgChange() {
      const rndCol = 'rgb(' + random(255) + ',' + random(255) + ',' + random(255) + ')';
      document.body.style.backgroundColor = rndCol;
    }

      bgChange();
    </script>
</body>
</html>
```

여기서도 </body> 태그 앞에 스크립 소스를 작성한 것을 확인할 수 있다.

<br>

**인라인 스크립트와 내부 스크립트 소스의 단점**

장점: HTML 문서에 자바스크립트 소스를 함께 사용하면 웹 문서에서 자바스크립트 소스를 함께 확인할 수 있다.

단점

HTML 태그와 자바스크립트 소스가 뒤섞여 있으므로 웹 문서의 소스가 복잡해진다. 태그나 자바스크립트를 수정해야할 때 필요한 소스를 한 눈에 알아보기 어렵다.

같은 자바스크립트의 소스를 여러 웹 문서에서 사용해야할 경우, 필요한 문서마다 똑같은 소스코드를 반복해서 삽입해야한다. 수정 사항이 생겼다면 이 소스가 포함도니 모든 문서를 다 찾아다니면서 하나씩 모두수정해야한다.

**➡️ 외부 스크립트 파일로 저장하여 링크하는 방법 사용**

<br>

### 외부 스크립트 파일 링크하기

자바스크립트 소스를 다로 파일로 저장한 후 링크해서 사용하면 웹 문서에서는 직접 자바스크립트 소스가 드러나지 않아서 웹 문서 소스를 훨씬 깔끔하게 사용할 수 있음

수정 부분이 있을 때도 js 파일만 수정하여 링크한 모든 HTML 문서에 곧바로 적용할 수 있다.

외부 스크립트 파일을 작성할 때는 태그 없이 자바스크립스 소스만 작성하고 확장자가 .js인 파일로 저장한다.

그리고 HTML 문서에서 <script> 태그 src속성을 이용해 자바스크립트 파일을 링크할 수 있고 이렇게 링크한 자바스크립트 소스는 웹문서에 직접 작성한 자바스크립트 소스 처럼 사용할 수 있다.

외부스크립트 파일도 </body> 태그 앞에 추가해서 웹 문서 요소를 모두 가져온 후에 실행해야한다.

최근에는 <script> 태그 안에 defer라는 속성을 추가해서 무조건 문서를 가져온 후에 스크립트 소스를 실행하도록 지정하기도 한다.
defer 속성은 외부 스크립트 파일을 링크하는 경우에만 사용할 수 있다.

```html
<script src="스크립트 파일 경로"></script>
<script defer src="스크립트 파일 경로"></script>
```

ex)

```html
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>문서 안에 스크립트 작성</title>
  <link rel="stylesheet" href="css/main.css">
  <script defer src="js/changeBg.js"></script>
</head>
```

```jsx
function random(number) {
  return Math.floor(Math.random() * number);
}

function bgChange() {
  const rndCol = 'rgb(' + random(255) + ',' + random(255) + ',' + random(255) + ')';
  document.body.style.backgroundColor = rndCol;
}

bgChange();
```

<br>

### 웹 브라우저에서 스크립트를 해석하는 과정

```jsx
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>문서 안에 스크립트 작성하기</title>
  <link rel="stylesheet" href="css/main.css">
</head>
<body>
  <p>새로 고침해 보세요</p>
  
  <script src="js/changeBg.js"></script>
</body>
</html>
```

```jsx
function random(number) {
  return Math.floor(Math.random() * number);
}

function bgChange() {
  const rndCol = 'rgb(' + random(255) + ',' + random(255) + ',' + random(255) + ')';
  document.body.style.backgroundColor = rndCol;
}

bgChange();
```

1. <!DOCTYPE html> 소스를 보고 웹 브라우저는 현재 문서가 웹 문서라는 사실을 알게 됨 → <html> </html> 태그 사이의 내용을 HTML표준에 맞춰 해석
2. 웹 문서에서 HTML 태그 순서와 포함 관계 확인
3. 태그 분석이 끝나면 외부 스타일 시트나 문서 안의 스타일 정보를 분석하면서 화면에 표시
4. <script> 태그를 만나면 자바 스크립트 해걱기로 스크립트 소스를 넘김. 내부 스크립트면 태그 사이의 소스를 해석하고, 외부 파일이 연결되어있으면 외부 파일의 소스를 해석
5. 스크립트 파일이 실행되어 문서의 배경색이 바뀜
<img width="1006" alt="image" src="https://github.com/user-attachments/assets/a7ff1f40-995a-41d3-9ae4-fbbd35abaa84" />

![image](https://github.com/user-attachments/assets/f727a4b4-8abb-4a1c-90fa-9b2fac9476f6)
