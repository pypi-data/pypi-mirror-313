import { createSlice } from '@reduxjs/toolkit'
import { IAlgorithmsSlice } from '../../types/slices'
import { IStore } from '../../types/store'

const initialState: IAlgorithmsSlice = {
  selectedAlgorithm: null,
  selectedResource: null,
  selectedAlgorithmMetadata: null,
  selectedCMRCollection: null
}

export const algorithmsSlice = createSlice({
  name: 'Algorithms',
  initialState,
  reducers: {
    resetValue: () => initialState,

    /**
     * Algorithm user has selected
     */
    setAlgorithm: (state, action): any => {
      state.selectedAlgorithm = action.payload
    },

    /**
     * Metadata for selected algorithm
     */
    setAlgorithmMetadata: (state, action): any => {
      state.selectedAlgorithmMetadata = action.payload
    },

    /**
     * Resource user has selected
     */
    setResource: (state, action): any => {
      state.selectedResource = action.payload
    },

    /**
     * CMR collection user has selected
     */
    setCMRCollection: (state, action): any => {
      state.selectedCMRCollection = action.payload
    },
  },
})

// Actions
export const algorithmsActions = algorithmsSlice.actions

// Selector
export const selectAlgorithms = (state: IStore): IAlgorithmsSlice => state.Algorithms

export default algorithmsSlice.reducer
