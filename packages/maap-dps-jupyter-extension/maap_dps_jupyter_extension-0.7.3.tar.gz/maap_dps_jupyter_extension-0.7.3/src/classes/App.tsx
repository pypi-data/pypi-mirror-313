import React from 'react'
import { ReactWidget } from '@jupyterlab/apputils'
import { Provider } from 'react-redux'
import { JobsApp } from '../components/JobsApp'
import { JUPYTER_EXT } from '../constants'
import store from '../redux/store'
import 'regenerator-runtime/runtime'
import { JobSubmissionForm } from '../components/JobSubmissionForm'
import { JupyterFrontEnd } from '@jupyterlab/application';

export class ViewJobsReactAppWidget extends ReactWidget {
  jupyterApp: JupyterFrontEnd
  constructor(jupyterApp: JupyterFrontEnd) {
    super()
    this.addClass(JUPYTER_EXT.EXTENSION_CSS_CLASSNAME)
    this.jupyterApp = jupyterApp
  }

  render(): JSX.Element {
    return (
      <Provider store={store}>
        <JobsApp jupyterApp={this.jupyterApp} />
      </Provider>
    )
  }
}

export class SubmitJobsReactAppWidget extends ReactWidget {
  data: any
  jupyterApp: JupyterFrontEnd
  constructor(data: any, jupyterApp: JupyterFrontEnd) {
    super()
    this.addClass(JUPYTER_EXT.EXTENSION_CSS_CLASSNAME)
    this.data = data
    this.jupyterApp = jupyterApp
  }

  render(): JSX.Element {
    return (
      <Provider store={store}>
        <JobSubmissionForm jupyterApp={this.jupyterApp} />
      </Provider>
    )
  }
}
