import React from 'react'
import { useSelector } from 'react-redux'
import { getProducts, getProductFolderPath } from '../utils/utils'
import { selectJobs } from '../redux/slices/jobsSlice'
import { OUTPUTS_JOBS_INFO } from '../templates/OutputsJobInfoTable'
import { EMPTY_FIELD_CHAR } from '../constants'
import { Button } from 'react-bootstrap'
import { FaFolder } from "react-icons/fa"
import { JupyterFrontEnd } from '@jupyterlab/application'
import { copyTextToClipboard } from '../utils/utils'
import { Notification } from '@jupyterlab/apputils'

async function navigateToFolder(folderPath: string, jupyterApp: JupyterFrontEnd): Promise<void> {
    const contents = jupyterApp.serviceManager.contents;

    if (folderPath) {
        // Check if the folder exists
        contents.get(folderPath).then(() => {
            // Navigate to the folder
            jupyterApp.shell.activateById('filebrowser');
            jupyterApp.commands.execute('filebrowser:go-to-path', { path: folderPath });
        }).catch(error => {
            let errorMessage = `Error navigating to folder: ${error.message}`;
            console.error(errorMessage);
            Notification.error(errorMessage, { autoClose: 3000 });
        });
    } else {
        Notification.error("No folder path to open.", { autoClose: 3000 });
    }
    const activeElement = document.activeElement as HTMLElement | null;
    if (activeElement) activeElement.blur();
  }

  function copyProductFolderPath(folderPath: string) {
    copyTextToClipboard(folderPath, "Copied product folder path to clipboard.");
    const activeElement = document.activeElement as HTMLElement | null;
    if (activeElement) activeElement.blur();
  }

export const OutputsJobInfoTable = ({ jupyterApp }): JSX.Element => {
    // Redux
    const { selectedJob } = useSelector(selectJobs)

    let productFolderPath = null;
    if (selectedJob['jobInfo'][OUTPUTS_JOBS_INFO.accessor]) {
        productFolderPath = getProductFolderPath(selectedJob['jobInfo'][OUTPUTS_JOBS_INFO.accessor]);
    }

    return (
        <table className='table'>
            <tbody>
                {selectedJob['jobInfo'][OUTPUTS_JOBS_INFO.accessor] ? 
                    <>
                    <tr key={OUTPUTS_JOBS_INFO.header+ " folder path"}>
                        <th style={{ whiteSpace: 'pre', verticalAlign: 'middle' }}>{OUTPUTS_JOBS_INFO.header+ " folder path"}</th>
                        <td style={{ whiteSpace: 'pre', verticalAlign: 'middle' }}>
                            <p>{productFolderPath}</p>
                            {productFolderPath ? 
                                <>
                                    <Button variant="primary" onClick={() => navigateToFolder(productFolderPath, jupyterApp)}><FaFolder />   Open in File Browser</Button>
                                    {"        "}
                                    <Button variant="primary" onClick={() => copyProductFolderPath(productFolderPath)}><FaFolder />   Copy Folder Path to Clipboard</Button>
                                </>: null}
                        </td>
                    </tr>
                    <tr key={OUTPUTS_JOBS_INFO.header+ " urls"}>
                        <th style={{ whiteSpace: 'pre', verticalAlign: 'middle' }}>{OUTPUTS_JOBS_INFO.header+ " urls"}</th>
                        <td style={{ whiteSpace: 'pre', verticalAlign: 'middle' }}>
                            {getProducts(selectedJob['jobInfo'][OUTPUTS_JOBS_INFO.accessor])}
                        </td>
                    </tr> 
                </>
                : <tr key="no-outputs">
                        <th>{OUTPUTS_JOBS_INFO.header}</th>
                        <td>{EMPTY_FIELD_CHAR}</td>
                    </tr>
                }
            </tbody>
        </table>
    )
}