import React, { FC, useEffect, useState } from 'react';
import './Fruits.scss';
import { useDispatch, useSelector } from 'react-redux';
import ingredientsService from '../../servises/ingredients.service';
import { addIngredient, removeIngredient } from '../../redux/arrIngredientsSlice';
import V_image from '../../gifs/check (1).png'

interface FruitsProps {}

const Fruits: FC<FruitsProps> = () => {
  const [fruits, setFruits] = useState<any[]>([]);
  const dispatch = useDispatch();
  const arrIngredients = useSelector((state: any) => state.arrIngredients.arrIngredients);
  useEffect(() => {
    debugger
    //mySqL פה צריך להיות הטעינה של התמונה מהשרת שעובר דרך 
    const getVegetablesData = async () => {
      debugger
      ingredientsService.getFruits().then((ingredients:any)=>{
        setFruits(ingredients.data);
      })
    }
    getVegetablesData();
  }, []);
  const handleClick = (name: any) => {
    const index = arrIngredients.findIndex((ingredient:any)=>ingredient==name);
    if (index !== -1) {
      dispatch(removeIngredient({ ingredient: name }));
    } else {
      dispatch(addIngredient({ ingredient: name }));
    }
  }

  return (
    <div className="fruits">
      <div>
        {fruits.map((image, index) => {
          const periodIndex = image.indexOf('.');
          let imageName = periodIndex !== -1 ? image.substring(0, periodIndex) : image;
          imageName = imageName.replace(/_/g, ' ');

          return (
            <button
              key={index}
              id={`button-${imageName}`}
              onClick={() => handleClick(imageName)}
              className={`fruitImage ${arrIngredients.includes(imageName) ? 'overlay' : ''}`}
            >
              <h5>{imageName}</h5>
              {arrIngredients.includes(imageName) && (
                <img className="gifOverlay" src={V_image} alt="GIF" />
              )}
              <img
                className="fruitImage"
                src={`http://localhost:5000/ingredients/fruits/${image}`}
                alt={`Fruits ${imageName}`}
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
};

export default Fruits;
