import React from 'react'
import { useReactiveVar } from '@apollo/client'
import { selectTopRange } from '../../../cache/main/rVar'


export const CardTop = () => {

    const selected = useReactiveVar(selectTopRange)

    return <div className="alert alert-info" role="alert">
        <div className='row justify-content-center'>
            <div className='col-5 mx-1 text-center'>
                <input
                    type="radio"
                    checked={selected == 'month'}
                    value="month"
                    className="form-check-input"
                    onChange={()=>selectTopRange('month')}
                    id="select-month"/>
                <label className="form-check-label mx-2" htmlFor="select-month">Месяц</label>
            </div>
            <div className='col-5 mx-1 text-center'>
                <input
                    type="radio"
                    checked={selected == 'year'}
                    value="year"
                    className="form-check-input"
                    onChange={()=>selectTopRange('year')}
                    id="select-year"/>
                <label className="form-check-label mx-2" htmlFor="select-year">Год</label>
            </div>
        </div>
    </div>
    // return <div className="card">
    //     <div className='col-auto my-1'>
    //             <input
    //                 type="radio"
    //                 checked={selected == 'month'}
    //                 value="month"
    //                 className="form-check-input"
    //                 onChange={()=>selectTopRange('month')}
    //                 id="select-month"/>
    //             <label className="form-check-label" htmlFor="select-month">За месяц</label>
    //         </div>
    //         <div className='col-auto my-1'>
    //             <input
    //                 type="radio"
    //                 checked={selected == 'year'}
    //                 value="year"
    //                 className="form-check-input"
    //                 onChange={()=>selectTopRange('year')}
    //                 id="select-year"/>
    //             <label className="form-check-label" htmlFor="select-year">За год</label>
    //         </div>
    //         {[10, 15, 30, 50, 100, data?.[subject == 'users' ? 'topUsers': 'topOrgs'].length].map((item, key) => {
    //         return <div key={key} className="form-check form-check-inline">
    //         <input
    //         className="form-check-input"
    //         type="radio"
    //         value={item}
    //         checked={count == item}
    //         id={"top-" + item}
    //         onChange={(e) => topQuantity({...topQuantity(), [subject]: parseInt(e.target.value)})}/>
    //         <label className="form-check-label" htmlFor={"top-" + item}>{item}</label>
    //     </div>
    //     })}
    // </div>
}