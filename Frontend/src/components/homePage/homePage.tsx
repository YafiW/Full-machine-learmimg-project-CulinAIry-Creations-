import React, { FC, useState } from 'react';
import './homePage.scss';
import 'bootstrap/dist/css/bootstrap.min.css';
import RecipesService from '../../servises/recipes.servises'
import { useNavigate } from 'react-router-dom'
import { error } from 'console';

interface HomePageProps { }

const HomePage: FC<HomePageProps> = () => {
  const [ingredientsInputs, setingredientsInputs] = useState([{ id: 1, value: '' }]);
  const [recipe, setRecipe] = useState<any>()
  const addInput = () => {
    const newInputId = ingredientsInputs.length + 1;
    setingredientsInputs([...ingredientsInputs, { id: newInputId, value: '' }]);
  };

//   const sendIngredientsToServer = () => {
//     debugger
//      RecipesService.getRecipe(ingredientsInputs).then((recipe)=>{
//       setRecipe(recipe)
//       console.log(recipe)
//     },(error)=>{
// debugger
//     })
  
  // }
  const handleInputChange = (id: any, value: any) => {
    const updatedingredientsInputs = ingredientsInputs.map(input => {
      if (input.id === id) {
        return { ...input, value: value };
      }
      return input;
    });
    setingredientsInputs(updatedingredientsInputs);
  };

  return (
    <div className='about'>
      <h4 className='about1'><h1>Hi, welcome to culinAIry creation!!</h1><br></br>
          A site for creating customized recipes for products you have at home!<br></br>
          Here you can choose a selected amount of products that you have in your cupboard or refrigerator, thus avoiding an unnecessary trip to the supermarket...
          <br></br>Our website will create an amazing recipe for you that will give you a new way of thinking for using the products you already have and will filter for the recipe products that are not suitable for the dish we will create for you.
          <br></br>Come on let's start!</h4>
    </div>
  );

}

export default HomePage;
