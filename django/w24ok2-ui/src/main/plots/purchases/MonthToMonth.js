import React from 'react'
import Plot from 'react-plotly.js'
import { useParams, Redirect }            from 'react-router-dom'
import { useQuery, useReactiveVar } from '@apollo/client'
import { MONTH_TO_MONTH } from '../../requests/query'
import { selectedMonthToMonthSubject } from '../../../cache/main/rVar'
import { Spiner } from '../../../share/Spiner'
import * as localeDictionary from 'plotly.js/lib/locales/ru.js'
import { ErrorMessage } from '../../../share/Errors/ErrorMessage'



export const MonthToMonth = () => {
    const {slug} = useParams()

    const {data, loading, error} = useQuery(MONTH_TO_MONTH, {variables: {warh: slug}})
    
    // console.log(data)
    
    const subSelectedMonthToMonthSubject = useReactiveVar(selectedMonthToMonthSubject)
    const month_ = [
        'Январь',
        'Февраль',
        'Март',
        'Апрель',
        'Май',
        'Июнь',
        'Июль',
        'Август',
        'Сентябрь',
        'Октябрь',
        'Ноябрь',
        'Декабрь',
    ]
    const selectedMonthToMonthSubjectHandler = e => {
        switch(e.target.value){
            case '1':
                selectedMonthToMonthSubject({title: 'выручки', key: 'paid', yaxis: 'Выручка'})
                break
            case '2':
                selectedMonthToMonthSubject({title: 'выдач', key: 'transactions', yaxis: 'Выдач'})
                break
            case '3':
                selectedMonthToMonthSubject({title: 'пользователей', key: 'uniqueUsers', yaxis: 'Пользователей'})
                break
        }
    }

    if(error?.graphQLErrors.find(item => item.message == 'Permission denied')){
        return <div>Permission denied</div>
    }



    if(data && !loading){
        return <div className="my-6">
            <div className='row justify-content-center'>
                <div className='col-auto'>
                    <select defaultValue='1' className="form-select form-select-sm noFocus mt-1" onChange={e => selectedMonthToMonthSubjectHandler(e)}>
                        <option value='1'>Выручка</option>
                        <option value='2'>Выдачи</option>
                        <option value='3'>Пользователи</option>
                    </select>
                </div>
            </div>
            <Plot
                useResizeHandler
                data={data.monthToMonth.map(year => {
                    return {
                        x: month_,
                        y: year.body.map((month, iter) => month[subSelectedMonthToMonthSubject.key]),
                        type: 'scatter',
                        name: year.date,
                        line: {shape: 'spline'},
                        hovertemplate: year.body.map(month=> 
                            month.transactions + ' выдач<br>' +
                            month.uniqueUsers + ' пользователей<br>' +
                            month.paid + ' заплачено<br>'
                        ),
                    }
                })}
                layout={{
                    dragmode: 'pan',
                    title: `График ${subSelectedMonthToMonthSubject.title} по месяцам`,
                    autosize: true,
                    xaxis: {
                        title: {
                            text: 'Месяц',
                            font: {
                                size: 18
                            }
                        }
                    },
                    yaxis: {
                        title: {
                            text: subSelectedMonthToMonthSubject.yaxis,
                            font: {
                                size: 18
                            }
                        }
                    }
                }}
                style={{height: '100%', width: '100%'}}
                config={{
                    displaylogo: false,
                    locales: { 'ru': localeDictionary },
                    locale: 'ru'
                }}
            />
        </div>
    }

    if(error) return <ErrorMessage error={error}/>
    return <Spiner text="График по годам" />
}