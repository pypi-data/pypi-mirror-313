import React from 'react'
import { useSelector } from 'react-redux'
import { selectJobs } from '../redux/slices/jobsSlice'
import { METRICS_JOBS_INFO } from '../templates/MetricsJobInfoTable'

export const MetricsJobInfoTable = (): JSX.Element => {

    // Redux
    const { selectedJob } = useSelector(selectJobs)

    return (
        <table className='table'>
            <tbody>
                {METRICS_JOBS_INFO.map((field) => {
                    {
                        switch (field.type) {
                            case "code": return <tr key={field.header}>
                                <th>{field.header}</th>
                                {selectedJob['jobInfo'][field.accessor] ? <td><code>{selectedJob['jobInfo'][field.accessor]}</code></td> : <td>-</td>}
                            </tr>
                            case "url": return <tr key={field.header}>
                                <th>{field.header}</th>
                                {selectedJob['jobInfo'][field.accessor] ? <td><a href={selectedJob['jobInfo'][field.accessor]}>{selectedJob['jobInfo'][field.accessor]}</a></td> : <td>-</td>}
                            </tr>
                            default: return <tr key={field.header}>
                                <th>{field.header}</th>
                                {selectedJob['jobInfo'][field.accessor] ? <td>{selectedJob['jobInfo'][field.accessor]}</td> : <td>-</td>}
                            </tr>
                        }
                    }
                })}
            </tbody>
        </table>
    )
}