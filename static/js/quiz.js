// Quiz functionality
function initializeQuiz(totalQuestions, quizDuration) {
    document.addEventListener('DOMContentLoaded', function() {
        // Quiz navigation
        const nextButtons = document.querySelectorAll('.next-question');
        const prevButtons = document.querySelectorAll('.prev-question');
        
        nextButtons.forEach(function(button) {
            button.addEventListener('click', function() {
                const currentQuestion = parseInt(this.getAttribute('data-question'));
                const currentCard = document.getElementById('question-' + currentQuestion);
                const nextCard = document.getElementById('question-' + (currentQuestion + 1));
                
                // Check if current question is answered
                const inputs = currentCard.querySelectorAll('input[type="radio"]');
                const questionId = inputs[0].name.split('_')[1];
                const isAnswered = document.querySelector('input[name="question_' + questionId + '"]:checked');
                
                if (!isAnswered) {
                    alert('Please select an answer before proceeding.');
                    return;
                }
                
                currentCard.classList.remove('active');
                nextCard.classList.add('active');
                
                // Update progress bar
                updateProgress((currentQuestion + 1) / totalQuestions * 100);
            });
        });
        
        prevButtons.forEach(function(button) {
            button.addEventListener('click', function() {
                const currentQuestion = parseInt(this.getAttribute('data-question'));
                const currentCard = document.getElementById('question-' + currentQuestion);
                const prevCard = document.getElementById('question-' + (currentQuestion - 1));
                
                currentCard.classList.remove('active');
                prevCard.classList.add('active');
                
                // Update progress bar
                updateProgress((currentQuestion - 1) / totalQuestions * 100);
            });
        });
        
        // Progress bar update
        function updateProgress(percentage) {
            const progressBar = document.getElementById('progress-bar');
            progressBar.style.width = percentage + '%';
            progressBar.setAttribute('aria-valuenow', percentage);
            progressBar.textContent = Math.round(percentage) + '%';
        }
        
        // Timer functionality
        const timerDisplay = document.getElementById('quiz-timer');
        if (timerDisplay && quizDuration) {
            const timeParts = quizDuration.split(':').map(Number);
            const hours = timeParts[0] || 0;
            const minutes = timeParts[1] || 0;
            let totalSeconds = hours * 3600 + minutes * 60;
            
            const timer = setInterval(function() {
                totalSeconds--;
                
                if (totalSeconds <= 0) {
                    clearInterval(timer);
                    alert('Time is up! Your quiz will be submitted.');
                    document.getElementById('quiz-form').submit();
                    return;
                }
                
                const hoursLeft = Math.floor(totalSeconds / 3600);
                const minutesLeft = Math.floor((totalSeconds % 3600) / 60);
                const secondsLeft = totalSeconds % 60;
                
                const hoursStr = String(hoursLeft).padStart(2, '0');
                const minutesStr = String(minutesLeft).padStart(2, '0');
                const secondsStr = String(secondsLeft).padStart(2, '0');
                
                timerDisplay.textContent = 'Time remaining: ' + hoursStr + ':' + minutesStr + ':' + secondsStr;
                
                // Warning when 5 minutes left
                if (totalSeconds === 300) {
                    alert('5 minutes remaining!');
                }
            }, 1000);
        }
    });
}