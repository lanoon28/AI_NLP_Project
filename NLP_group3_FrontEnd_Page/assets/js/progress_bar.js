        // 백분율을 받아와 프로그래스 바 업데이트 함수
        function updateProgressBar(percentage) {
            var progressBar = document.getElementById('progress-bar');
            var progressText = document.getElementById('progress-text');

            progressBar.style.width = percentage + '%';
            progressText.innerText = percentage + '%';
        }

        // 백분율이 변할 때 프로그래스 바 업데이트 (예: 50%)
        var percentage = 0;
        var updateInterval = 50; // 업데이트 간격 (0.05초)

        var targetPercentage = localStorage.getItem('progress_bar');
        console.log('L : Value of key:', localStorage.getItem('progress_bar'));
        console.log('T : Value of key:', targetPercentage);
        
        function updateProgressBarWithPercentage() {
            if (percentage <= targetPercentage) {
                updateProgressBar(percentage);
                percentage++;
                setTimeout(updateProgressBarWithPercentage, updateInterval);
            }

        }

        // 초기화 및 업데이트 시작
        updateProgressBarWithPercentage();