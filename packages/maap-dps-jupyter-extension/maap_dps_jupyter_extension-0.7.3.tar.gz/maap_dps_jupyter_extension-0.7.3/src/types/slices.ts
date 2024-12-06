/* eslint-disable @typescript-eslint/member-delimiter-style */
export interface ICountSlice {
  count: number
  clicked: number
}

export interface IJobsContainerSlice {
  itemSize: number
}

export interface IJobsSlice {
  userJobIDs: [],
  userJobs: [],
  userJobStatuses: [],
  selectedJob: any,
  userJobInfo: any,
  formattedJobsInfo: any,
  jobRefreshTimestamp: any
}

export interface IAlgorithmsSlice {
  selectedAlgorithm: any
  selectedResource: any
  selectedAlgorithmMetadata: any
  selectedCMRCollection: any
}

export interface ICMRSwitchSlice {
  switchIsChecked: boolean
  switchIsDisabled: boolean
}

export interface IUserInfoSlice {
  username: string
}
