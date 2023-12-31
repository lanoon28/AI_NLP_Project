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


      // API 호출
      // API 엔드포인트 URL
      const callDetailInfoUrl = 'https://api.example.com/data';

      // Fetch API를 사용하여 GET 요청 보내기
      localStorage.setItem('jsonData', fetchData(callDetailInfoUrl));

      // 다른 창 호출. 호출할 html 창 주소 입력
      window.location.href = 'detail_information.html';

      })
    });
});


document.addEventListener('DOMContentLoaded', function() {
  const displayTextElement = document.getElementById('detail_enterName');

  // 페이지 2가 로드될 때 로컬 스토리지에서 텍스트를 가져와서 화면에 표시
  const textReceived = localStorage.getItem('textToSend');

  // if (textReceived) {
  //   // 해당 id 요소가 존재하면 그 요소의 텍스트를 출력
  //   console.log(`Text inside ${"Test"}: ${textReceived}`);
  // } else {
  //   console.log(`Element with id ${"Test"} not found.`);
  // }

  if (textReceived) {
    displayTextElement.textContent = `: ${textReceived}`;
    // 로컬 스토리지의 데이터를 한 번 사용하고 나면 삭제 (선택사항)
    localStorage.removeItem('textToSend');
  }

});



// document.getElementById('getDataButton').addEventListener('click', fetchData);

// function fetchData(apiUrl) {
//   // API 엔드포인트 URL
//   // const apiUrl = 'https://api.example.com/data';

//   // Fetch API를 사용하여 GET 요청 보내기
//   fetch(apiUrl)
//     .then(response => {
//       // 응답이 성공인 경우 JSON 데이터 추출
//       if (!response.ok) {
//         throw new Error(`HTTP error! Status: ${response.status}`);
//       }
//       return response.json();
//     })
//     .then(data => {
//       // JSON 데이터를 처리하고 결과를 화면에 표시
//       displayData(data);
//     })
//     .catch(error => {
//       console.error('Fetch error:', error);
//     });
// }

// function displayData(data) {
//   // 결과를 화면에 표시하는 로직 작성
//   const resultElement = document.getElementById('result');
//   resultElement.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
// }