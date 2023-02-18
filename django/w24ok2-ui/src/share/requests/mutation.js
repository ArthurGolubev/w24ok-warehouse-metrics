import { gql } from '@apollo/client'


export const GET_TOKEN = gql`
    mutation get_token_mutation($username: String!, $password: String!){
        tokenAuth(username: $username, password: $password){
            token
            payload
            refreshExpiresIn
        }
    }
`

export const CREATE_USER = gql`
    mutation create_user_mutation(
        $username: String!,
        $firstName: String!,
        $lastName: String!,
        $email: String!,
        $password: String!
        ){
            createUser(
                username: $username,
                firstName: $firstName,
                lastName: $lastName,
                email: $email,
                password: $password){
                    createdUser{
                        id
                    }
                }
        }
`