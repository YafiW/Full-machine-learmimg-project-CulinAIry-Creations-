# Machine-learning-full-project
## An artificial intelligence project to create customized recipes.
The project is built by a client - React.
Server side - Python.
Libraries used server side:
os, sklearn, nupmy, keras, trasentflow, matplotlib, pandas, nltk, flask.
The user chooses selected products that he has at home through the screen.
The selected products are sent to a Python server,
The server classifies the products using an AI code and an appropriate classification model for the appropriate category for these products.
After the appropriate category has been selected for the products chosen by the user, the algorithm filters products that are not relevant for this category and for the remaining products it creates an appropriate quantity for each product with the help of a rival network model.
The user receives back the products suitable for the created recipe together with appropriate quantities and relevant preparation instructions for this category.

## An extensive explanation of the project structure:
### Data preparation
The project is based on a dataset that does not exactly meet all the requirements of the project, and I adjusted it manually to my needs, by algorithms I wrote and ran on the dataset.
The algorithms:
An algorithm that produces vectors - one for each category, that contain keywords of that category. Then go through each recipe and according to its title, and with the help of the vectors, add a category column that has the classification of the specific recipe.

An algorithm that adds a column of filtered components to the dataset and for each recipe goes through its components, extracts from there only the nouns, i.e. without the quantities and without adjectives, etc. using the nltk library, generates an array of clean components only, and puts it in the appropriate cell.

After that I wrote an algorithm that for each recipe extracts its filtered products, and adds a column for each product, so that for each product that exists in the recipes there will be a column in the dataset. And finally goes through all the recipes and marks 1 for a product that is in the recipe, and 0 if not.
After the data was processed it could be sent to the model.
The model was a logistic regression model.

After predicting the category of most of the received products, for which we want to generate a recipe, we will clean the products that do not match this category from the user's product vector.
By building a vector for each category, and sifting through the products that do not fit.
So we are left with the products that match the category only.

We would then like to produce the quantities for the remaining respective products,
Preparing the data for the quantity forecasting model - Cgan:
Pumping the products together with their quantity and sending the quantities to the model.
The selected model is:
Conditional generative adversarial network
The model builds a generator - whose role is to come up with the quantities for each product, and a discriminator - whose role is to improve the performance of the generator, by determining whether its inventions are false or true until an optimal result.

After training the respective models, we will send to the model container the corresponding vector according to the products chosen by the user and return to the user the recipe created for him.

#### enjoy your meal!
