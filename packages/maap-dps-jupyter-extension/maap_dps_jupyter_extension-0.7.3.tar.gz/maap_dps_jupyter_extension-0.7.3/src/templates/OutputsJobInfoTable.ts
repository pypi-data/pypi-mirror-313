/**
 * Describes the fields to be displayed in the GeneralJobsInfo table component.
 * The accessors are relative to the IJob type.
 */

import { STYLE_TYPE } from "../constants";
import { IJobInfoTable } from "../types/types";

export const OUTPUTS_JOBS_INFO: IJobInfoTable = 
    {
        header: "Products",
        accessor: "products",
        type: STYLE_TYPE.URL
    }