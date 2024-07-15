import { createSlice } from '@reduxjs/toolkit';
import { RootState } from '../App';

const initialState = {
    arrIngredients:[] as string[]
};

const arrIngredientsSlice = createSlice({
    name: 'arrIngredients',
    initialState: initialState,
    reducers: {
        addIngredient: (state, action) => {
            // const stringIngredient = JSON.stringify(action.payload.ingredient);
            state.arrIngredients.push(action.payload.ingredient);
        },
        removeIngredient: (state, action) => {
            const index = state.arrIngredients.indexOf(action.payload.ingredient);
            if (index !== -1) {
              state.arrIngredients.splice(index, 1);
            }
          }
    },
});
export const selectArrIngredients = (state: RootState) => state.arrIngredients.arrIngredients;
export const { addIngredient,removeIngredient } = arrIngredientsSlice.actions;
export default arrIngredientsSlice.reducer;
