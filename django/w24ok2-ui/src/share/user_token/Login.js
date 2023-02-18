import React from 'react'
import { Link } from 'react-router-dom'
import { Redirect } from 'react-router'
import { useMutation } from '@apollo/client'
import { GET_TOKEN } from '../requests/mutation'

export const Login = ({location}) => {
    // console.log('c ->', location.state?.from)

    const [getToken, {data, loading, error}] = useMutation(GET_TOKEN)

    const getTokenHandler = () => {
        let username = document.querySelector("#form-username")
        let password = document.querySelector("#form-password")
        getToken({variables: { username: username.value, password: password.value}})
        // console.log('getTokenData ->', data)
    }

    if(data?.tokenAuth){
        // console.log(data)
        localStorage.setItem('w24ok_token', data?.tokenAuth.token)
        return <Redirect to='/'/>
    }

    return <div className='card-body'>
        <div className="row justify-content-center align-items-center" style={{height: '80vh'}}>
            <div className="col-xl-4 col-sm-auto">
                <div className="card">
                    <div className="card-body">
                        <form>
                            <div className="mb-3">
                                <label htmlFor="form-username" className="form-label">Enter login:</label>
                                <input type="text" className="form-control" id="form-username" />
                            </div>
                            <div className="mb-3">
                                <label htmlFor="form-password" className="form-label">Enter password:</label>
                                <input type="password" className="form-control" id="form-password" />
                            </div>
                        </form>
                        <div className="row justify-content-center">
                            {
                                loading ? <div className="spinner-border" /> : 
                                <div className="d-grid gap-2 col-10 mx-auto">
                                    <button onClick={()=>getTokenHandler()} className="btn btn-sm btn-primary">Авторизироваться</button>
                                    <Link className="btn btn-sm btn-primary disabled" to='/registration'>Создать пользователя</Link>
                                </div>
                            }
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
}