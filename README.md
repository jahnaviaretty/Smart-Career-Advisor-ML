
# Smart Career Advisor Using Machine Learning

## Project Overview

Smart Career Advisor is a machine learning-based web application that recommends suitable career paths based on a user's academic performance, technical skills, communication skills, problem-solving ability, projects, and certifications.

The application uses a Random Forest Classifier to generate the Top 3 career recommendations.

## Features

- User Registration and Login
- Secure Password Hashing
- Machine Learning-Based Career Prediction
- Top 3 Career Recommendations
- Prediction Scores and Visualization
- Interactive Career Prediction Dashboard
- User Prediction History
- SQLite Database Integration
- Responsive Web Interface

## Technologies Used

### Frontend
- HTML
- CSS

### Backend
- Python
- Flask

### Machine Learning
- Scikit-learn
- Random Forest Classifier
- Pandas
- NumPy
- Joblib

### Data Visualization
- Matplotlib

### Database
- SQLite

### Development Tools
- Visual Studio Code
- Git
- GitHub

## Career Categories

The application provides recommendations across five career categories:

1. Data Science
2. Artificial Intelligence and Machine Learning
3. Web Development
4. Cyber Security
5. Cloud Computing

## Project Structure

```text
Smart-Career-Advisor-ML/
│
├── database/
│   ├── app.py
│   ├── db_setup.py
│   ├── train_model_script.py
│   ├── career_dataset.csv
│   └── career_advisor.db
│
├── models/
│   └── career_model.joblib
│
├── static/
│   ├── style.css
│   └── career_chart.png
│
├── templates/
│   ├── index.html
│   ├── result.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
│
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the Project Folder

```bash
cd Smart-Career-Advisor-ML
```

### 3. Install Required Packages

```bash
python -m pip install -r requirements.txt
```

### 4. Create the Database

```bash
python database/db_setup.py
```

### 5. Run the Application

```bash
python database/app.py
```

### 6. Open in Browser

```text
http://127.0.0.1:5000
```

Register an account, log in, and start exploring career recommendations.

## Machine Learning Workflow

1. Collect and prepare the career dataset.
2. Perform data preprocessing.
3. Train a Random Forest Classifier.
4. Evaluate the model.
5. Save the trained model using Joblib.
6. Load the model into the Flask application.
7. Generate Top 3 career recommendations.
8. Visualize recommendation scores using Matplotlib.

## Future Enhancements

- Improve the training dataset with more diverse and representative records.
- Add more career categories.
- Improve model evaluation and recommendation quality.
- Add an administrator dashboard.
- Deploy the application online.
- Improve user experience and interface design.

## Important Note

This is an academic demonstration project. The current model is trained on a small sample dataset. Its recommendation scores are model outputs and should not be interpreted as validated probabilities of career suitability.

## Author

**Aretty Jahnavi**

B.Tech – Computer Science and Engineering (Data Science)

GitHub: https://github.com/jahnu08
