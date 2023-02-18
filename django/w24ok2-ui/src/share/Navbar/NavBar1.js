import { useQuery, useApolloClient } from '@apollo/client'
import React from 'react'
import { Switch, Route, useParams, NavLink } from 'react-router-dom'
import { Link } from 'react-router-dom'
import { WARH_LIST } from '../../main/requests/query'
import { ErrorMessage } from '../Errors/ErrorMessage'
import { UserLogo } from './UserLogo'


export const NavBar1 = ({data}) => {
    const client = useApolloClient()
    const {data: warh, loading, error} = useQuery(WARH_LIST, {fetchPolicy: 'cache-first'})
    // console.log('warh form navbar->', warh)

    const logout = () => {
        localStorage.removeItem('w24ok_token')
        client.resetStore()
    }

    return <nav className="navbar navbar-expand-lg navbar-light bg-light shadow-sm">
        <div className="container-fluid">
            <div className="col-2">
            <Link className="navbar-brand position-relative" to='/'>
                w24ok2
                <span className=" fw-light position-absolute top-0 start-150 badge rounded-pill bg-success">
                    {/* v1.8.0-beta.4 */}
                    v1.8.1
                </span>
            </Link>
            <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span className="navbar-toggler-icon"></span>
            </button>
            </div>
                    <div className="collapse navbar-collapse" id="navbarSupportedContent">
                        <ul className='navbar-nav'>
                            {
                                warh?.warhList &&
                                <li className="nav-item dropdown">
                                    <a className="nav-link dropdown-toggle" href="#" id="navbarDarkDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                        Склады
                                    </a>
                                        <ul className="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                                            {
                                                warh.warhList.map(item => {
                                                    return <li key={item.id} className="nav-item">
                                                        <NavLink
                                                            className="dropdown-item"
                                                            activeClassName="selected"
                                                            activeStyle={{
                                                                fontWeight: "bold",
                                                                color: "red"
                                                            }}
                                                            to={'/warh/'+ item.shortName+'/main'}>
                                                                {item.name}
                                                            </NavLink>
                                                    </li>
                                                })
                                            }
                                        </ul>
                                    </li>
                            }
                            <li className="nav-item">
                                <Link onClick={()=>logout()} className="nav-link" to="/login">Logout</Link>
                            </li>
                            </ul>
                        <div className="d-flex justify-content-between">
                            <div className="col-auto">
                                <Switch>
                                    {/* <Route path='/books/book/:slug' component={ErrorMessage} /> */}
                                    {/* <Route path='/schedule'         component={ScheduleNav}/> */}
                                </Switch>
                            </div>        
                        </div>
                        {/* <UserLogo data={data} /> */}
                    </div>
        </div>
    </nav>
}