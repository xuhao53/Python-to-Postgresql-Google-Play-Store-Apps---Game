# Python-SQL-Project
This repository contains the data analysis work I completed using Python and PostgreSQL. The dataset is from https://www.kaggle.com/datasets/yusufdelikkaya/google-play-store-apps-dataset/data. Credits to Yusuf Delikkaya for providing the dataset.
## Step 1: Data Cleaning using Python:

I created a Kaggle notebook that provides a detailed explanation of each step in the data cleaning process. https://www.kaggle.com/code/haoxu1041/data-cleaning-project-google-play-store-apps

## Step 2: Adding sqlalchemy toolkits to Python, Converting cleaned dataset to PostgreSQL database

Prerequisites: pandas and sqlalchemy

<img width="311" alt="Screenshot 2024-11-07 at 12 22 20 PM" src="https://github.com/user-attachments/assets/fc6100f9-ee85-4d94-b4ad-f0657a2dd872">

Prerequisites: Insatll PostgreSQL on your pc

<img width="720" alt="Screenshot 2024-11-07 at 12 22 32 PM" src="https://github.com/user-attachments/assets/94014e01-3b53-47f2-b14b-a9a213470c68">

To use the Python-SQL-Project, you first need to create a password during the PostgreSQL installation. Next, create a database using pgAdmin4, verify the port, and fill in the information in Python.


This is what the database looks like. I'm using Visual Studio Code to handle both Python and SQL.

<img width="392" alt="Screenshot 2024-11-07 at 12 32 03 PM" src="https://github.com/user-attachments/assets/77a6bcf4-7de9-4a8c-9079-73de02b38613">

## Step 3: Analysis

I want to develop my next mobile game. To do that, I need to know what's trending on the Google Play Store. That's why I'm analyzing this dataset. The insights I gain will help me determine the direction of my next game. Unfortunately, the dataset doesn't include in-app purchase (IAP) data, so I won't be able to calculate revenue for Free games. Therefore, I will avoid questions related to revenue.

> 1.  What are the top 5 most downloaded games in each genre?
```
SELECT app, genres, rank
FROM(
    SELECT app, genres, installcounts,ROW_NUMBER() OVER (PARTITION BY genres ORDER BY installcounts DESC) AS rank
    FROM googleplaystore_app
    WHERE category = 'GAME' AND rating IS NOT NULL
)as ranked_games
WHERE rank <= 5
ORDER BY genres, rank
```
This question helps to find the most popular games within each genre.

> 2. What are the top 5 most frequently occurring genres in the GAME category?
```
SELECT genres, COUNT(*) AS Genre_Count
FROM googleplaystore_app
WHERE category = 'GAME'
GROUP BY genres
ORDER BY Genre_Count DESC
LIMIT 5;
```
This question helps identify popular genres.

> 3. What is the average number of installs for games based on their "Content Rating" (like Everyone, Teen, etc.)?
```
SELECT "content rating", ROUND(AVG(installcounts),0) AS Average_Installs
FROM googleplaystore_app
WHERE category = 'GAME'
GROUP BY "content rating"
ORDER BY Average_Installs DESC;
```
This question provies insight into how different target age group correlate with installs

> 4. How does the average price and ratings of paid games vary by genre
```
SELECT genres, ROUND(AVG(price)::numeric,2) as avg_price, ROUND(AVG(rating)::numeric,2) as avg_ratings
FROM googleplaystore_app
WHERE category = 'GAME' AND type = 'Paid'
GROUP BY genres
ORDER BY avg_price DESC;
```
If I want to make a Paid game this time, this question can provide standard selling price so that I can set a reasonable price. Average ratings can give me a sense of quality within genres.

> 5. Find paid games within the Action genre that have the same price, and calulate the different in their ratings and installs
```
SELECT g1.app as Game1, g2.app AS Game2, g1.genres, g1.price, ROUND((g1.rating - g2.rating)::numeric,2) AS rating_difference,(g1.installcounts - g2.installcounts) AS install_difference
FROM googleplaystore_app as g1
JOIN googleplaystore_app as g2
ON g1.genres = g2.genres AND g1.price = g2.price AND g1.app <> g2.app AND g1.category = g2.category AND g1.type = g2.type
WHERE g1.category = 'GAME' AND g1.type = 'Paid' AND g1.genres = 'Action'
ORDER BY rating_difference, install_difference DESC;
```
I want to know if there is a correlation between the ratings difference and the installs difference for paid games with the same genre and the same selling price. 
