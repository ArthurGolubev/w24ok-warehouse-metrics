import React from 'react'
import { useQuery, useReactiveVar } from '@apollo/client'
import { TOP_ORGS, TOP_USERS } from '../../requests/query';
import { useParams } from 'react-router';
import { topQuantity } from '../../../cache/main/rVar'
import { selectTopRange } from '../../../cache/main/rVar'

export const Top = ({subject}) => {
    const { slug } = useParams()
    const selected = useReactiveVar(selectTopRange)
    const { data, loading, error } = useQuery(subject == 'users' ? TOP_USERS : TOP_ORGS, {variables: {warh: slug, rangeTop: selected}})
    
    const count = useReactiveVar(topQuantity)[subject]
    // console.log('count ->', count)

    return <div className="text-center">
        <h5>Top-{count} {subject == 'users' ? 'участников' : 'организаторов'} за этот месяц</h5>
            
        <table className="table table-bordered table-sm table-hover">
            <thead>
                <tr>
                    <th>#</th>
                    <th>{subject == 'users' ? 'Пользователь' : 'Организатор'}</th>
                    <th>Закупок</th>
                </tr>
            </thead>
            <tbody>
                {
                    data?.[subject == 'users' ? 'topUsers': 'topOrgs'].slice(0, count).map((item, iter) => {
                        return <tr key={iter}>
                            <th scope="row">{iter+1}</th>
                            <td>{item[subject == 'users' ? 'user_Username': 'org_Username']}</td>
                            <td>{item['id_Count']}</td>
                        </tr>
                    })
                }
            </tbody>
        </table>
        {[30, 50, 100, data?.[subject == 'users' ? 'topUsers': 'topOrgs'].length].map((item, key) => {
            return <div key={key} className="form-check form-check-inline">
            <input
            className="form-check-input"
            type="radio"
            value={item}
            checked={count == item}
            id={"top-" + item}
            onChange={(e) => topQuantity({...topQuantity(), [subject]: parseInt(e.target.value)})}/>
            <label className="form-check-label" htmlFor={"top-" + item}>{item}</label>
        </div>
        })}
    </div>
}