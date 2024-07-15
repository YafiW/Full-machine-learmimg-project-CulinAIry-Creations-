import React, { useState } from 'react';
import { useSelector } from 'react-redux';
import RecipesService from '../../servises/recipes.servises';
import { useNavigate } from 'react-router-dom';
import Loadder from '../Loadder/Loadder';
import './Sending_the_ingredients.scss';

const SendingTheIngredients = () => {
    const arrIngredients = useSelector((state: any) => state.arrIngredients.arrIngredients);
    const [response, setResponse] = useState<any>();
    const [isLoadder, setIsLoadder] = useState<boolean>(false);
    const navigate = useNavigate();

    const handleSubmit = async () => {
        setIsLoadder(true);
        try {
            const response = await RecipesService.getRecipe(arrIngredients);
            console.log(response);
            setResponse(response.data);
            navigate('/recipeResult', { state: response.processedData });
        } catch (error) {
            console.error("Error fetching recipe:", error);
        } finally {
            setIsLoadder(false);
        }
    };

    return (
        <div className='btnnn'>
            <button className="btn btn-outline-success" onClick={handleSubmit}>Send the Ingredients</button>
            {isLoadder && <Loadder />}
        </div>
    );
};

export default SendingTheIngredients;
