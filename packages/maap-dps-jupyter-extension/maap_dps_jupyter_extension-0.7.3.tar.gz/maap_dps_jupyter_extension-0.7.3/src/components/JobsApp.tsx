import React, { useEffect } from 'react'
import { JobsView } from './JobsView'
import { JUPYTER_EXT } from '../constants'
import 'bootstrap/dist/css/bootstrap.min.css'
import { useDispatch, useSelector } from 'react-redux'
import { selectUserInfo, userInfoActions } from '../redux/slices/userInfoSlice'

export const JobsApp = ({ jupyterApp }): JSX.Element => {

  // Redux
  const dispatch = useDispatch()

  return (
    <div className={JUPYTER_EXT.EXTENSION_CSS_CLASSNAME}>
      <JobsView jupyterApp={jupyterApp} />
    </div>
  )
}
