import React from 'react'


export const Spiner = ({text}) => {

    return <div>
        <div className="d-flex justify-content-center">
            <div className="spinner-border text-warning" role="status">
                <span className="visually-hidden">Loading...</span>
            </div>
            <p className="text-center mx-4">{text}</p>
        </div>
    </div>
}   