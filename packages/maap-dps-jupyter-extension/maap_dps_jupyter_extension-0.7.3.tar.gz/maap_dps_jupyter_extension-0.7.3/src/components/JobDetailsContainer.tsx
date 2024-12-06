import React from 'react'
import { Button, Tab, Tabs } from 'react-bootstrap'
import { useSelector } from 'react-redux'
import { GeneralJobInfoTable } from './GeneralJobInfoTable'
import { InputsJobInfoTable } from './InputsJobInfoTable'
import { selectJobs } from '../redux/slices/jobsSlice'
import { MetricsJobInfoTable } from './MetricsJobInfoTable'
import '../../style/JobDetailsContainer.css'
import { ErrorsJobInfoTable } from './ErrorsJobInfoTable'
import { OutputsJobInfoTable } from './OutputsJobInfoTable'
import { JOB_QUEUED, JOB_STARTED } from '../constants'
import { cancelJob } from '../api/maap_py'
import { Notification } from "@jupyterlab/apputils";

export const JobDetailsContainer = ({ jupyterApp }): JSX.Element => {

    // Redux
    const { selectedJob } = useSelector(selectJobs)

    const cancelableStatuses: string[] = [JOB_STARTED, JOB_QUEUED] 

    const handleCancelJob = (job_id: string) => {
        cancelJob(job_id)
          .then((response) => {
            if (response["exception_code"] === "") {
              Notification.success(response["response"], { autoClose: false });
              return;
            }
            Notification.error(response["response"], { autoClose: false });
          })
          .catch((error) => {
            Notification.error(error.message, { autoClose: false });
          });
      };

    return (
      <div className="job-details-container">
        <div className='job-details-toolbar'>
          <h2>Job Details</h2>
          {selectedJob && cancelableStatuses.includes(selectedJob["jobInfo"]["status"]) ? (
            // TODO
            <Button variant="outline-primary" onClick={(e) => {
                handleCancelJob(selectedJob["jobInfo"]["payload_id"])
                e.currentTarget.blur();
            }
              }>Cancel Job</Button>
          ) : null}
        </div>
        <Tab.Container id="left-tabs-example" defaultActiveKey="general">
          <Tabs defaultActiveKey="general">
            <Tab eventKey="general" title="General">
              {selectedJob ? (
                <GeneralJobInfoTable />
              ) : (
                <div className="subtext mt-4">No job selected</div>
              )}
            </Tab>
            <Tab eventKey="inputs" title="Inputs">
              {selectedJob ? (
                <InputsJobInfoTable />
              ) : (
                <span className="subtext mt-4">No job selected</span>
              )}
            </Tab>
            <Tab eventKey="outputs" title="Outputs">
              {selectedJob ? (
                <OutputsJobInfoTable jupyterApp={jupyterApp} />
              ) : (
                <span className="subtext mt-4">No job selected</span>
              )}
            </Tab>
            <Tab eventKey="errors" title="Errors">
              {selectedJob ? (
                <ErrorsJobInfoTable />
              ) : (
                <span className="subtext mt-4">No job selected</span>
              )}
            </Tab>
            <Tab eventKey="metrics" title='Metrics'>
              {selectedJob ? (
                <MetricsJobInfoTable />
              ) : (
                <span className="subtext mt-4">No job selected</span>
              )}
            </Tab>
          </Tabs>
        </Tab.Container>
      </div>
    );
}