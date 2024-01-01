        // 백분율을 받아와 프로그래스 바 업데이트 함수
        function updateProgressBar(percentage) {
            var progressBar = document.getElementById('progress-bar');
            var progressText = document.getElementById('progress-text');

            progressBar.style.width = percentage + '%';
            progressText.innerText = percentage + '%';
        }

        // 백분율이 변할 때 프로그래스 바 업데이트 (예: 50%)
        var percentage = 0;
        var targetPercentage = 50;
        var updateInterval = 50; // 업데이트 간격 (0.05초)

        function updateProgressBarWithPercentage() {
            if (percentage <= targetPercentage) {
                updateProgressBar(percentage);
                percentage++;
                setTimeout(updateProgressBarWithPercentage, updateInterval);
            }

        }

        // 초기화 및 업데이트 시작
        updateProgressBarWithPercentage();