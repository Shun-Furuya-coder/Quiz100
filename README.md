# Quiz100

## Project Overview
Quiz100 is an interactive web-based quiz platform that combines education with entertainment. It allows users to both take quizzes across a variety of categories and create their own quizzes. This platform aims to enhance learning experiences while providing a fun and engaging way to test knowledge and discover new information.

## Features
- **User Authentication**: Secure login and registration system to manage user sessions.
- **Quiz Creation and Management**: Users can create and customize their own quizzes.
- **Interactive Quiz Taking**: Users can take quizzes with instant feedback on answers.

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup
1. Clone the repository:

git clone https://github.com/Shun-Furuya-coder/Quiz100.git
cd quiz-project

2. Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate

3. Install the required dependencies:

pip install -r requirements.txt

4. Initialize the database:

python init_db.py

5. Start the server:

python app.py