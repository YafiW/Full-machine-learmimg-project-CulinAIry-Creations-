import React, { FC } from 'react';
import './recipeResult.scss';
import { useLocation } from 'react-router-dom';
import { bool } from 'yup';

interface RecipeResultProps { }

const RecipeResult: FC<RecipeResultProps> = () => {
  const location = useLocation();
  const recipe = location.state || [];
  debugger
  const cakePreparationInstructions = [
    "Mix the dry ingredients in one bowl.",
    "Mix the liquid ingredients in a separate bowl.",
    "Combine the two bowls with gentle folding movements.",
    "Pour into a suitable mold.",
    "Bake the cake until a toothpick comes out dry."
  ];

  const saladPreparationInstructions = [
    "Cut all the ingredients to the right size for you.",
    "Pour into a suitable bowl.",
    "Shake all the liquids into the sauce in a small bowl.",
    "Pour over the beautiful ingredients you cut.",
    "Mix everything and serve."
  ];

  const meatAndChicken = [
    'entrecote', 'hamburger', 'Chicken thighs', 'Chicken sausage',
    'Brisket', 'beef schnitzel', 'Asado', 'Chicken wings', 'edges',
    'Lamb shoulder', 'Roast shoulder', 'roast beef', 'muscle meat',
    'Mock fillet', 'Mince', 'meat ribs', 'Shoulder cubes', 'sirloin',
    'turkey throat', 'turkey breast', 'turkey turkey', 'turkey shawarma',
    'turkey wings', 'turkey thighs', 'turkey liver'
  ];

  const fish = [
    'carp', 'Dennis', 'Bermondi', 'mullet', 'salmon', 'Sea bass', 'tilapia', 'tuna'
  ];

  const predictedCategory = recipe[recipe.length - 1];
  let preparationInstructions = [];

  if (predictedCategory === 'cake') {
    preparationInstructions = cakePreparationInstructions;
  } else if (predictedCategory === 'salad') {
    preparationInstructions = saladPreparationInstructions;
  } else if (predictedCategory === 'meat and chicken and fish') {
    let meatFound = false;
    let fishFound = false;
    
    for (let ingredient of recipe.slice(0, -1)) {
      if (meatAndChicken.includes(ingredient.product)) {
        meatFound = true;
      }
      if (fish.includes(ingredient.product)) {
        fishFound = true;
      }
    }

    if (meatFound) {
      preparationInstructions.push("Put the meat in a suitable pot.\n",
        "Cut the accompanying products if necessary.\n",
        "Put everything in the pot.\n",
        "Fill with water until the products are completely covered.\n",
        "Bring to a boil.\n",
        "Add salt, black pepper and appropriate spices.\n",
        "Cook over low heat until the meat is soft and ready to eat.\n");
    }
    if (fishFound) {
      preparationInstructions.push("Cut the fish into slices that suit you.\n",
      "Place the pieces of fish on a tray lined with baking paper.\n",
      "Mix the rest of the ingredients and pour over the fish.\n",
      "Bake for a short time only until the fish is ready.\n");
    }
  } else {
    preparationInstructions = ["Put all the ingredients in a suitable pot.",
      "Fill with water.",
      "Cook until desired softening.",
      "Strain and serve"];
  }

  return (
    <div className="recipeResult">
      <div className='title'>
        <h1>Hooray!!</h1>
        <p>How beautiful! We created a recipe for you from the ingredients you have at home!</p>
      </div>  
      <div className="card border-success mb-3">
        <div className="card-header">The Products</div>
        <div className="card-body text-success">
          <ul>
            {recipe.slice(0, -1).map((ingredient: any, index: any) => (
              <li key={index}>{ingredient.quantity} {ingredient.product}</li>
            ))}
          </ul>
        </div>
      </div>
      <div className="card border-success-aa mb-3">
        <div className="card-header">Preparation Instructions</div>
        <div className="card-body text-success">
          <ol>
            {preparationInstructions.map((instruction:any, index:any) => (
              <li key={index}>{instruction}</li>
            ))}
          </ol>
        </div>
      </div>
    </div>
  );
}

//   return (
//     <div className="recipeResult">
//       <h1>Hooray!!</h1>
//       <p>How beautiful! We created a recipe for you from the ingredients you have at home!</p>
//       <div className="card border-success mb-3"></div>
//       <div className="card-header">The Products</div>
//         <div className="card-body text-success">
//             <ul>
//               {recipe.slice(0, -1).map((ingredient: any, index: any) => (
//                 <li key={index}>{ingredient.quantity} {ingredient.product}</li>
//               ))}
//             </ul>
//         </div>
//         <div className="card-header">Preparation Instructions</div>
//         {/* <h2>Preparation Instructions</h2> */}
//         <p className="card-text">
//           <ol>
//             {preparationInstructions.map((instruction:any, index:any) => (
//               <li key={index}>{instruction}</li>
//             ))}
//           </ol>
//           </p>
//       </div>
//       </div>
//   );
// }

export default RecipeResult;
