from django_cron import CronJobBase, Schedule

from webservice.twitter.pull_data import \
    pull_latest_status, \
    pull_title_and_images, \
    remove_duplicate_news, \
    update_channel_latest_news


class TwitterCronJob(CronJobBase):

    RUN_EVERY_MINUTES = 10
    RETRY_AFTER_FAILURE_MINS = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINUTES)
    code = 'webservice.cron.twitter_cron_job'

    def do(self):
        pull_latest_status()
        remove_duplicate_news()
        pull_title_and_images()
        update_channel_latest_news()
