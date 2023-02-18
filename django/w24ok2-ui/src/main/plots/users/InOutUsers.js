import React from 'react'
import Plot from 'react-plotly.js'
import { useParams, Redirect }            from 'react-router-dom'
import { useQuery, useReactiveVar } from '@apollo/client'
import { selectedUsersPlot, TLSOptions } from '../../../cache/main/rVar'
import { IN_OUT_USERS } from '../../requests/query'
import { Spiner } from '../../../share/Spiner'
import * as localeDictionary from 'plotly.js/lib/locales/ru.js'
import { ErrorMessage } from '../../../share/Errors/ErrorMessage'
import { PermissionDenied } from '../../../share/Errors/PermissionDenied'

export const InOutUsers = () => {
    const {slug} = useParams()

    const subSelectedUsersPlot = useReactiveVar(selectedUsersPlot)
    const { data, loading, error } = useQuery(IN_OUT_USERS, {variables: {warh: slug}})
    



    const m = []
    if(error?.graphQLErrors.find(item => item.message == 'Permission denied')){
        return <PermissionDenied />
    }
    
    if(data && !loading){
        return <div>
            <div className='row justify-content-center'>
                    <div className='col-auto'>
                        <select defaultValue='1' className="form-select form-select-sm noFocus mt-1" onChange={e => selectedUsersPlot(e.target.value)}>
                            <option value='absolute'>Абсолютное значение</option>
                            <option value='ratio'>Соотношение</option>
                        </select>
                    </div>
                </div>
            {/* -------------------------------------------Waterfall-plot-Start------------------------------------------ */}
            {
                subSelectedUsersPlot == 'absolute' && (
                    <Plot 
                        useResizeHandler
                        data={[{
                            x: data.inOutUsers.map(item => item.date),
                            // y: m.map(item => item.incomingUsers.length - item.departedUsers.length),
                            y: data.inOutUsers.map(item => item.waterfallStepChange),

                            type: 'waterfall',
                            orientation: 'v',
                            measure: data.inOutUsers.map(() => 'relative'),
                            textposition: 'outside',
                            connector: {
                                line: {
                                    color: "rgb(63, 63, 63)"
                                }
                            }
                        }]}
                        layout={{
                            dragmode: 'pan',
                            title: { text: 'График новых | ушедших пользователей'},
                            autosize: true,
                            xaxis: {
                                title: {
                                    type: 'date',
                                    text: 'Месяц',
                                    font: {
                                        size: 18
                                    }
                                }
                            },
                            yaxis: {
                                type: 'linear',
                                title: {
                                    text: 'Пользователей',
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
                )
            }
            {/* -------------------------------------------Waterfall-plot-End------------------------------------------ */}
            {/* -------------------------------------------Rato-two-plots-Start------------------------------------------ */}
            {
                subSelectedUsersPlot == 'ratio' && (
                    <Plot 
                        useResizeHandler
                        data={[
                            {
                                x: data.inOutUsers.map(item => item.date),
                                y: data.inOutUsers.map(item => item.incoming),
                                type: 'scatter',
                                name: 'Новых',
                                marker: {
                                    color: 'green'
                                },
                                line: {shape: 'spline'},
                            },
                            {
                                x: data.inOutUsers.map(item => item.date),
                                y: data.inOutUsers.map(item => item.departed),
                                name: 'Ушедших',
                                type: 'scatter',
                                marker: {
                                    color: '#f4564e'
                                },
                                line: {shape: 'spline'},
                            }
                        ]}
                        layout={{
                            dragmode: 'pan',
                            autosize: true,
                            title: { text: 'График пришедших | ушедших пользователей'},
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
                                    text: 'Пользователей',
                                    font: {
                                        size: 18
                                    }
                                }
                            },
                        }}
                        
                        style={{height: '100%', width: '100%'}}
                        config={{
                            displaylogo: false,
                            locales: { 'ru': localeDictionary },
                            locale: 'ru'
                        }}
                    />
                )
            }
            {/* -------------------------------------------Rato-two-plots-End------------------------------------------ */}
        </div>
    }

    if(error) return <ErrorMessage error={error}/>
    return <Spiner text="График пришедших | ушедших пользователей" />
}