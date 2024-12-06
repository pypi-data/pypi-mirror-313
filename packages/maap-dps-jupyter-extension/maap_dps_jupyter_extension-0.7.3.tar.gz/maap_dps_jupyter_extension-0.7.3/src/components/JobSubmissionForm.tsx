import React from 'react'
import { Button, ButtonToolbar, Form } from 'react-bootstrap'
import { AlgorithmDetailsBox } from './AlgorithmDetailsBox'
import { AlertBox } from './Alerts'
import { useSelector, useDispatch } from 'react-redux'
import AsyncSelect from 'react-select/async';
import { useEffect, useState, useRef } from 'react'
import { selectCMRSwitch, CMRSwitchActions } from '../redux/slices/CMRSwitchSlice'
import { getAlgorithms, describeAlgorithms, getResources, getCMRCollections, submitJob, getUserJobs } from '../api/maap_py'
import { algorithmsActions, selectAlgorithms } from '../redux/slices/algorithmsSlice'
import { parseScienceKeywords } from '../utils/ogc_parsers'
import '../../style/JobSubmission.css'
import { Notification } from "@jupyterlab/apputils"
import { jobsActions } from '../redux/slices/jobsSlice'
import { parseJobData } from '../utils/mapping'
import { copyTextToClipboard, openViewJobs } from '../utils/utils'
import { SUBMITTING_JOB_TEXT, SUBMITTED_JOB_SUCCESS, SUBMITTED_JOB_FAIL, SUBMITTED_JOB_ELEMENT_ID } from '../constants'


export const JobSubmissionForm = ({ jupyterApp }) => {

    // Redux
    const dispatch = useDispatch()

    const { setAlgorithm, setResource, setAlgorithmMetadata, setCMRCollection } = algorithmsActions
    const { setUserJobInfo, setJobRefreshTimestamp } = jobsActions
    const { selectedAlgorithm, selectedResource, selectedAlgorithmMetadata, selectedCMRCollection } = useSelector(selectAlgorithms)

    const { toggleValue, toggleDisabled } = CMRSwitchActions
    const { switchIsChecked, switchIsDisabled } = useSelector(selectCMRSwitch)


    // Local state variables
    const [jobTag, setJobTag] = useState('')
    const [command, setCommand] = useState('')
    const [showWaitCursor, setShowWaitCursor] = useState(false)
    const jobSubmitForm = useRef(null)

    useEffect(() => {
        if (selectedAlgorithm != null) {
            let res = describeAlgorithms(selectedAlgorithm["value"])
            res.then((data) => {
                dispatch(setAlgorithmMetadata(data))
            })
        }
    }, [selectedAlgorithm]);

    useEffect(() => {
        if (command != '') {
            copyTextToClipboard(command, "Copied Jupyter Notebook python command to clipboard.")
        }
    }, [command]);

    useEffect(() => {
        let elems: HTMLCollectionOf<Element> = document.getElementsByClassName("jl-ReactAppWidget")
        let pElement: HTMLElement = document.getElementById(SUBMITTED_JOB_ELEMENT_ID)
        
        // Apply the css to the parent div
        if (showWaitCursor) {
            elems[0].classList.add('wait-cursor')
            pElement.textContent = SUBMITTING_JOB_TEXT;
        } else {
            elems[0].classList.remove('wait-cursor')
        }
    }, [showWaitCursor]);


    const handleAlgorithmChange = value => {
        dispatch(setAlgorithm(value))
    }

    const handleResourceChange = value => {
        dispatch(setResource(value))
    }

    const handleCMRCollectionChange = value => {
        dispatch(setCMRCollection(value))
    }

    const disableSubmitButton = () => {
        let elemsButtons: HTMLCollectionOf<Element> = document.getElementsByClassName("btn btn-primary");
        for (let i=0; i<elemsButtons.length; i++){
            if (elemsButtons[i].getAttribute("type") === "submit") {
                elemsButtons[i].setAttribute("disabled", "true");
            }
        }
    }

    const enableSubmitButton = () => {
        let elemsButtons: HTMLCollectionOf<Element> = document.getElementsByClassName("btn btn-primary");
        for (let i=0; i<elemsButtons.length; i++){
            if (elemsButtons[i].getAttribute("type") === "submit" && elemsButtons[i].hasAttribute("disabled")) {
                elemsButtons[i].removeAttribute("disabled");
            }
        }
    }

    const setSubmittedJobText = (success: boolean, id: string, errorMessage: string) => {
        let pElement: HTMLElement = document.getElementById(SUBMITTED_JOB_ELEMENT_ID)
        if (success) {
            pElement.textContent = SUBMITTED_JOB_SUCCESS.replace("{TIME}", new Date().toUTCString()).replace("{ID}", id);
        } else {
            pElement.textContent = SUBMITTED_JOB_FAIL.replace("{TIME}", new Date().toUTCString()).replace("{ERROR}", errorMessage);
        }
    }

    const onSubmit = (event: any) => {
        disableSubmitButton();
        event.preventDefault();
        
        var jobParams = {
            algo_id: null,
            version: null,
            queue: null,
            identifier: null
        }
        
        if (selectedAlgorithm) {
            let algorithm = selectedAlgorithm.value.split(':')
            jobParams.algo_id = algorithm[0]
            jobParams.version = algorithm[1]
        }

        if (selectedResource) {
            jobParams.queue = selectedResource.value
        }

        jobParams.identifier = jobTag

        let data = new FormData(event.target)

        for (const input of data.entries()) {
            jobParams[input[0]] = input[1]
        }

        let formValidation = validateForm(jobParams)
        if (!formValidation) {

            // Submit job
            submitJob(jobParams).then((data) => {
                let msg = " Job submitted successfully. " + data['response'];
                Notification.success(msg, { autoClose: false, actions: [{
                    label: "View Jobs",
                    callback: () => {
                        openViewJobs(jupyterApp, null);
                      }

                }] })
                setSubmittedJobText(true, data['response'], null);
                setTimeout(() => {
                    enableSubmitButton()
                    setShowWaitCursor(false)
                }, 2000);
            }).catch(error => {
                Notification.error(error.message, { autoClose: false })
                setSubmittedJobText(false, null, error.message);
                setTimeout(() => {
                    enableSubmitButton()
                    setShowWaitCursor(false)
                }, 2000);
            })

            // Refresh job list once job has been submitted
            let response = getUserJobs()

            response.then((data) => {
                dispatch(setUserJobInfo(parseJobData(data["response"]["jobs"])))
            }).finally(() => {
                dispatch(setJobRefreshTimestamp(new Date().toUTCString()))
            })
            
        }else {
            Notification.error("Job failed to submit because "+formValidation, { autoClose: false })
            setShowWaitCursor(false);
            enableSubmitButton();
            setSubmittedJobText(false, null, formValidation);
        }
    }

    const validateForm = (params) => {
        let errorMsg = ""

        if (!params.algo_id) {
            errorMsg = "missing algorithm selection."
        }else if (!params.identifier) {
            errorMsg = "missing job tag."
        }else if (!params.queue) {
            errorMsg = "missing resource selection."
        }

        return errorMsg
    }

    // Reset job form
    const clearForm = () => {
        dispatch(setAlgorithm(null))
        dispatch(setResource(null))
        dispatch(setAlgorithmMetadata(null))

        setJobTag('')

        if (!switchIsDisabled) {
            dispatch(toggleDisabled())
        }

        if (switchIsChecked) {
            dispatch(toggleValue())
        }
        const activeElement = document.activeElement as HTMLElement | null;
        if (activeElement) activeElement.blur();
    }

    // Build job submission jupyter notebook command from user-provided selections
    const buildNotebookCommand = () => {
        // maap.submitJob({"algo_id": "test_algo", "username": "anonymous", "queue": "geospec-job_worker-32gb"})
        let jobParams = {
            algo_id: null,
            version: null,
            queue: null,
            identifier: null
        }
        
        if (selectedAlgorithm) {
            let algorithm = selectedAlgorithm.value.split(':')
            jobParams.algo_id = algorithm[0]
            jobParams.version = algorithm[1]
        }

        if (selectedResource) {
            jobParams.queue = selectedResource.value
        }

        jobParams.identifier = jobTag

        let data = new FormData(jobSubmitForm.current)
        

        let inputStr = ""
        for (const input of data.entries()) {
            jobParams[input[0]] = input[1]
            if (inputStr == "") {
                inputStr = input[0] + "=" + "\"" + input[1] + "\""
            } else {
                inputStr = inputStr + ",\n    " + input[0] + "=" + "\"" + input[1] + "\""
            }
        }

        let tmp = "maap.submitJob(identifier=\"" + jobParams.identifier + "\",\n    " + 
                  "algo_id=\"" + jobParams.algo_id + "\",\n    " + 
                  "version=\"" + jobParams.version + "\",\n    " + 
                  "queue=\"" + jobParams.queue + "\",\n    " + inputStr + ")"

        setCommand(tmp)
        const activeElement = document.activeElement as HTMLElement | null;
        if (activeElement) activeElement.blur();
    }
    
    return (
        <div className="submit-wrapper">
            <Form onSubmit={onSubmit} ref={jobSubmitForm}>
                <h5>1. General Information</h5>
                <Form.Group className="mb-3 algorithm-input">
                    <Form.Label>Algorithm</Form.Label>
                    <AsyncSelect
                        menuPortalTarget={document.querySelector('body')}
                        cacheOptions
                        defaultOptions
                        value={selectedAlgorithm}
                        loadOptions={getAlgorithms}
                        onChange={handleAlgorithmChange}
                        placeholder="Select algorithm..."
                    />
                </Form.Group>
                <Form.Group className="mb-3 algorithm-input">
                    <Form.Label>Job Tag</Form.Label>
                    <Form.Control type="text" value={jobTag} placeholder="Enter job tag..." onChange={event => setJobTag(event.target.value)} />
                </Form.Group>
                <Form.Group className="mb-3 algorithm-input">
                    <Form.Label>Resource</Form.Label>
                    <AsyncSelect
                        cacheOptions
                        defaultOptions
                        value={selectedResource}
                        loadOptions={getResources}
                        onChange={handleResourceChange}
                        placeholder="Select resource..."
                    />
                </Form.Group>

                {selectedAlgorithmMetadata ?
                    
                    // If user has selected an algorithm, render inputs and CMR info
                    <><h5>2. Algorithm Inputs</h5>
                        {Array.isArray(selectedAlgorithmMetadata.inputs) ? 
                        selectedAlgorithmMetadata.inputs.map((item, index) => {
                            switch (item["ows:Title"]) {
                                case "publish_to_cmr":
                                    if (switchIsDisabled) {
                                        dispatch(toggleDisabled())
                                    }
                                    return "publish to cmr"
                                case "queue_name":
                                    return "" // already integrated above using the resource async select
                                default:
                                    return <div key={`${item["ows:Title"]}_${index}`}>
                                        <Form.Group className="algorithm-input">
                                            <Form.Label>{`${item["ows:Title"]}`}</Form.Label>
                                            <Form.Control
                                                // value={item["ows:Title"]}
                                                name={item["ows:Title"]}
                                                placeholder={`Enter ${item["ows:Title"]}...`}
                                                required={false}
                                            />
                                        </Form.Group>
                                    </div>}}) : <AlertBox text="No inputs defined for selected algorithm." variant="primary" />}
                        <div className="cmr">
                            <div style={{ display: 'flex' }}>
                                <h5>3. Publish to Content Metadata Repository (CMR)?</h5>
                                <Form.Group>
                                    <Form.Switch
                                        //custom
                                        disabled={switchIsDisabled}
                                        type="switch"
                                        checked={switchIsChecked}
                                        onChange={() => dispatch(toggleValue())}
                                    />
                                </Form.Group>
                            </div>
                            {switchIsChecked ?
                                <Form.Group className="mb-3 algorithm-input">
                                    <Form.Label>CMR Collections</Form.Label>
                                    <AsyncSelect
                                        cacheOptions
                                        defaultOptions
                                        value={selectedCMRCollection}
                                        loadOptions={getCMRCollections}
                                        onChange={handleCMRCollectionChange}
                                        placeholder="Select CMR collection..."
                                    />
                                </Form.Group>
                                : null}
                            {selectedCMRCollection && switchIsChecked ?
                                <table className="cmr-table">
                                    <tr key={"concept-id"}>
                                        <td>Concept ID</td>
                                        <td>{selectedCMRCollection["concept-id"]}</td>
                                    </tr>
                                    <tr key={"name"}>
                                        <td>Name</td>
                                        <td>{selectedCMRCollection["ShortName"]}</td>
                                    </tr>
                                    <tr key={"description"}>
                                        <td>Description</td>
                                        <td>{selectedCMRCollection["Description"]}</td>
                                    </tr>
                                    <tr key={"science-keywords"}>
                                        <td>Science Keywords</td>
                                        {parseScienceKeywords(selectedCMRCollection["ScienceKeywords"]).map((item) => item + ", ")}
                                    </tr>
                                </table> : null}
                            {switchIsDisabled ? <AlertBox text="CMR publication not available for selected algorithm." variant="primary" /> : null}
                        </div></> : null}

                <hr />
                <ButtonToolbar>
                    <div style={{ display: 'flex', gap: '8px' }}>
                    <Button type="submit" onClick={() => setShowWaitCursor(true)}>Submit Job</Button>
                    <Button variant="outline-secondary" onClick={clearForm}>Clear</Button>
                    </div>
                    <div style={{ marginLeft: 'auto', display: 'flex', gap: '8px' }}>
                    <Button variant="outline-primary" onClick={() => openViewJobs(jupyterApp, null)}>View Jobs</Button>
                    <Button variant="outline-primary" onClick={buildNotebookCommand}>Copy as Jupyter Notebook Code</Button>
                    </div>
                </ButtonToolbar>
                <br />
                <p id={SUBMITTED_JOB_ELEMENT_ID}></p>
            </Form>
            {/* <AlgorithmDetailsBox /> */}
        </div>
    )
}