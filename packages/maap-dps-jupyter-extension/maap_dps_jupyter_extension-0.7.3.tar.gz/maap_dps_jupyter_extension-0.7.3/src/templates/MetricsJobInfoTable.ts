/**
 * Describes the fields to be displayed in the MetricsJobsInfo table component.
 * 
 */

import { IJobInfoTable } from "../types/types";

export const METRICS_JOBS_INFO: IJobInfoTable[] = [
    {
        header: "Instance Type",
        accessor: "ec2_instance_type",
    },
    {
        header: "Job Directory Size (B)",
        accessor: "job_dir_size",
    },
    {
        header: "Container Image Name",
        accessor: "container_image_name",
    },
    {
        header: "Container Image URL",
        accessor: "container_image_url",
    },
]