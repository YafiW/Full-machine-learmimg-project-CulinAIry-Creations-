import axios from 'axios';
import { RootState } from '../App'; 

import arrIngredientsSlice from '../redux/arrIngredientsSlice';

class RecipesService {
    BASE_URL = "http://127.0.0.1:5000";

    async getRecipe(arrIngredients:[]) {
        try {
            const response = await axios.post(`${this.BASE_URL}/get_prediction`, { selectedProducts: arrIngredients });
            
            return response.data;
        } catch (error) {
            console.error('There was an error!', error);
        }
    }
}
export const selectArrIngredients = (state: RootState) => state.arrIngredients.arrIngredients;
export default new RecipesService();
