import { createSlice } from '@reduxjs/toolkit'
import { IJobsContainerSlice } from '../../types/slices'
import { IStore } from '../../types/store'

const initialState: IJobsContainerSlice = {
    /**
     * Number of rows in the jobs table to display per page.
     */
    itemSize: 10,
}

export const JobsContainerSlice = createSlice({
  name: 'JobsContainer',
  initialState,
  reducers: {
    resetSize: () => initialState,
    updateSize: (state, action) => {
      state.itemSize = action.payload
    },
  },
})

// Actions
export const JobsContainerActions = JobsContainerSlice.actions

// Selector
export const selectJobsContainer = (state: IStore): IJobsContainerSlice => state.JobsContainer

export default JobsContainerSlice.reducer
