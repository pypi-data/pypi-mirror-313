/**
 * Describes the fields to be displayed in the AlgorithmDetailsBox component.
 * The accessors are relative to the IJob type.
 */

import { STYLE_TYPE } from "../constants";

export const ALGORITHM_DETAILS_BOX = [
    {
        header: "Description",
        accessor: "description",
        type: STYLE_TYPE.TEXT
    },
    {
       header: "Repo URL",
       accessor: "url",
       type: STYLE_TYPE.URL
   },
   {
       header: "Version",
       accessor: "version",
       type: STYLE_TYPE.TEXT
   },
   {
       header: "Run Command",
       accessor: "command",
       type: STYLE_TYPE.CODE
   }
]