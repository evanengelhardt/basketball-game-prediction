# basketball-game-prediction

Python application with the ultimate goal of predicting point differential in NBA basketball games using Machine Learning

# Data Retrieval
How
- Utilizing beautiful soup to scrape the website basketball-reference.com for game information
- Currently saving data into a CSV file, but eventually will be saved into a database
What
- Using very basic data (win %, points per game, opponent points per game) for both the home and road teams
- Uses data on seasons since 2012. Will collect more data once the data parameters are refined more to optimize the algorithm

# Algorithms
What
- Predicting the winning team (home or road)
How
- Utilizing logistic regression to classify each set of data as either 1 (home win) or 0 (road win)

# Current Application
Currently the application is still in its very early stages. It objective is simply to determine the winner of each game based of the few statistical categories we collect. With the limited amount of data, parameters, and algorithm clarity, it is working with about 70% success rate. The next steps I plan on doing is finding other parameters which would help the algorithm and try to get it up to 90% success rate.

# Final Vision for product
When it's done it should be able to utilize very specific statistics and neural networks to be able to predict the approximate point differential of the game with above 75% accuracy
