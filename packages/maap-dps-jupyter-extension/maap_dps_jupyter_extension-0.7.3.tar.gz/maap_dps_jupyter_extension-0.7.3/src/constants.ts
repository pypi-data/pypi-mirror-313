/*******************************
 * Jupyter Extension
 *******************************/
export const JUPYTER_EXT = {
    EXTENSION_CSS_CLASSNAME : 'jl-ReactAppWidget',

    VIEW_JOBS_PLUGIN_ID : 'jobs_view:plugin',
    VIEW_JOBS_NAME : 'View Jobs',
    VIEW_JOBS_OPEN_COMMAND : 'jobs_view:open',

    SUBMIT_JOBS_PLUGIN_ID : 'jobs_submit:plugin',
    SUBMIT_JOBS_NAME : 'Submit Jobs',
    SUBMIT_JOBS_OPEN_COMMAND : 'jobs_submit:open',

    REGISTER_ALGORITHM_PLUGIN_ID : 'register_algorithm:plugin',
    REGISTER_ALGORITHM_NAME : 'Register Algorithm',
    REGISTER_ALGORITHM_OPEN_COMMAND : 'register_algorithm:open'
}


/*******************************
 * Jobs Tables
 *******************************/

export const MAX_CELL_WIDTH = 350

export const STYLE_TYPE = {
    CODE : "code",
    TEXT : "text",
    URL  : "url"
}

export const EMPTY_FIELD_CHAR = '-'

export const SUBMITTING_JOB_TEXT = "Submitting job...";
export const SUBMITTED_JOB_SUCCESS = "{TIME}\nJob submitted successfully. {ID}";
export const SUBMITTED_JOB_FAIL = "{TIME}\nJob submission failed because {ERROR}";
export const SUBMITTED_JOB_ELEMENT_ID = "submitting_job_text";

export const JOB_STARTED = "job-started";
export const JOB_QUEUED = "job-queued";