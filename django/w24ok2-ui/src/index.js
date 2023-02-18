import React from 'react'
import { ApolloClient, ApolloProvider, createHttpLink } from '@apollo/client'
import { setContext } from '@apollo/client/link/context'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import ReactDOM from 'react-dom'

import { cache } from './cache/cache'
import { App } from './App'


const httpLink = createHttpLink({
    uri: 'graphql/'
})

const authLink = setContext((_, { headers }) => {
    const token = localStorage.getItem('w24ok_token')  
    console.log(token)
    return {
        headers: {
            ...headers,
            authorization: token ? `JWT ${token}` : ''
        }
    }
})

const client = new ApolloClient({
    link: authLink.concat(httpLink),
    cache: cache
})

ReactDOM.render(
    <ApolloProvider client={client}>
        <App />
    </ApolloProvider>,
    document.querySelector('#root')
)