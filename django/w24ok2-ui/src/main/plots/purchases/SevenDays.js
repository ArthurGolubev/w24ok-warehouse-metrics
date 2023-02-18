import React from 'react'
import { useParams, Redirect }            from 'react-router-dom'
import Plot from 'react-plotly.js'
import { useQuery } from '@apollo/client'
import { SEVEN_DAYS } from '../../requests/query'
import { TLSOptions } from '../../../cache/main/rVar'
import { Spiner } from '../../../share/Spiner'
import * as localeDictionary from 'plotly.js/lib/locales/ru.js'
import { ErrorMessage } from '../../../share/Errors/ErrorMessage'

export const SevenDays = () => {
    const {slug} = useParams()

    const {data, loading, error} = useQuery(SEVEN_DAYS, {variables: {warh: slug}})
    
    // console.log('data SevenDays ->', data)
    if(error?.graphQLErrors.find(item => item.message == 'Permission denied')){
        return <Redirect to={{ pathname: '/permission-denied', state: { from: '/123'} }}/>
    }
    if(data){
        return <div>
            <Plot
                useResizeHandler
                data={[
                    {
                        x: data.sevenDays.map(day=> day.date),
                        y: data.sevenDays.map(day=> day.transactions),
                        type: 'scatter',
                        mode: 'lines+markers',
                        marker: {color: 'green'},
                        name: '',
                        hovertemplate: data.sevenDays.map(day=> 
                            'Дата: ' + new Date(day.date).toLocaleString('ru', TLSOptions()) +
                            '<br>Выдано ' + day.transactions +
                            '<br>Человек ' + day.uniqueUsers +
                            '<br>Касса ' + day.paid
                        ),
                    }
                ]}
                layout={{
                    dragmode: 'pan',
                    title: 'График выдач за последние 7 дней',
                    autosize: true,
                    xaxis: {
                        title: {
                            text: 'День',
                            font: {
                                size: 18
                            }
                        }
                    },
                    yaxis: {
                        title: {
                            text: 'Закупок',
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
    return <Spiner text="График за 7 дней" />
}