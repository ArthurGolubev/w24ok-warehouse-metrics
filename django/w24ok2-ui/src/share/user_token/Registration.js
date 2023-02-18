import React from 'react'
import { useQuery } from '@apollo/client'
import { Redirect } from 'react-router-dom'
import { useMutation } from '@apollo/client'

import { VALID_REG_FORM } from '../requests/query'
import { validRegForm } from '../../cache/login_reg/rVar'
import { CREATE_USER } from '../requests/mutation'

export const Registration = () => {


    const [createUser, {data, loading, error}] = useMutation(CREATE_USER)
    const {data: sub_valid_reg_form} = useQuery(VALID_REG_FORM)

    const createUserHandler = () => {
        let validPass = document.querySelector("#registration-password-1").value == document.querySelector("#registration-password-2").value
        if(validPass){
            createUser({variables: {
                username: document.querySelector("#registration-username").value,
                firstName: document.querySelector("#registration-first-name").value,
                lastName: document.querySelector("#registration-last-name").value,
                email: document.querySelector("#registration-email").value,
                password: document.querySelector("#registration-password-1").value
            }})
        } else {
            validRegForm({
                password: "form-control is-invalid",
            })
        }
    }

    if(data?.createUser){
        return <Redirect to='/login'/>
    }

    return <div className="row justify-content-center align-items-center" style={{height: '100vh'}}>
        <div className="col-4">
            <div className="card">
                <div className="card-body">
                    
                    <form>
                        <div className="mb-3">
                            <label htmlFor="registration-username" className="form-label">Username:</label>
                            <input type="text" className="form-control" id="registration-username" />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="registration-first-name" className="form-label">First name:</label>
                            <input type="text" className="form-control" id="registration-first-name" />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="registration-last-name" className="form-label">Last name:</label>
                            <input type="text" className="form-control" id="registration-last-name" />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="registration-email" className="form-label">Email name:</label>
                            <input type="text" className="form-control" id="registration-email" />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="registration-password-1" className="form-label">Enter password:</label>
                            <input type="password" className={sub_valid_reg_form.validRegForm.password} id="registration-password-1" />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="registration-password-2" className="form-label">Repeat password:</label>
                            <input type="password" className={sub_valid_reg_form.validRegForm.password} id="registration-password-2"/>
                        </div>
                    </form>
                    <div className="row justify-content-center">
                        <div className="btn-group">
                            {
                                loading ? <div className="spinner-border" /> :
                                <button onClick={()=>createUserHandler()} className="btn btn-primary">Создать пользователя</button>
                            }
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
}