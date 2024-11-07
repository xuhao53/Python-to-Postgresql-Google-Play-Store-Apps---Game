--1. What are the top 5 most downloaded games in each genre?
SELECT app, genres, rank
FROM(
    SELECT app, genres, installcounts,ROW_NUMBER() OVER (PARTITION BY genres ORDER BY installcounts DESC) AS rank
    FROM googleplaystore_app
    WHERE category = 'GAME' AND rating IS NOT NULL
)as ranked_games
WHERE rank <= 5
ORDER BY genres, rank

--2.What are the top 5 most frequently occurring genres in the "GAME" category?
SELECT genres, COUNT(*) AS Genre_Count
FROM googleplaystore_app
WHERE category = 'GAME'
GROUP BY genres
ORDER BY Genre_Count DESC
LIMIT 5;

--3.What is the average number of installs for games based on their "Content Rating" (like Everyone, Teen, etc.)?
SELECT "content rating", ROUND(AVG(installcounts),0) AS Average_Installs
FROM googleplaystore_app
WHERE category = 'GAME'
GROUP BY "content rating"
ORDER BY Average_Installs DESC;

-- 4. How does the average price and ratings of paid games vary by genre
SELECT genres, ROUND(AVG(price)::numeric,2) as avg_price,
 ROUND(AVG(rating)::numeric,2) as avg_ratings
FROM googleplaystore_app
WHERE category = 'GAME' AND type = 'Paid'
GROUP BY genres
ORDER BY avg_price DESC;

--5. Find paid games within the Action genre that have the same price,
-- and calulate the different in their ratings and installs
SELECT g1.app as Game1, g2.app AS Game2, g1.genres, g1.price, ROUND((g1.rating - g2.rating)::numeric,2) AS rating_difference,
(g1.installcounts - g2.installcounts) AS install_difference
FROM googleplaystore_app as g1
JOIN googleplaystore_app as g2
ON g1.genres = g2.genres AND g1.price = g2.price AND g1.app <> g2.app AND g1.category = g2.category AND g1.type = g2.type
WHERE g1.category = 'GAME' AND g1.type = 'Paid' AND g1.genres = 'Action'
ORDER BY rating_difference, install_difference DESC;
