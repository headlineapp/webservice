from django_cron import CronJobBase, Schedule

from webservice.twitter.pull_data import pull_latest_status, pull_title_and_images


class TwitterCronJob(CronJobBase):

    RUN_EVERY_MINUTES = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINUTES)
    code = 'webservice.cron.twitter_cron_job'

    def do(self):
        pull_latest_status()
        pull_title_and_images()
