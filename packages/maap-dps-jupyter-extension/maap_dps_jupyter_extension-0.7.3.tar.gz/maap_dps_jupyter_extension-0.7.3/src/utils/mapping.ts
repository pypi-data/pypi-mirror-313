import { IJob } from '../types/types'

export const parseJobData = (data: any) => {

    let tmpJobs: IJob[] = []
    data.map((job: any) => {

        let tmpJob: IJob = {}
        let tmp = Object.entries(job)

        if (tmp[0][0]) {
            tmpJob.payload_id = tmp[0][0]
        }

        if (tmp[0][1]) {
            tmpJob.name = ""
            tmpJob.job_type = tmp[0][1]['type']
            tmpJob.status = tmp[0][1]['status']
            tmpJob.tags = tmp[0][1]['tags']
            tmpJob.traceback = tmp[0][1]['traceback']

            if (tmp[0][1]['job']) {
                tmpJob.username = tmp[0][1]['job']['username']
                tmpJob.job_id = tmp[0][1]['job']['job_id']
                

                if (tmp[0][1]['job']['job_info']) {
                    tmpJob.queue = tmp[0][1]['job']['job_info']['job_queue']
                    tmpJob.time_end = tmp[0][1]['job']['job_info']['time_end']

                    /* If there is no time_start field, that implies the job never started (i.e. revoked). For sorting purposes, grab time_queued instead. */
                    tmpJob.time_start = tmp[0][1]['job']['job_info']['time_start'] ? tmp[0][1]['job']['job_info']['time_start'] : "" //tmp[0][1]['job']['job_info']['time_queued']
                    tmpJob.time_queued = tmp[0][1]['job']['job_info']['time_queued']
                    tmpJob.duration = tmp[0][1]['job']['job_info']['duration']

                    if (tmp[0][1]['job']['job_info']['facts']) {
                        tmpJob.ec2_instance_id = tmp[0][1]['job']['job_info']['facts']['ec2_instance_id']
                        tmpJob.ec2_instance_type = tmp[0][1]['job']['job_info']['facts']['ec2_instance_type']
                        tmpJob.ec2_availability_zone = tmp[0][1]['job']['job_info']['facts']['ec2_placement_availability_zone']
                    }

                    if (tmp[0][1]['job']['job_info']['metrics']) {
                        tmpJob.job_dir_size = tmp[0][1]['job']['job_info']['metrics']['job_dir_size']

                        if (tmp[0][1]['job']['job_info']['metrics']['products_staged']) {
                            tmpJob.products = tmp[0][1]['job']['job_info']['metrics']['products_staged']
                        }
                    }
                }
            }

            if (tmp[0][1]['job']['context']) {
                tmpJob.command = tmp[0][1]['job']['context']['_command']
                tmpJob.disk_usage = tmp[0][1]['job']['context']['_disk_usage']
                tmpJob.container_image_name = tmp[0][1]['job']['context']['container_image_name']
                tmpJob.container_image_url = tmp[0][1]['job']['context']['container_image_url']


                if (tmp[0][1]['job']['context']['job_specification']) {
                    tmpJob.params = tmp[0][1]['job']['context']['job_specification']['params']
                }
            }
        }

        tmpJobs.push(tmpJob)

    })

    return tmpJobs
}