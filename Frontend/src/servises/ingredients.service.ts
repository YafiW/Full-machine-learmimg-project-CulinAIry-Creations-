import axios from'axios'
export default new class IngredientsService {
    
    BASE_URL="http://127.0.0.1:5000/ingredients";
   
    getVegetables(){
        return axios.get(`${this.BASE_URL}/vegetable`);
    }
    getFruits(){
        return axios.get(`${this.BASE_URL}/fruits`);

    }
    getDairyProducts(){
        return axios.get(`${this.BASE_URL}/dairy_products`);
    }
    getFish(){
        return axios.get(`${this.BASE_URL}/fish`);
    }
    getMeatAndChicken(){
        return axios.get(`${this.BASE_URL}/meat_and_chicken`);

    }
    getDryProducts(){
        return axios.get(`${this.BASE_URL}/dry_products`);

    }
}
