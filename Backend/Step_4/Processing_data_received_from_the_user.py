from flask import Flask, request, jsonify
from MachineLearningFinalProject.Step_5.The_category_prediction_by_the_model import the_final_prediction_result
app = Flask(__name__)

@app.route('/get_prediction', methods=['GET'])
def get_prediction():
    data = request.json
    selected_products = data.get('selectedProducts', [])
    if selected_products:
        predict_category = the_final_prediction_result(selected_products)
        response = {
            "message": "The category was successfully predicted",
            "processedData": predict_category
        }

        return jsonify(response), 200
    else:
        return jsonify({'error': 'No ingredients provided'})




if __name__ == '__main__':
    app.run(debug=True)