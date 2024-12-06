/**
 * Describes the fields to be displayed in the GeneralJobsInfo table component.
 * The accessors are relative to the IJob type.
 */

import { IJobInfoTable } from "../types/types";

export const GENERAL_JOBS_INFO: IJobInfoTable[] = [
    {
        header: "Tag",
        accessor: "tags"
    },
    {
        header: "Payload ID",
        accessor: "payload_id"
    },
    {
        header: "Job ID",
        accessor: "job_id"
    },
    {
        header: "Status",
        accessor: "status"
    },
    {
        header: "Queued Time",
        accessor: "time_queued"
    },
    {
        header: "Start Time",
        accessor: "time_start"
    },
    {
        header: "End Time",
        accessor: "time_end"
    },
    {
        header: "Duration",
        accessor: "duration"
    },
    {
        header: "Resource",
        accessor: "queue"
    }
]