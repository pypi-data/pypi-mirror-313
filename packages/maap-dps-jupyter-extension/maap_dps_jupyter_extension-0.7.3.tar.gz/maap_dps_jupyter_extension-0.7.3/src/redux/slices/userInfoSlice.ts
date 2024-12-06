import { createSlice } from '@reduxjs/toolkit'
import { IUserInfoSlice } from '../../types/slices'
import { IStore } from '../../types/store'

const initialState: IUserInfoSlice = {
    username: null
}

export const userInfoSlice = createSlice({
  name: 'UserInfo',
  initialState,
  reducers: {
    resetUsername: () => initialState,
    setUsername: (state, action) => {
      state.username = action.payload
    },
  },
})

// Actions
export const userInfoActions = userInfoSlice.actions

// Selector
export const selectUserInfo = (state: IStore): IUserInfoSlice => state.UserInfo

export default userInfoSlice.reducer
