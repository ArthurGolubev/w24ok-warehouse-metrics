import React from 'react'
import { SevenDays } from './plots/purchases/SevenDays'
import { MonthToMonth } from './plots/purchases/MonthToMonth'
import { InOutUsers } from './plots/users/InOutUsers'
import { Top } from './plots/users/Top'
import { CardTop } from './plots/users/CardTop'

export const Main = () => {
    return <div className='card-body'>
        <div className='row justify-content-center'>
            <div className='col-sm-auto col-lg-12 col-xl-12 col-xxl-12'>
                <SevenDays />
            </div>
        </div>
        <hr/>
        <div className='row justify-content-center'>
            <div className='col-sm-auto col-lg-12 col-xl-12 col-xxl-12'>
                <MonthToMonth />
            </div>
        </div>
        <hr/>
        <div className='row justify-content-center'>
            <div className='col-sm-auto col-lg-12 col-xl-12 col-xxl-12'>
                <InOutUsers />
            </div>
        </div>
        <hr/>
        <div className='row justify-content-center'>
            <div className='col-sm-4 col-4'>
                <CardTop />
            </div>
        </div>
        <div className='row justify-content-evenly'>
            <div className='col-sm-auto col-lg-5 col-xl-5 col-xxl-5'>
                <Top subject='users' />
            </div>
            <div className='col-sm-auto col-lg-5 col-xl-5 col-xxl-5'>
                <Top subject='orgs' />
            </div>
        </div>
    </div>
}