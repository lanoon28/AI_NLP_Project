document.addEventListener('DOMContentLoaded', function() {
  // 클래스명이 myClass인 모든 요소를 선택하고 이벤트 리스너 등록
  const elementsWithClass = document.querySelectorAll('.listing-item');
  const enterNameID = "enterName"
  
  // 핵심 : 이벤트 리스너 연결
  elementsWithClass.forEach(element => {
    element.addEventListener('click', function() {

      console.log('이벤트 작동');

      // 클릭된 요소의 "enterName" ID를 가진 하위 요소의 텍스트 가져오기
      const enterNameText = this.querySelector('#enterName').textContent;
      
      // JS 내부 스토리지에, 텍스트 저장
      localStorage.setItem('textToSend', enterNameText);

      // 다른 창 호출. 호출할 html 창 주소 입력
      // window.location.href = 'detail_information.html';
      })
    });
});


document.addEventListener('DOMContentLoaded', function() {
  const displayTextElement = document.getElementById('detail_enterName');
  const displayDetailElement = document.getElementById('detailInfoText');
  // 페이지 2가 로드될 때 로컬 스토리지에서 텍스트를 가져와서 화면에 표시
  const textReceived = localStorage.getItem('textToSend');


  if (textReceived) {
    displayTextElement.textContent = `: ${textReceived}`;
    // 로컬 스토리지의 데이터를 한 번 사용하고 나면 삭제 (선택사항)
    localStorage.removeItem('textToSend');
  }


  // API 호출
  // API 엔드포인트 URL
  const apiUrl = 'http://127.0.0.1:5000/api/data';
  // RESTful API로 GET 요청 보내기
  console.log('fetch 요청 전송');
  console.log(location.origin);

  fetch(apiUrl)
    .then(response => {
        // 응답이 성공적인지 확인
        // response 매개변수는 HTTP 응답 객체

        console.log('response 이벤트 작동 1');

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
                
        console.log(`Text inside ${"response"}: ${response}`)
        console.log('response 이벤트 작동 2');

        // JSON 형태로 변환하여 반환
        return response.json();
      })
      .then(data => {
          // 화면에 결과 출력
          // data 매개변수는 JSON으로 변환된 데이터
          console.log(`Text inside ${"data"}: ${JSON.stringify(data)}`)

          // 'key'에 해당하는 값을 출력
          if ('avg_esti' in data) {
            console.log('Value of key:', data['avg_esti']);

            localStorage.removeItem('progress_bar');
            console.log('LocalStorage 초기화');

            localStorage.setItem('progress_bar', data['avg_esti']);
            console.log('LocalStorage 저장');

          } else {
            console.log('Key not found in data.');
          }

        })
      .catch(error => {
          console.error('Error:', error);
      });



  // if (textReceived) {
  //   // 해당 id 요소가 존재하면 그 요소의 텍스트를 출력
  //   console.log(`Text inside ${"Test"}: ${textReceived}`);
  // } else {
  //   console.log(`Element with id ${"Test"} not found.`);
  // }

});



