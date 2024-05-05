document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/quizzes')
        .then(response => response.json())
        .then(quizzes => {
            const quizList = document.getElementById('quiz-list');
            if (quizzes.length > 0) {
                quizzes.forEach((quiz, index) => {
                    const quizItem = document.createElement('div');
                    quizItem.className = 'application-item';

                    const quizTitle = document.createElement('span');
                    quizTitle.className = 'job-title';
                    quizTitle.textContent = quiz.title;

                    const actionsDiv = document.createElement('div');
                    actionsDiv.className = 'actions';

                    const takeButton = document.createElement('button');
                    takeButton.className = 'button';
                    takeButton.textContent = 'Take';

                    takeButton.addEventListener('click', () => {
                        window.location.href = `TakingQuiz.html?quiz_id=${quiz.quiz_id}`;
                    });

                    actionsDiv.appendChild(takeButton);
                    quizItem.appendChild(quizTitle);
                    quizItem.appendChild(actionsDiv);
                    quizList.appendChild(quizItem);
                });
            } else {
                const noQuizMessage = document.createElement('p');
                noQuizMessage.textContent = "No quizzes available. Please create a new quiz.";
                quizList.appendChild(noQuizMessage);
            }
        })
        .catch(error => console.error('Error fetching quizzes:', error));
});
