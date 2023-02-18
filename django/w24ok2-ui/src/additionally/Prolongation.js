import { useQuery } from '@apollo/client'
import React from 'react'


export const Prolongation = () => {

    const {data, loading, error} = useQuery()
    return <div>
        Prolongations
    </div>
}