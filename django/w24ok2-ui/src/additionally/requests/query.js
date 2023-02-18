import { gql } from '@apollo/client'

export const PROLONGATIONS = gql`
    query prolongations_query($warh: String!){
        prolongations(warh: $warh){
            
        }
    }
`