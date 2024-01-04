document.addEventListener('DOMContentLoaded', function() {
    
    const growthListElement = document.getElementById('growth_list');
    const decreasedListElement = document.getElementById('decreased_list');

    // RESTful API로 GET 요청 보내기
    console.log('fetch 요청 전송 : index hot');

    // 급상승 기업
    const apiNewsUrl_growth = `http://127.0.0.1:5000/news/hot`;

    fetch(apiNewsUrl_growth)
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
            console.log(`Text inside json ${"data"}: ${JSON.stringify(data)}`)
            growthListElement.textContent = JSON.stringify(data);

            })
        .catch(error => {
            console.error('Error:', error);
        });

    // 급상승 기업
    const apiNewsUrl_descrease = `http://127.0.0.1:5000/news/cold'`;

    console.log('fetch 요청 전송 : index cold');
    fetch(apiNewsUrl_descrease)
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
            console.log(`Text inside json ${"data"}: ${JSON.stringify(data)}`)
            decreasedListElement.textContent = JSON.stringify(data);

            })
        .catch(error => {
            console.error('Error:', error);
        });
});