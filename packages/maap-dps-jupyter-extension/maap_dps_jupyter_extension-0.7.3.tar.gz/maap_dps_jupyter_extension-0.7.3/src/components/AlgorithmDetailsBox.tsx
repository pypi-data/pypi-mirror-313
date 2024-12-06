import React from 'react'
import { useSelector } from 'react-redux'
import { selectAlgorithms } from '../redux/slices/algorithmsSlice'
import { ALGORITHM_DETAILS_BOX } from '../templates/AlgorithmDetailsBox'

export const AlgorithmDetailsBox = () => {
    
    // Redux
    const { selectedAlgorithm } = useSelector(selectAlgorithms)

    return (
        <div className="algorithm-details">
            <h5>Algorithm Details</h5>
            <hr />
            { selectedAlgorithm ? ALGORITHM_DETAILS_BOX.map((field) => {
                if (selectedAlgorithm[field.accessor]) {
                    switch (field.type) {
                        case "code": return <><h6>{field.header}</h6>
                            <code>{selectedAlgorithm[field.accessor]}</code></>
                        case "url": return <><h6>{field.header}</h6>
                            <a href={field.accessor}>{selectedAlgorithm[field.accessor]}</a></>
                        default: <><h6>{field.header}</h6>
                            <span>{selectedAlgorithm[field.accessor]}</span></>
                    }
                }
            }) : <span className="subtext">No algorithm selected</span>
            }
        </div>
    )
}