let quiz;

document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const quizId = urlParams.get('quiz_id');

    fetch(`/api/quizzes/${quizId}`)
        .then(response => response.json())
        .then(data => {
            quiz = data;
            displayQuiz(quiz);
        })
        .catch(error => console.error('Error loading the quiz:', error));
});

function displayQuiz(quiz) {
    const quizTitleElement = document.getElementById('quiz-title');
    const questionsContainer = document.getElementById('questions-container');

    quizTitleElement.textContent = quiz.title;

    quiz.questions.forEach((question, questionIndex) => {
        const questionElement = document.createElement('div');
        questionElement.className = 'quiz-question';
        questionElement.innerHTML = `<p>Q${questionIndex + 1}. ${question.question_text}</p>`;

        question.options.forEach((option, optionIndex) => {
            const optionID = `q${questionIndex}-option${optionIndex}`;
            questionElement.innerHTML += `
                <div class="form-check">
                    <input class="form-check-input" type="radio" name="answer${questionIndex}" id="${optionID}" value="${option.option_id}">
                    <label class="form-check-label" for="${optionID}">${option.option_text}</label>
                </div>
            `;
        });

        questionsContainer.appendChild(questionElement);
    });

    document.getElementById('submit-quiz').addEventListener('click', function() {
        submitQuiz(quiz);
    });
}

function submitQuiz(quiz) {
    const answers = {};
    let isAllAnswered = true;

    quiz.questions.forEach((question, index) => {
        const selectedOption = document.querySelector(`input[name="answer${index}"]:checked`);
        if (selectedOption) {
            answers[question.question_id] = parseInt(selectedOption.value);
        } else {
            isAllAnswered = false;
        }
    });

    if (!isAllAnswered) {
        alert('Please answer all questions before submitting the quiz.');
    } else {
        fetch('/api/submit_quiz', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ quiz_id: quiz.quiz_id, answers: answers })
        })
        .then(response => response.json())
        .then(result => {
            localStorage.setItem('score', result.score);
            localStorage.setItem('totalQuestions', result.total_questions);
            window.location.href = 'Score.html';
        })
        .catch(error => console.error('Error submitting quiz:', error));
    }
}