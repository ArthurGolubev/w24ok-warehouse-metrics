import { gql } from '@apollo/client'

export const SEVEN_DAYS = gql`
    query seven_days_query($warh: String!){
        sevenDays(warh: $warh){
            date
            paid
            transactions
            uniqueUsers
        }
    }
`

export const MONTH_TO_MONTH = gql`
    query month_to_month_query($warh: String!){
        monthToMonth(warh: $warh){
            date
            body{
                date
                paid
                transactions
                uniqueUsers
            }
        }
    }
`
export const IN_OUT_USERS = gql`
    query in_out_users_query($warh: String!){
        inOutUsers(warh: $warh){
            date
            waterfallStepChange
            incoming
            departed
        }
    }
`

export const WARH_LIST = gql`
    query warh_list_query{
        warhList{
            id
            shortName
            name
        }
    }
`
export const TOP_USERS = gql`
    query top_users_query($warh: String!, $rangeTop: String!){
        topUsers(warh: $warh, rangeTop: $rangeTop){
            user_Username
            id_Count
        }
    }
`

export const TOP_ORGS = gql`
    query top_orgs_query($warh: String!, $rangeTop: String!){
        topOrgs(warh: $warh, rangeTop: $rangeTop){
            org_Username
            id_Count
        }
    }
`