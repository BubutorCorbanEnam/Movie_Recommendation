# Movie Recommendation System

## Overview
This project is a **Movie Recommendation System** built using **Streamlit** and **Python**. It provides three types of recommendations:

1. **Popularity-Based Recommendation** - Recommends top-rated movies from a selected genre.
2. **Content-Based Recommendation** - Suggests movies similar to a selected movie based on genre.
3. **Collaborative Filtering** - Uses user preferences to recommend movies based on similar users.

## Features
- Uses **Pandas** for data manipulation.
- Implements **Cosine Similarity** for collaborative filtering.
- Provides an interactive web interface using **Streamlit**.
- Loads a preprocessed dataset stored in a **Pickle file**.

## Dataset
The system utilizes a dataset containing:
- **Movie ratings** provided by different users.
- **Movie metadata** including titles and genres.

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/BubutorCorbanEnam/Movie-Recommendation-System.git
   cd Movie-Recommendation-System
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

## Usage
- Select the type of recommendation from the sidebar.
- Provide necessary inputs (e.g., genre, movie title, user ID, etc.).
- Click the **"Get Recommendations"** button.
- View the recommended movies.

## Dependencies
- Python 3.x
- Pandas
- Streamlit
- Scikit-learn
- Pickle

## Author
**Corban Enam Bubutor**

## License
This project is licensed under the MIT License. Feel free to use and modify it!

