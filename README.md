# Full Stack Music Search & Recommendation Engine with Graph-based Visualization

## 1. DESCRIPTION

This package mainly contains 4 directories (backend, d3tree and recommendation_algo, libs) and other web application files (html, css and js).
- backend: database initialization, backend server setup, recommendation algorithms
- d3graph: visualization frame of the searching results using D3.js
- index.html, styles.css, script.js: interactive interface with the system


## 2. INSTALLATION

Please install below packages to make all files run correctly.

- sqlite3 (If you Python version is over 3.7x, sqlite3 library is built in.)
- csv
- pandas
- numpy
- matplotlib
- seaborn
- tqdm
- plotly
- sklearn
- scipy
- spotipy (Spotify python libs)

For flask:
    - Enter "CODE" directory from root directory "final_project"
        $ cd CODE
    - Use flask to manage our backend source
        $ pip install Flask
    - Handle Cross Origin Resource Sharing
        $ pip install flask-cors


## 3. EXECUTION (make sure you are in the root directory ("code"))

A. Run backend server

   - Go to backend directory
     $ cd backend
     $ python3 init_db.py

B. Run frontend with GUI

   - Create a HTTP server in "code" directory
     $ python -m http.server 5501 (python3)

   - Open a web browser and go to http://localhost:5501/


C. See data preparation and feature engineering

   - Run the cs6452_data_analysis.ipynb from /backend



## 4. LET'S TRY A SEARCH (run server and go to http://localhost:5501/)

- Enter the music name in the search bar -> click SEARCH button. 
(For example, you can fill in "Attention" in the search bar -> click "Search" to get the music features and up to 5 recommendation from "Attention".)

- After seeing d3 graph, you can drag the node or single-click it to pin (double-click to unpin). 
(Nodes exploration will be added soon.)

- The recommendation results are displayed on the center-right, you can re-search using their names to explore more.

- Feel free to answer the likert question and choose your satisfied recommendation by clicking on those checkboxes on the website, providing some suggestions to improve the system.



---- !! Important Notes !! ----

1. Currently, the graph is based on the test data, not the real search results. (Will be finished by 07/17) 

2. Recommendation lists isn't displayed. (Will be finished by 07/17) 

-------------------------------

