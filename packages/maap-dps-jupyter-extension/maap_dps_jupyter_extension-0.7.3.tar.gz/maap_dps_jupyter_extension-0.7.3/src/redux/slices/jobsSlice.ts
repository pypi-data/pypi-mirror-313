import { createSlice } from '@reduxjs/toolkit'
import { IJobsSlice } from '../../types/slices'
import { IStore } from '../../types/store'

const initialState: IJobsSlice = {
  userJobIDs: [],
  userJobs: [],
  userJobStatuses: [],
  selectedJob: null,
  userJobInfo: [],
  formattedJobsInfo: [],
  jobRefreshTimestamp: null
}

export const jobsSlice = createSlice({
  name: 'Jobs',
  initialState,
  reducers: {
    resetValue: () => initialState,

    setUserJobIDs: (state, action): any => {
      state.userJobIDs = action.payload
    },

    setUserJobs: (state, action): any => {
        state.userJobs = action.payload
    },

    setJobStatuses: (state, action): any => {
      state.userJobStatuses = action.payload
    },

    setSelectedJob: (state, action): any => {
      state.selectedJob = action.payload
    },

    setUserJobInfo: (state, action): any => {
      state.userJobInfo = action.payload
    },

    setFormattedJobsInfo: (state, action): any => {
      state.formattedJobsInfo = action.payload
    },

    setJobRefreshTimestamp: (state, action): any => {
      state.jobRefreshTimestamp = action.payload
    }
  },
})

// Actions
export const jobsActions = jobsSlice.actions

// Selector
export const selectJobs = (state: IStore): IJobsSlice => state.Jobs

export default jobsSlice.reducer
