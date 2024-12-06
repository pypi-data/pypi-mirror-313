import { createSlice } from '@reduxjs/toolkit'
import { ICMRSwitchSlice } from '../../types/slices'
import { IStore } from '../../types/store'

const initialState: ICMRSwitchSlice = {
  switchIsChecked: false,
  switchIsDisabled: true
}

export const CMRSwitchSlice = createSlice({
  name: 'CMRSwitch',
  initialState,
  reducers: {
    resetValue: () => initialState,
    toggleValue: (state): void => {
      state.switchIsChecked = !state.switchIsChecked
    },
    toggleDisabled: (state): void => {
      state.switchIsDisabled = !state.switchIsDisabled
    },
  },
})

// Actions
export const CMRSwitchActions = CMRSwitchSlice.actions

// Selector
export const selectCMRSwitch = (state: IStore): ICMRSwitchSlice => state.CMRSwitch

export default CMRSwitchSlice.reducer
