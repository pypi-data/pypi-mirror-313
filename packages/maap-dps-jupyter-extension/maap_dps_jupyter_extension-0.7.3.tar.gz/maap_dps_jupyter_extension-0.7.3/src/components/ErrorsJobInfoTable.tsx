import React, { useState } from 'react'
import { useSelector } from 'react-redux'
import { EMPTY_FIELD_CHAR } from '../constants'
import { selectJobs } from '../redux/slices/jobsSlice'
import { ERRORS_JOBS_INFO } from '../templates/ErrorsJobInfoTable'
import { MdArrowDropDown, MdArrowRight } from 'react-icons/md';

export const ErrorsJobInfoTable = (): JSX.Element => {

    // Redux
    const { selectedJob } = useSelector(selectJobs)

    // Component local state
    const [expandError, setExpandError] = useState(false)

    return (
        <table className='table'>
            <tbody>
                {ERRORS_JOBS_INFO.map((field) => {
                    {
                        if (selectedJob['jobInfo'][field.accessor]) {
                            return <tr key={field.header}>
                                <th>{field.header}</th>
                                <td>
                                    <div onClick={() => setExpandError(!expandError)} className={expandError ? "show-content clickable" : "hide-content clickable"}>{expandError ? <MdArrowDropDown size={28} /> : <MdArrowRight size={28} />}{selectedJob['jobInfo'][field.accessor]}</div>
                                </td>
                            </tr>
                        } else {
                            return <tr key={field.header}>
                                <th>{field.header}</th>
                                <td>{EMPTY_FIELD_CHAR}</td>
                            </tr>
                        }
                    }
                })}
            </tbody>
        </table>
    )
}