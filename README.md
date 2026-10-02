Great — here’s how you can embed the video link into the README and make it look polished:

---

## 📽 Demo Video

You can watch the project in action here:
[▶ Watch Demo Video on YouTube](https://youtu.be/Pl4YZ1LzM38)

Or embed it directly (if GitHub supports the preview):

```markdown
[![Project Demo Video](https://img.youtube.com/vi/Pl4YZ1LzM38/0.jpg)](https://youtu.be/Pl4YZ1LzM38)
```

Clicking the thumbnail will open the video: [https://youtu.be/Pl4YZ1LzM38](https://youtu.be/Pl4YZ1LzM38)



# Auto-MCQ-ML-LMS

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python\&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green?logo=django\&logoColor=white)](https://www.djangoproject.com/)
[![NLTK](https://img.shields.io/badge/NLTK-3.8-orange?logo=python\&logoColor=white)](https://www.nltk.org/)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)

**Intelligent Learning Management System with Automated MCQ Generation using Machine Learning**

---

## 🎯 Project Overview

This project is a **Django-based Learning Management System (LMS)** designed for both instructors and students. It leverages **Machine Learning and NLP** to automatically generate multiple-choice questions (MCQs) from any input text, helping instructors save time while creating assessments.

**Key Features:**

* Instructor & student dashboards
* Course creation, enrollment, and management
* Python question bank and test creation
* Automated MCQ generation from text using ML & NLP
* Real-time test taking and scoring
* Student performance tracking and analytics
* MCQs review and save to question bank
* Secure authentication and role-based access

---

## 🧠 Technology Stack

* **Backend:** Django, Python
* **Frontend:** HTML, CSS, Bootstrap
* **Machine Learning & NLP:** NLTK (tokenization, POS tagging, lemmatization)
* **Database:** SQLite (default, can switch to PostgreSQL/MySQL)

---

## ⚡ Features in Detail

1. **Automated MCQ Generation**

   * Extracts keywords, replaces them with blanks, and creates distractors.
   * Supports review and saving of generated MCQs.

2. **Course & Enrollment Management**

   * Instructors can create courses and assign subjects.
   * Students can enroll in available courses.

3. **Test Creation & Analytics**

   * Instructors can create tests from the question bank.
   * Students can take tests and get instant scores.
   * Average scores and test attempts are tracked for performance analysis.

4. **Role-Based Dashboards**

   * Instructor dashboard for course, test, and student management.
   * Student dashboard for enrolled courses, active tests, and performance history.

---

## 📽 Demo Video

You can watch the project in action here:

![Project Demo](path-to-your-video.gif)

> Replace `path-to-your-video.gif` with your actual video or GIF file in the repo.

---

## 🛠 Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/Auto-MCQ-ML-LMS.git
cd Auto-MCQ-ML-LMS
```

2. **Create a virtual environment:**

```bash
python -m venv venv
# Activate the virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

> **requirements.txt** example:

```
Django>=4.2
nltk
```

4. **Download necessary NLTK data:**

```python
import nltk

nltk.download('punkt')  # Sentence & word tokenizer
nltk.download('stopwords')  # Stopwords list
nltk.download('wordnet')  # Lemmatizer
nltk.download('averaged_perceptron_tagger')  # POS tagging
```

5. **Apply database migrations:**

```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create a superuser:**

```bash
python manage.py createsuperuser
```

7. **Run the development server:**

```bash
python manage.py runserver
```

8. **Access the app:**
   Open your browser at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 📂 Folder Structure

```
Auto-MCQ-ML-LMS/
├── manage.py
├── README.md
├── requirements.txt
├── mcq_generator.py
├── app/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── templates/
│   └── static/
└── media/   # For uploaded videos/images
```

---

## 🤖 Machine Learning / NLP Part

* Uses **NLTK** for:

  * Tokenization (`sent_tokenize`, `word_tokenize`)
  * Stopwords removal
  * POS tagging (to extract nouns/adjectives)
  * Lemmatization
* Generates MCQs with **correct answers** and **distractors** automatically.

---

## 📈 Future Enhancements

* Use **WordNet-based smarter distractors** for more challenging MCQs
* Add **text-to-speech** for accessibility
* Add **AI-powered hints/explanations** for each question
* Deploy on **cloud platforms** like AWS or Heroku for live access

---

## 📄 License


