import React, { useState } from 'react'
import { useSelector } from 'react-redux'
import { selectJobs } from '../redux/slices/jobsSlice'
import { GENERAL_JOBS_INFO } from '../templates/GeneralJobInfoTable'
import { secondsToReadableString } from '../utils/utils'
import { EMPTY_FIELD_CHAR } from '../constants'

export const GeneralJobInfoTable = (): JSX.Element => {

    // Redux
    const { selectedJob } = useSelector(selectJobs)

    return (
        <table className='table'>
            <tbody>
                {GENERAL_JOBS_INFO.map((field) => {
                    {
                        if (selectedJob['jobInfo'][field.accessor]) {
                            switch (field.accessor) {
                                case "duration": return <tr key={field.header}>
                                    <th>{field.header}</th>
                                    <td>
                                        {secondsToReadableString(selectedJob['jobInfo'][field.accessor])}
                                    </td>
                                </tr>
                                default: return <tr key={field.header}>
                                    <th>{field.header}</th>
                                    <td>{selectedJob['jobInfo'][field.accessor]}</td>
                                </tr>
                            }
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