import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import SignUp from './components/sign-up/sign-up';
import LogIn from './components/log-in/log-in';
import HomePage from './components/homePage/homePage';
import { Route, Routes, useNavigate } from 'react-router-dom';
import Vegetables from './components/vegetables/vegetables';
import { Provider, useSelector } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';
import arrIngredientsReducer, { selectArrIngredients } from './redux/arrIngredientsSlice';
import Fruits from './components/Fruits/Fruits';
import DairyProducts from './components/dairy_products/dairy_products';
import Fish from './components/fish/fish';
import MeatAndChicken from './components/meat_and_chicken/meat_and_chicken';
import sh from './images/shopping-bag.png'
import SendingTheIngredients from './components/Sending_the_ingredients/Sending_the_ingredients';
import DryProducts from './components/dry_products/dry_products';
import RecipeResult from './components/recipeResult/recipeResult';
const myStore = configureStore({
  reducer: {
    arrIngredients: arrIngredientsReducer,
  },
});

const IngredientsCart = () => {
  const [showDropdown, setShowDropdown] = useState(false);
  const ingredients = useSelector(selectArrIngredients);

  const handleMouseEnter = () => setShowDropdown(true);
  const handleMouseLeave = () => setShowDropdown(false);

  return (
    <li onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
      <button className="nav-link align-middle px-0">
        {/* <img src={sh} alt="Shopping Cart" width="30px" height='30px'/> */}
        <i className="fs-4 bi-house"></i>
        <span className="ms-1 d-none d-sm-inline ingredient">Ingredients cart</span>
      </button>
      {showDropdown && (
        <div className="dropdown-content">
          <ul>
            {ingredients.map((ingredient: any, index: any) => (
              <li key={index}>{ingredient}</li>
            ))}
          </ul>
        </div>
      )}
    </li>
  );
};

const App = () => {
  const navigate = useNavigate();
  const [selectedCategory, setSelectedCategory] = useState('');

  const handleCategoryClick = (category: any) => {
    setSelectedCategory(category);
    navigate(`/${category}`);
  };
  const [isLoadder,setIsLoadder] = useState<boolean>(false)
  const handleClickLoadder= ()=>{
    setIsLoadder(true)
  }
  return (
    <Provider store={myStore}>
      <div className="container-fluid">
        <div className="row flex-nowrap">
          <div className="col-auto col-md-3 col-xl-2 px-sm-2 px-0 ">
            <div className="d-flex flex-column align-items-center align-items-sm-start px-3 pt-2 text-white min-vh-100">
              <ul className="nav nav-pills flex-column mb-sm-auto mb-0 align-items-center align-items-sm-start" id="menu">
                <li className="nav-item">
                  <button className="nav-link align-middle px-0" onClick={() => handleCategoryClick('')}>
                    <i className="fs-4 bi-house"></i> <span className="ms-1 d-none d-sm-inline">Home</span>
                  </button>
                </li>
                <li>
                  <button className="nav-link align-middle px-0" onClick={() => handleCategoryClick('vegetables')}>
                    <i className="fs-4 bi-house"></i> <span className="ms-1 d-none d-sm-inline">Vegetables</span>
                  </button>
                </li>
                <li>
                  <button className="nav-link align-middle px-0" onClick={() => handleCategoryClick('meats_and_chickens')}>
                    <i className="fs-4 bi-house"></i> <span className="ms-1 d-none d-sm-inline">Meat & Chickens</span>
                  </button>
                </li>
                <li>
                  <button className="nav-link align-middle px-0" onClick={() => handleCategoryClick('fruits')}>
                    <i className="fs-4 bi-house"></i> <span className="ms-1 d-none d-sm-inline">Fruits</span>
                  </button>
                </li>
                <li>
                  <button className="nav-link align-middle px-0" onClick={() => handleCategoryClick('dry_products')}>
                    <i className="fs-4 bi-house"></i> <span className="ms-1 d-none d-sm-inline">Dry products</span>
                  </button>
                </li>
                <li>
                  <button className="nav-link align-middle px-0" onClick={() => handleCategoryClick('dairy_products')}>
                    <i className="fs-4 bi-house"></i> <span className="ms-1 d-none d-sm-inline">Dairy products</span>
                  </button>
                </li>
                <li>
                  <button className="nav-link align-middle px-0" onClick={() => handleCategoryClick('fish')}>
                    <i className="fs-4 bi-house"></i> <span className="ms-1 d-none d-sm-inline">Fish</span>
                  </button>
                  <div className="btn-sending">
                  <span className="ms-1 d-none d-sm-inline"><SendingTheIngredients></SendingTheIngredients></span>
                    </div>
                  
                </li>
                
                <IngredientsCart />
              </ul>
              <hr />
            </div>
          </div>
          <div className="col py-3">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/vegetables" element={<Vegetables />} />
              <Route path="/login" element={<LogIn />} />
              <Route path="/signup" element={<SignUp />} />
              <Route path="/fruits" element={<Fruits />} />
              <Route path="/dairy_products" element={<DairyProducts />} />
              <Route path="/dry_products" element={<DryProducts/>} />
              <Route path="/fish" element={<Fish />} />
              <Route path="/meats_and_chickens" element={<MeatAndChicken />} />
              <Route path="/recipeResult" element={<RecipeResult />} />
            </Routes>
          </div>
        </div>
      </div>
    </Provider>
  );
};
export type RootState = ReturnType<typeof myStore.getState>;
export type AppDispatch = typeof myStore.dispatch;
export default App;
