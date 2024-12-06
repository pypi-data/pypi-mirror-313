import React from 'react'
import { Alert } from 'react-bootstrap'
import { BsInfoCircleFill } from 'react-icons/bs'
import '../../style/Alerts.css'

export const AlertBox = ({ text, variant }) => {
    return (
        <Alert variant={variant}><BsInfoCircleFill />{text}</Alert>
    )
}