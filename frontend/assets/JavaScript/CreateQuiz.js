document.addEventListener('DOMContentLoaded', function() {
    let quizData = {
        title: '',
        questions: []
    };

    document.getElementById('add-question').addEventListener('click', function() {
        const questionsContainer = document.getElementById('questions-container');
        const questionIndex = questionsContainer.querySelectorAll('.question-container').length;

        const questionHTML = `
            <div class="question-container" id="question-container-${questionIndex}">
                <div class="form-group mb-3">
                    <label>Question ${questionIndex + 1}</label>
                    <input type="text" class="form-control" id="question-${questionIndex}">
                </div>
                ${[1, 2, 3, 4].map(option => `
                    <div class="form-group mb-3">
                        <label>Option ${option}:</label>
                        <input type="text" class="form-control" id="option${option}-${questionIndex}">
                    </div>
                `).join('')}
                <div class="form-group mb-3">
                    <label>Correct Option#:</label>
                    <select class="form-control" id="correct-option-${questionIndex}">
                        <option value="1">1</option>
                        <option value="2">2</option>
                        <option value="3">3</option>
                        <option value="4">4</option>
                    </select>
                </div>
            </div>
        `;
        const questionDiv = document.createElement('div');
        questionDiv.innerHTML = questionHTML;
        questionsContainer.appendChild(questionDiv);
    });

    document.getElementById('submit-quiz').addEventListener('click', function(event) {
        event.preventDefault();
        const quizName = document.getElementById('quiz-name').value.trim();
        if (!quizName) {
            alert('Please enter a quiz name.');
            return;
        }

        let isValid = true;
        const questions = [];

        const questionContainers = document.querySelectorAll('.question-container');
        questionContainers.forEach((container, index) => {
            const questionInput = document.getElementById(`question-${index}`);
            const questionText = questionInput ? questionInput.value.trim() : '';
            const options = [1, 2, 3, 4].map(option => {
                const optionInput = document.getElementById(`option${option}-${index}`);
                return optionInput ? optionInput.value.trim() : '';
            });
            const correctOptionInput = document.getElementById(`correct-option-${index}`);
            const correctOption = correctOptionInput ? parseInt(correctOptionInput.value) : null;

            if (!questionText || options.some(option => option === '') || correctOption === null) {
                isValid = false;
                console.error(`Validation failed for question ${index + 1}`);
            }

            if (isValid) {
                questions.push({
                    question: questionText,
                    options: options,
                    answer: correctOption
                });
            }
        });

        if (!isValid || questions.length === 0) {
            alert('Please complete all fields in each question and ensure each question has at least one option.');
            return;
        }

        const quizData = {
            title: quizName,
            questions: questions
        };

        fetch('/api/create_quiz', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(quizData)
        })
        .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    window.location.href = 'Home.html';
                } else {
                    alert('Failed to create quiz: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error creating quiz:', error);
                alert('An error occurred. Please try again.');
            });
    });
});
