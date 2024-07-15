import os


from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector

import requests
import shutil

from The_category_prediction_by_the_model import the_final_prediction_result

app = Flask(__name__)
CORS(app)
db = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="mysql24",
    database="ingredients"
)
# cursor = db.cursor()
cursor = db.cursor(dictionary=True)


def fetch_data_vegatables():
    cursor.execute("SELECT * FROM vegetables")
    data = cursor.fetchall()
    print(data)

    return data


@app.route('/ingredients/vegetable', methods=['GET'])
def list_images():
    IMAGE_FOLDER = 'downloaded_images_vegatables'
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)

    try:
        urls = fetch_data_vegatables()

        for url_tuple in urls:
            url = url_tuple['picture_src']  # Assuming the field name is 'picture_src'
            file_name = os.path.basename(url)
            file_path = os.path.join(IMAGE_FOLDER, file_name)
            ingredientName = url_tuple['ingredient_name']
            # Download the image if it doesn't already exist
            if not os.path.exists(file_path):
                source_path = os.path.join('..', '..', 'images', 'vegatables', file_name)
                shutil.copyfile(source_path, file_path)
                print(f"Copied {file_name} from {source_path} to {file_path}")
            else:
                print(f"{file_name} already exists")

        images = os.listdir(IMAGE_FOLDER)
        return jsonify(images)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
@app.route('/ingredients/vegetable/<filename>', methods=['GET'])
def get_image(filename):
    # return send_from_directory(IMAGE_FOLDER, filename)
    return send_from_directory(r'./downloaded_images_vegatables', filename)

def fetch_data_fruits():

    cursor.execute("SELECT picture_src FROM fruits")
    data = cursor.fetchall()

    # Close the connection

    return data


@app.route('/ingredients/fruits', methods=['GET'])
def list_images_fruits():
    IMAGE_FOLDER = 'downloaded_images_fruits'
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)

    try:
        urls = fetch_data_fruits()

        for url_tuple in urls:
            url = url_tuple['picture_src']  # Assuming the field name is 'picture_src'
            file_name = os.path.basename(url)
            file_path = os.path.join(IMAGE_FOLDER, file_name)

            # Download the image if it doesn't already exist
            if not os.path.exists(file_path):
                source_path = os.path.join('..', '..', 'images', 'fruits', file_name)
                shutil.copyfile(source_path, file_path)
                print(f"Copied {file_name} from {source_path} to {file_path}")
            else:
                print(f"{file_name} already exists")

        images = os.listdir(IMAGE_FOLDER)
        return jsonify(images)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
@app.route('/ingredients/fruits/<filename>', methods=['GET'])
def get_image_fruits(filename):

    return send_from_directory(r'./downloaded_images_fruits', filename)

def fetch_data_dairy_products():
    # Connect to your MySQL database
    # cursor = db.cursor(dictionary=True)

    # Fetch the data
    cursor.execute("SELECT picture_src FROM dairy_product")
    data = cursor.fetchall()

    # Close the connection

    return data


@app.route('/ingredients/dairy_products', methods=['GET'])
def list_images_dairy_products():
    IMAGE_FOLDER = 'downloaded_images_dairy_products'
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)

    try:
        urls = fetch_data_dairy_products()

        for url_tuple in urls:
            url = url_tuple['picture_src']  # Assuming the field name is 'picture_src'
            file_name = os.path.basename(url)
            file_path = os.path.join(IMAGE_FOLDER, file_name)

            # Download the image if it doesn't already exist
            if not os.path.exists(file_path):
                source_path = os.path.join('..', '..', 'images', 'dairy_product', file_name)
                shutil.copyfile(source_path, file_path)
                print(f"Copied {file_name} from {source_path} to {file_path}")
            else:
                print(f"{file_name} already exists")

        images = os.listdir(IMAGE_FOLDER)
        return jsonify(images)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
@app.route('/ingredients/dairy_products/<filename>', methods=['GET'])
def get_image_dairy_products(filename):
    # return send_from_directory(IMAGE_FOLDER, filename)
    return send_from_directory(r'./downloaded_images_dairy_products', filename)

def fetch_data_fish():
    # Connect to your MySQL database
    # cursor = db.cursor(dictionary=True)

    # Fetch the data
    cursor.execute("SELECT picture_src FROM fish")
    data = cursor.fetchall()

    # Close the connection

    return data


@app.route('/ingredients/fish', methods=['GET'])
def list_images_fish():
    IMAGE_FOLDER = 'downloaded_images_fish'
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)

    try:
        urls = fetch_data_fish()

        for url_tuple in urls:
            url = url_tuple['picture_src']  # Assuming the field name is 'picture_src'
            file_name = os.path.basename(url)
            file_path = os.path.join(IMAGE_FOLDER, file_name)

            # Download the image if it doesn't already exist
            if not os.path.exists(file_path):
                source_path = os.path.join('..', '..', 'images', 'fish', file_name)
                shutil.copyfile(source_path, file_path)
                print(f"Copied {file_name} from {source_path} to {file_path}")
            else:
                print(f"{file_name} already exists")

        images = os.listdir(IMAGE_FOLDER)
        return jsonify(images)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
@app.route('/ingredients/fish/<filename>', methods=['GET'])
def get_image_fish(filename):
    # return send_from_directory(IMAGE_FOLDER, filename)
    return send_from_directory(r'./downloaded_images_fish', filename)


def fetch_data_meat_and_chicken():

    cursor.execute("SELECT picture_src FROM meat_and_chicken")
    data = cursor.fetchall()

    return data

def fetch_data_dry_products():
    # Connect to your MySQL database
    # cursor = db.cursor(dictionary=True)

    # Fetch the data
    cursor.execute("SELECT picture_src FROM dry_products")
    data = cursor.fetchall()

    # Close the connection

    return data


@app.route('/ingredients/dry_products', methods=['GET'])
def list_images_dry_products():
    IMAGE_FOLDER = 'downloaded_images_dry_products'
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)

    try:
        urls = fetch_data_dry_products()

        for url_tuple in urls:
            url = url_tuple['picture_src']  # Assuming the field name is 'picture_src'
            file_name = os.path.basename(url)
            file_path = os.path.join(IMAGE_FOLDER, file_name)

            # Download the image if it doesn't already exist
            if not os.path.exists(file_path):
                source_path = os.path.join('..', '..', 'images', 'dry_products', file_name)
                shutil.copyfile(source_path, file_path)
                print(f"Copied {file_name} from {source_path} to {file_path}")
            else:
                print(f"{file_name} already exists")

        images = os.listdir(IMAGE_FOLDER)
        return jsonify(images)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@app.route('/ingredients/dry_products/<filename>', methods=['GET'])
def get_image_dry_products(filename):

    return send_from_directory(r'./downloaded_images_dry_products', filename)

@app.route('/ingredients/meat_and_chicken', methods=['GET'])
def list_images_meat_and_chicken():
    IMAGE_FOLDER = 'downloaded_images_meat_and_chicken'
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)

    try:
        urls = fetch_data_meat_and_chicken()

        for url_tuple in urls:
            url = url_tuple['picture_src']  # Assuming the field name is 'picture_src'
            file_name = os.path.basename(url)
            file_path = os.path.join(IMAGE_FOLDER, file_name)

            # Download the image if it doesn't already exist
            if not os.path.exists(file_path):
                source_path = os.path.join('..', '..', 'images', 'meat_and_chicken', file_name)
                shutil.copyfile(source_path, file_path)
                print(f"Copied {file_name} from {source_path} to {file_path}")
            else:
                print(f"{file_name} already exists")

        images = os.listdir(IMAGE_FOLDER)
        return jsonify(images)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
@app.route('/ingredients/meat_and_chicken/<filename>', methods=['GET'])
def get_image_meat_and_chicken(filename):
    # return send_from_directory(IMAGE_FOLDER, filename)
    return send_from_directory(r'./downloaded_images_meat_and_chicken', filename)


@app.route('/get_prediction', methods=['POST'])
def get_prediction():
    data = request.json
    print(data)
    selected_products = data.get('selectedProducts', [])
    if selected_products:
        predict_result = the_final_prediction_result(selected_products)
        response = {
            "message": "The category was successfully predicted",
            "processedData": predict_result
        }

        return jsonify(response), 200
    else:
        return jsonify({'error': 'No ingredients provided'})


if __name__ == '__main__':
    app.run(debug=True)





