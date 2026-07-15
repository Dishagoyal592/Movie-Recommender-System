# 🎬 Movie Recommender System

## 📌 Overview

This project builds a movie recommendation system using the **Content-Based Filtering** technique.

Movies are recommended based on their similarity using movie features such as genres, keywords, cast, director and movie overview.

The project is deployed as an interactive **Streamlit web application**.

---

## 🚀 Features

- Movie Recommendation System
- Content-Based Movie Recommendation
- Top 5 Similar Movie Recommendations
- Cosine Similarity based Recommendations
- Movie Details and Ratings
- Movie Posters using TMDB API
- Interactive Streamlit Dashboard

---

## 📊 Dataset

**TMDB 5000 Movies Dataset**--https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata

### Features Used

- Genres
- Keywords
- Cast
- Director
- Movie Overview

Dataset Size:

- **4,803 Movies**
- **5 Features**

---

## 🤖 Machine Learning Pipeline

### Data Preprocessing

- Movie metadata processing
- Feature selection
- Feature combination
- Text preprocessing

### Model Training

**Algorithm Used**

- Content-Based Filtering
- Cosine Similarity

### Movie Recommendation

The application recommends the **Top 5 similar movies** based on the selected movie.

Recommendations are generated based on:

- Genres
- Keywords
- Cast
- Director
- Movie Overview

---

## 🛠️ Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- CountVectorizer
- Cosine Similarity
- Streamlit
- TMDB API

---

## 📂 Project Structure

    Movie-Recommender-System/
    │── app.py
    │── Movie_Recommender_System.ipynb
    │── movies.pkl
    │── similarity.pkl
    │── vectorizer.pkl
    │── requirements.txt
    │── README.md

---

## ▶️ Run Locally

    pip install -r requirements.txt
    streamlit run app.py

---

## 🌐 Live Demo

https://movie-recommender-system-j9kbxomexgqh9ogzezodvn.streamlit.app/

---

## 👩‍💻 Author

**Disha Goyal**

B.E. Robotics & AI Engineering

Thapar Institute of Engineering & Technology

---

⭐ If you found this project useful, consider giving it a star!
