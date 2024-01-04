document.addEventListener('DOMContentLoaded', function() {
  // 클래스명이 myClass인 모든 요소를 선택하고 이벤트 리스너 등록
  const elementsWithClass = document.querySelectorAll('.listing-item');
  const enterNameID = "enterName"
  
  // 핵심 : 이벤트 리스너 연결
  elementsWithClass.forEach(element => {
    element.addEventListener('click', function() {

      console.log('이벤트 작동');
      const enterNameText = this.querySelector('#enterName').textContent;
      const enterNameKorText = this.querySelector('#enterName_Kor').textContent;

      // var search_enterNameText = localStorage.getItem('enterName');
      // var search_enterNameKorText =  localStorage.getItem('enterNameKor');
      
      // 클릭된 요소의 "enterName" ID를 가진 하위 요소의 텍스트 가져오기
      // DB 저장된 기업명과 실제 기업명이 다른 경우가 있어 추가
      if (enterNameKorText == '한국전력'){
        enterNameKorText = '한전';
      }
      if (enterNameKorText == '삼성석유화학'){
        enterNameKorText = '삼성 화학';
      }

      // JS 내부 스토리지에, 텍스트 저장
      localStorage.setItem('enterName', enterNameText);
      localStorage.setItem('enterNameKor', enterNameKorText);
      // if (!search_enterNameKorText){

      //   }
      })
    });

    console.log("Enter : " + localStorage.getItem('enterName'));
    console.log("Enter Kor : " + localStorage.getItem('enterNameKor'));
});


document.addEventListener('DOMContentLoaded', function() {
  const displayTextElement = document.getElementById('detail_enterName');

  const DetailNewsElement_1 = document.getElementById('News_1');
  const DetailNewsElement_2 = document.getElementById('News_2');
  const DetailNewsElement_3 = document.getElementById('News_3');
  const DetailNewsElement_4 = document.getElementById('News_4');
  const DetailNewsElement_5 = document.getElementById('News_5');
  
  // 페이지 2가 로드될 때 로컬 스토리지에서 텍스트를 가져와서 화면에 표시
  const enterTextReceived = localStorage.getItem('enterName');
  
  if (enterTextReceived) {
    displayTextElement.textContent = `: ${enterTextReceived}`;
    // 로컬 스토리지의 데이터를 한 번 사용하고 나면 삭제 (선택사항)
    localStorage.removeItem('enterName');
  }

  
  // RESTful API로 GET 요청 보내기
  console.log('fetch 요청 전송 : Detail Information');
  // console.log(location.origin);
  const enterKorTextReceived = localStorage.getItem('enterNameKor');
  // localStorage.removeItem('enterNameKor');

  const apiNewsUrl = `http://127.0.0.1:5000/news/scrap/news/comp/${enterKorTextReceived}`;

  fetch(apiNewsUrl)
      .then(response => {
          // 응답이 성공적인지 확인
          // response 매개변수는 HTTP 응답 객체
          if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
          }
          // JSON 형태로 변환하여 반환
          return response.json();
      })
      .then(data => {
          // 화면에 결과 출력
          // data 매개변수는 JSON으로 변환된 데이터
          // console.log(`Text inside json ${"data"}: ${JSON.stringify(data)}`)
          if (data){
            DetailNewsElement_1.textContent = data[0];
            DetailNewsElement_2.textContent = data[1];
            DetailNewsElement_3.textContent = data[2];
            DetailNewsElement_4.textContent = data[3];
            DetailNewsElement_5.textContent = data[4];
            }
          })
      .catch(error => {
          console.error('Error:', error);
    });
          // 'key'에 해당하는 값을 출력
          // if ('avg_esti' in data) {
            // console.log('Value of key:', data['avg_esti']);

            // localStorage.setItem('progress_bar', data['avg_esti']);            
            // localStorage.setItem('detail_info', data['detail_info']);

            // console.log('LocalStorage 저장');
          // } else {
          //   console.log('Key not found in data.');
          // }

});



