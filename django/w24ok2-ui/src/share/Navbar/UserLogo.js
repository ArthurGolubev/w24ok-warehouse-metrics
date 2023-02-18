import React from 'react'

export const UserLogo = ({data}) => {
    return <div className="card p-2 text-center">{data?.me.firstName} {data?.me.lastName}</div>
}