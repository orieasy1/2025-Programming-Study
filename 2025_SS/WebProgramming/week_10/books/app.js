// 모듈 불러오기
const express = require('express'); // 웹 서버 구축용 프레임워크
const bodyParser = require('body-parser'); //JSON 요청 본문을 req.body로 파싱
const cors = require('cors'); // 브라우저의 CORS 정책 우회 허용
// 커스텀 파일 유틸리티 모듈에서 함수들 불러옴, files.js에서 정의되어 있어야함
const {readFile, readJSON, writeJSON} =require('./files');


const app = express();

app.use(cors()); //다른 origin에서의 요청을 허용
app.use(bodyParser.json());// client가 보낸 JSON을 req.body로 읽을 수 있도록 함
app.use(express.static('public')); // public 폴더의 정적 파일을 제공

const PORT = 8000;

//in-memory book storage
const books = [{
  "id":1,
  "title":"Lord of The Rings",
  "author":"JRR Tolkien"
}];

// 모든 책을 조회하는 api 엔드포인트
app.get('/api/books', function (req, res) {
  console.log("Endpoint /api/books received a GET request.");
  //res.type("text").send("Books app");
  res.json(books);
});

// 책 추가하는 api 엔드포인트
app.post('/api/books', (req, res) => {
  // 클라이언트가 보낸 요청 본문에서 title과 author를 추출
  // 이 코드가 동작하려면 반드시 app.use(bodyParser.json()) 또는 app.use(express.json())가 있어야 함
  const { title, author } = req.body;

  // title과 author 중 하나라도 없으면 400 에러 응답
  if (!title || !author) {
    console.log("Error 400. Title and author required");
    return res.status(400).json({ error: 'Title and author required' });
  }

  // tofhdns cor rorcp todtjd
  const newBook = { id: books.length + 1, title, author };
  // books 배열에 새 책 객체를 추가
  books.push(newBook); 
  console.log("Code 201. Book created successful");
  // 201로 HTTP 응답 상태 코드를 설정하고 새 책 객체를 JSON 형식으로 반환
  res.status(201).json(newBook); // HTTP 201 Created successful response status code
});

// 설정한 PORT에서 서버를 시작
// 서버가 시작되면 콘솔에 메시지를 출력
app.listen(PORT, () => {
    console.log(`Books app listening on port ${PORT}`);
});