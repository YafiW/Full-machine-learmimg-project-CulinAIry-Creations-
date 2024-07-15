import React, { FC, useEffect, useState } from 'react';
import './vegetables.scss';
// import artichoke from '../../images/artichoke.jpg';
// import carrot from '../../images/carrot.jpg'
// import asparagus from '../../images/asparagus.jpg'
// import beet from '../../images/beet.webp'
// import broccoli from '../../images/broccoli.webp'
// import cauliflower from '../../images/cauliflower.webp'
// import celery_leaves from '../../images/celery_leaves.webp'
// import chestnut_pupmkin from '../../images/chestnut_pumpkin.webp'
// import coriander from '../../images/coriander.webp'
// import cucumber from '../../images/cucumber.jpg'
// import dill from '../../images/dill.webp'
// import eggplant from '../../images/eggplant.webp'
// import garlic from '../../images/garlic.webp'
// import ginger from '../../images/ginger.webp'
// import green_oninon from '../../images/green_onion.webp'
// import green_peper from '../../images/green_peper.webp'
// import guard from '../../images/guard.webp'
// import head_celery from '../../images/head_celery.webp'
// import hot_peper from '../../images/hot_peper.webp'
// import kolorbi from '../../images/kolorbi.webp'
// import leeks from '../../images/leeks.webp'
// import lettuce from '../../images/lettuce.webp'
// import mushrooms from '../../images/mushrooms.webp'
// import nana from '../../images/nana.webp'
// import onion from '../../../../images/'
import RecipesService from '../../servises/recipes.servises'
// import V_gif from '../../gifs/V.gif'
import V_image from '../../gifs/check (1).png'
import { useDispatch, useSelector } from 'react-redux';
import { addIngredient, removeIngredient } from '../../redux/arrIngredientsSlice';
import axios from 'axios';
import ingredientsService from '../../servises/ingredients.service';

interface VegetablesProps { }

const Vegetables: FC<VegetablesProps> = () => {
  const [vegetables, setVegetables] = useState<any[]>([]);
  // const [images, setImages] = useState<any[]>([{ url: artichoke, name: "artichoke" }, { url: carrot, name: "carrot" },
  // { url: asparagus, name: 'asparagus' }, { url: beet, name: 'beet' }, { url: broccoli, name: 'broccoli' }, { url: cauliflower, name: 'cauliflower' },
  // { url: celery_leaves, name: 'celery_leaves' }, { url: chestnut_pupmkin, name: 'chestnut_pupmkin' }, { url: coriander, name: 'coriander' },
  // { url: cucumber, name: 'cucumber' }, { url: dill, name: 'dill' }, { url: eggplant, name: 'eggplant' }, { url: garlic, name: 'garlic' },
  // { url: ginger, name: 'ginger' }, { url: green_oninon, name: 'green_oninon' }, { url: green_peper, name: 'green_peper' },
  // { url: guard, name: 'guard' }, { url: head_celery, name: 'head_celery' }, { url: hot_peper, name: 'hot_peper' }, { url: kolorbi, name: 'kolorbi' },
  // { url: leeks, name: 'leeks' }, { url: lettuce, name: 'lettuce' }, { url: mushrooms, name: 'mushrooms' }, { url: nana, name: 'nana' },
  // { url: onion, name: 'onion' }]);
  const dispatch = useDispatch();
  const [selectedIngredients, setSelectedIngredients] = useState<any[]>([]);
  const arrIngredients = useSelector((state: any) => state.arrIngredients.arrIngredients);
  const [recipe, setRecipe] = useState<any>();
  useEffect(() => {
    //mySqL פה צריך להיות הטעינה של התמונה מהשרת שעובר דרך 
    const getVegetablesData = async () => {
      
      ingredientsService.getVegetables().then((ingredients: any) => {
        setVegetables(ingredients.data);
        console.log(vegetables);
      })
    }
    getVegetablesData();
  }, []);
  //הפונקציה בודקת האם המוצר שנלחץ כבר קיים במערך, 
  //במידה ולא, היא מוסיפה אותו למערך המוצרים הנבחרים, אחרת היא מסירה אותו מהמערך
  const handleClick = (name: any) => {
    const index = arrIngredients.findIndex((ingredient: any) => ingredient == name);
    if (index !== -1) {
      dispatch(removeIngredient({ ingredient: name }));
    } else {
      dispatch(addIngredient({ ingredient: name }));
    }
  }
  // const getVegetablesData = async () => {
  //   ingredientsService.getVegetables().then((ingredients:any)=>{
  //     setVegetables(ingredients.data);
  //   })
  // }
  //הפונקציה שולחת לשרת את המערך עם המוצרים שנבחרו
  const sendToServer = async () => {
    RecipesService.getRecipe(arrIngredients).then((recipe: any) => {
      setRecipe(recipe.data)
      console.log(recipe.data)
    }, (error: any) => {
      console.log(error)
    })
  }

  return (
    <div className="vegetables">
      <div>
        {vegetables.map((image, index) => {
          const periodIndex = image.indexOf('.');
          let imageName = periodIndex !== -1 ? image.substring(0, periodIndex) : image;
          imageName = imageName.replace(/_/g, ' ')
          return (
            <button
              key={index}
              id={`button-${imageName}`}
              onClick={() => handleClick(imageName)}
              className={`vegetableImage ${arrIngredients.includes(imageName) ? 'overlay' : ''}`}
            >
              {arrIngredients.includes(imageName) && (
                <img className="gifOverlay" src={V_image} alt="GIF" />
              )}

              <h5>{imageName}</h5>
              <img
                className="vegetableImage"
                src={`http://localhost:5000/ingredients/vegetable/${image}`}
                alt={`Vegetable ${imageName}`}
                width="150px"
                height="150px"
              />
            </button>
          );
        })}
      </div>
      {/* <button className="btn btn-primary btn-lg" onClick={sendToServer}>Finish</button> */}
    </div>
  );
  // return (
  //   <div className="vegetables">
  //     <div>
  //       {vegetables ? (
  //         vegetables.map((image: any) => (
  //           <button
  //             key={image.name}
  //             id={`button-${image.name}`}
  //             onClick={() => handleClick(image.name)}
  //             className={`vegetableImage ${arrIngredients.includes(image.name) ? 'overlay' : ''}`}
  //           >
  //             <h5>{image.name}</h5>
  //             {arrIngredients.includes(image.name) && (
  //               <img className="gifOverlay" src={V_gif} alt="GIF" />
  //             )}
  //             <img className="vegetableImage" src={image.src} width="150px" height="150px" />
  //           </button>
  //         ))
  //       ) : null}
  //     </div>
  //     {/* <button className="btn btn-primary btn-lg" onClick={sendToServer}>Finish</button> */}
  //   </div>
  // );

}

export default Vegetables;
