import React, { FC, useState } from 'react';
import './log-in.scss';
import * as Yup from 'yup'
import { useFormik } from 'formik';
import 'bootstrap/dist/css/bootstrap.min.css';
import userService from '../../servises/user.service';
import { Outlet, useNavigate } from 'react-router-dom';

interface LogInProps {}

const LogIn: FC<LogInProps> = () => {
  const navigate=useNavigate()
  const [isValidUser,setIsValidUser]=useState<boolean>(true);
  const checkIsValidUser = (user:any) =>{
    //הפונקציה מקבלת את הנתונים של המשתמש ובודקת בשרת האם הוא אכן קיים
    userService.getUser(user).then((result:any) => {
      console.log(result.data)
      if(result.data===true){
        navigate('/Home-page')
      }
      else{
        setIsValidUser(false)
      }
    }, (error:any) => {
      console.log(error)
    })
  }
  const userform = useFormik({
    initialValues: {
      email: "",
      password: "",
    },
    onSubmit: (valueForm: any, { resetForm }) => {
      let user = {
        email:valueForm.email,
        password:valueForm.password
      }
        
      checkIsValidUser(user);

      resetForm({
        values: {
          email: '',
          password: '',
        },
      });
    },
    validationSchema: Yup.object().shape({
      email: Yup.string().required().email('Invalid email address'),
      password: Yup.string().required().min(2, 'Password must be at least 2 characters long'),
    })
  })

  return <section className="vh-100">
    <div className="container h-100">
      <div className="row d-flex justify-content-center align-items-center h-100">
        <div className="col-lg-12 col-xl-11">
          <div className="card text-black">
            <div className="card-body p-md-5">
              <div className="row justify-content-center">
                <div className="col-md-10 col-lg-6 col-xl-5 order-2 order-lg-1">
                  <p className="text-center h1 fw-bold mb-5 mx-1 mx-md-4 mt-4">Log in</p>
                  <form className="mx-1 mx-md-4" onSubmit={userform.handleSubmit}>
                    <div className="d-flex flex-row align-items-center mb-4">
                      <i className="fas fa-envelope fa-lg me-3 fa-fw"></i>
                      <div className="form-outline flex-fill mb-0">
                        <label className="form-label" htmlFor="form3Example3c">Your Email</label>
                        <input value={userform.values.email} onChange={userform.handleChange} className={userform.errors.email ? 'form-control is-invalid' : 'form-control'} type="email" id="email" />
                        {typeof userform.errors.email === 'string' ? (
                          <small>{userform.errors.email}</small>
                        ) : null}
                      </div>
                    </div>
                    <div className="d-flex flex-row align-items-center mb-4">
                      <i className="fas fa-lock fa-lg me-3 fa-fw"></i>
                      <div className="form-outline flex-fill mb-0">
                        <label className="form-label" htmlFor="form3Example4c">Password</label>
                        <input value={userform.values.password} onChange={userform.handleChange} className={userform.errors.password ? 'form-control is-invalid' : 'form-control'} type="password" id="password" />
                        {typeof userform.errors.password === 'string' ? (
                          <small>{userform.errors.password}</small>
                        ) : null}
                      </div>
                    </div>
                    <a href="#">Don't have an account sign up</a>
                    <div className="d-flex justify-content-center mx-4 mb-3 mb-lg-4">
                      <button type="submit" onClick ={checkIsValidUser} className="btn btn-primary btn-lg">Connect</button>
                    </div>
                      {!isValidUser?
                      <span>User not found!</span>
                      :null}
                  </form>
                </div>
                <div className="col-md-10 col-lg-6 col-xl-7 d-flex align-items-center order-1 order-lg-2">
                  <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-registration/draw1.webp"
                    className="img-fluid" alt="Sample image" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <Outlet></Outlet>

    </div>
  </section>
  
}

export default LogIn;
