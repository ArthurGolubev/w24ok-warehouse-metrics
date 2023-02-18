import { gql } from '@apollo/client'

export const TOKEN_CHECK = gql`
    query token_check_query{
        me{
            username
            firstName
            lastName
        }
    }
`

export const VALID_REG_FORM = gql`
    query valid_reg_form_query{
        validRegForm @client
    }
`

