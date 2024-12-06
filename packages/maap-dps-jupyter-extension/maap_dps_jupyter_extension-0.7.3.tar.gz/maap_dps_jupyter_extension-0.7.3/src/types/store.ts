import { IAlgorithmsSlice, ICMRSwitchSlice, IJobsSlice, IJobsContainerSlice, IUserInfoSlice } from "./slices"

export interface IStore {
  Algorithms: IAlgorithmsSlice,
  CMRSwitch: ICMRSwitchSlice,
  JobsContainer: IJobsContainerSlice,
  Jobs: IJobsSlice,
  UserInfo: IUserInfoSlice
}
