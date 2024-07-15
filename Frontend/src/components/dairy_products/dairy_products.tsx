import React, { FC, useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import ingredientsService from '../../servises/ingredients.service';
import { addIngredient, removeIngredient } from '../../redux/arrIngredientsSlice';
import V_image from '../../gifs/check (1).png'
import './dairy_products.scss';

interface DairyProductsProps {}

const DairyProducts: FC<DairyProductsProps> = () => {
  const [dairy_products, setdairy_products] = useState<any[]>([]);
  const dispatch = useDispatch();
  const arrIngredients = useSelector((state: any) => state.arrIngredients.arrIngredients);
  useEffect(() => {
    //mySqL פה צריך להיות הטעינה של התמונה מהשרת שעובר דרך 
    const getVegetablesData = async () => {
      ingredientsService.getDairyProducts().then((ingredients:any)=>{
        setdairy_products(ingredients.data);
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
    <div className="dairy_products">
      <div>
        {dairy_products.map((image, index) => {
          const periodIndex = image.indexOf('.');
          let imageName = periodIndex !== -1 ? image.substring(0, periodIndex) : image;
          imageName = imageName.replace(/_/g, ' ');

          return (
            <button
              key={index}
              id={`button-${imageName}`}
              onClick={() => handleClick(imageName)}
              className={`dairy_productsImage ${arrIngredients.includes(imageName) ? 'overlay' : ''}`}
            >
              <h5>{imageName}</h5>
              {arrIngredients.includes(imageName) && (
                <img className="gifOverlay" src={V_image} alt="GIF" />
              )}
              <img
                className="dairy_productsImage"
                src={`http://localhost:5000/ingredients/dairy_products/${image}`}
                alt={`dairy_products ${imageName}`}
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
}

export default DairyProducts;
