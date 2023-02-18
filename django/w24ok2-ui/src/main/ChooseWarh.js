import { useQuery } from '@apollo/client'
import React from 'react'
import { Link } from 'react-router-dom'
import { WARH_LIST } from './requests/query'


export const ChooseWarh = () => {
    const {data, loading, error} = useQuery(WARH_LIST, {fetchPolicy: 'network-only'})

    if(data && !loading){
        return <div className='row justify-content-center align-items-center' style={{height: '80vh'}}>
            <div className='col-auto'>
                <div className='list-group'>
                    {
                        data.warhList?.map(item => <Link
                            key={item.id}
                            className="list-group-item list-group-item-action text-center"
                            to={'warh/'+ item.shortName+'/main'}>{item.name}</Link>)
                    }
                </div>       
            </div>
        </div>
    }
    return null
}