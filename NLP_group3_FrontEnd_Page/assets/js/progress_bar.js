// 백분율이 변할 때 프로그래스 바 업데이트 (예: 50%)
var percentage = 0;
var updateInterval = 50; // 업데이트 간격 (0.05초)
var targetPercentage = 0;


document.addEventListener('DOMContentLoaded', function() {

    const enterKorTextReceived = localStorage.getItem('enterNameKor');
    console.log(enterKorTextReceived);
    // API 호출
    // API 엔드포인트 URL
    const apiAvgEstiUrl = `http://127.0.0.1:5000/news/scrap/esti/comp/${enterKorTextReceived}`;

    // RESTful API로 GET 요청 보내기
    console.log('fetch 요청 전송 : Progress Bar');
    // console.log(location.origin);

    fetch(apiAvgEstiUrl)
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
            console.log(`Text inside json ${"data"}: ${JSON.stringify(data[0])}`)
            // AVG(avg_esti)
            targetPercentage = data[0];
                    
            // console.log('detail Enter', localStorage.getItem('detail_enterName'));
            // console.log('L : Value of key:', data[0]);
            // console.log('T : Value of key:', targetPercentage);

            // 초기화 및 업데이트 시작
            updateProgressBarWithPercentage();

            })
        .catch(error => {
            console.error('Error:', error);
    });

});


// 백분율을 받아와 프로그래스 바 업데이트하는 함수
function updateProgressBar(percentage) {
    var progressBar = document.getElementById('progress-bar');
    var progressText = document.getElementById('progress-text');

    progressBar.style.width = percentage + '%';
    progressText.innerText = percentage + '%';
}

function updateProgressBarWithPercentage() {
    if (percentage <= targetPercentage) {
        updateProgressBar(percentage);
        percentage++;
        setTimeout(updateProgressBarWithPercentage, updateInterval);
    }

}

