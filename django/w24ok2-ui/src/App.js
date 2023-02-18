import React from 'react'
import { useQuery } from '@apollo/client'
import { HashRouter, Route, Switch, Link, Redirect } from 'react-router-dom'
import { ChooseWarh } from './main/ChooseWarh'
import { Main } from './main/Main'
import { NavBar1 } from './share/Navbar/NavBar1'
import { Login } from './share/user_token/Login'
import { TOKEN_CHECK } from './share/requests/query'
import { PermissionDenied } from './share/Errors/PermissionDenied'
import { Spiner } from './share/Spiner'
import { ErrorMessage } from './share/Errors/ErrorMessage'
import { Prolongation } from './additionally/Prolongation'

export const App = () => {
    const { data, loading, error } = useQuery(TOKEN_CHECK, {fetchPolicy: 'network-only'})
    if(loading) return <Spiner />

    return <HashRouter>
        <NavBar1 />
        {
            error && (
                error.graphQLErrors.find(
                    item => item.message == 'Not logged in!' || item.message == 'Signature has expired'
                    ) ?
                        <Redirect to={{ pathname: '/login', state: { from: '/123'} }}/>
                    :
                        <ErrorMessage error={error} />
            )
        }
        <Switch>
            <Route exact path='/' component={ChooseWarh} />
            <Route path='/warh/:slug/main' component={Main} />
            <Route path='/warh/:slug/prolongation' component={Prolongation} />
            {/* -------------------------------------------Errors-handling-Start------------------------------------------ */}
            <Route path='/login' component={Login} />
            <Route path='/permission-denied' component={PermissionDenied} />

            {/* -------------------------------------------Errors-handling-End------------------------------------------ */}
        </Switch>
    </HashRouter>
}