import { configureStore } from '@reduxjs/toolkit'
import CMRSwitchReducer from './slices/CMRSwitchSlice'
import JobsContainerReducer from './slices/JobsContainerSlice'
import algorithmsReducer from './slices/algorithmsSlice'
import jobsReducer from './slices/jobsSlice'
import userInfoReducer from './slices/userInfoSlice'


export default configureStore({
  reducer: {
    Algorithms: algorithmsReducer,
    CMRSwitch: CMRSwitchReducer,
    JobsContainer: JobsContainerReducer,
    Jobs: jobsReducer,
    UserInfo: userInfoReducer
  },
  devTools: true,
})
