import React from 'react'


export const ErrorMessage = ({error}) => {

    console.log('ErrorMessage->',error?.graphQLErrors)
    return <div>
        <div className='row justify-content-center'>
            <div className='col-aouto'>
                <i>Что-то пошло не так... ошибка.</i>
            </div>
        </div>
    </div>
}