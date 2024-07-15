import React, { FC } from 'react';
import './Loadder.scss';
import cooking from '../../gifs/cooking.gif'
interface LoadderProps { }

const Loadder: FC<LoadderProps> = () => (
  <div className="Loadder-overlay">
    <div className="Loadder-content">
      <p className="Loadder-caption">How fun! <br></br>We are preparing a recipe for you right now, it's already coming out of the oven!</p>
      <img className="gifCooking" src={cooking} alt="GIF" />
    </div>
  </div>
);

export default Loadder;
