import React, { FC ,useState} from 'react';
import './sign-up.scss';
import 'bootstrap/dist/css/bootstrap.min.css';
import * as Yup from 'yup'
import { Outlet, useNavigate } from 'react-router-dom';
import { useFormik } from 'formik';
import usersModel from '../../models/userModel';
import userService from '../../servises/user.service';
import { Formik, Form, Field, ErrorMessage } from 'formik';

interface SignUpProps { }

const SignUp: FC<SignUpProps> = () => {
  const navigate=useNavigate()
  const [isValidUser,setIsValidUser]=useState<boolean>(true);
  const addUser = (userToAdd: usersModel) => {
    userService.createUser(userToAdd).then((result:any) => {
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

    //לכתוב את הפונקציה ששולחת לשרת את הפרטים של המשתמש החדש שנרשם
  }
  const userform = useFormik({
    initialValues: {
      name: "",
      email: "",
      password: "",
      password_to_check: "",
      statements: false
    },
    onSubmit: (valueForm: any, { resetForm }) => {
      let userToAdd = new usersModel(
        valueForm.name,
        valueForm.email,
        valueForm.password,
        valueForm.statements
      );
      addUser(userToAdd);

      resetForm({
        values: {
          name: '',
          email: '',
          password: '',
          password_to_check: '',
          statements: false,
        },
      });
    },
    validationSchema: Yup.object().shape({
      name: Yup.string().required().min(2, 'Name must be at least 2 characters long'),
      password: Yup.string().required('Password is required').matches(/^(?=.*[A-Za-z].*[A-Za-z])(?=.*\d).*$/, 'Password must contain at least 2 letters and a number').min(2, 'Password must be at least 2 characters long'),
      password_to_check: Yup.string().oneOf([Yup.ref('password')], 'Passwords must match'),
      email: Yup.string().required().email('Invalid email address'),
      statements: Yup.boolean().required()
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
                  <p className="text-center h1 fw-bold mb-5 mx-1 mx-md-4 mt-4">Sign up</p>
                  <form className="mx-1 mx-md-4" onSubmit={userform.handleSubmit}>
                    <div className="d-flex flex-row align-items-center mb-4">
                      <i className="fas fa-user fa-lg me-3 fa-fw"></i>
                      <div className="form-outline flex-fill mb-0">
                        <label className="form-label" htmlFor="form3Example1c">Your Name</label>
                        <input value={userform.values.name} onChange={userform.handleChange} type="text" id="name" className={userform.errors.name ? 'form-control is-invalid' : 'form-control'}/*className="form-control"*/ />
                        {typeof userform.errors.name === 'string' ? (
                          <small>{userform.errors.name}</small>
                        ) : null}
                      </div>
                    </div>
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
                    <div className="d-flex flex-row align-items-center mb-4">
                      <i className="fas fa-key fa-lg me-3 fa-fw"></i>
                      <div className="form-outline flex-fill mb-0">
                      <label className="form-label" htmlFor="form3Example4cd">Repeat your password</label>
                        <input value={userform.values.password_to_check} onChange={userform.handleChange} className={userform.errors.password_to_check ? 'form-control is-invalid' : 'form-control'} type="password" id="password_to_check" />
                        {typeof userform.errors.password_to_check === 'string' ? (
                          <small>{userform.errors.password_to_check}</small>
                        ) : null}
                      </div>
                    </div>
                    <div className="form-check d-flex justify-content-center mb-5">
                      <input onChange={userform.handleChange} checked={userform.values.statements} className="form-check-input me-2" type="checkbox" id="statements" />
                      <label className="form-check-label" htmlFor="form2Example3">
                        I agree all statements in <a href="#!">Terms of service</a>
                      </label>
                    </div>
                    <div className="d-flex justify-content-center mx-4 mb-3 mb-lg-4">
                      <button type="submit" className="btn btn-primary btn-lg">Register</button>
                    </div>
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
    </div>
  </section>
}

export default SignUp;
