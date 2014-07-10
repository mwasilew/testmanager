from testmanager.testrunner.models import Bug


class BugTracker(object):

    def __init__(self, tracker_name, tracker):
        self.tracker_name = tracker_name
        self.tracker = tracker

    def update_bugs(self, bug_id_list):
        getattr(self,
                "_update_%s_buglist" % (self.tracker['type']))(
                    bug_id_list,
                    **self.tracker)

    def _update_bugzilla_buglist(self,
                                 bug_id_list,
                                 username=None,
                                 password=None,
                                 **kwargs):
        import requests
        import csv
        from StringIO import StringIO

        if username and password:
            response = requests.get(
                "%sbuglist.cgi?bug_id=%s&ctype=csv&bug_id_type=anyexact&query_format=advanced&columnlist=bug_status,short_desc,bug_severity" % (self.tracker['url'], '%2C'.join(str(x) for x in bug_id_list)),
                auth=(username, password))
        else:
            response = requests.get(
                "%sbuglist.cgi?bug_id=%s&ctype=csv&bug_id_type=anyexact&query_format=advanced&columnlist=bug_status,short_desc,bug_severity" % (self.tracker['url'], '%2C'.join(str(x) for x in bug_id_list))
            )

        if response.status_code == 200:
            tmp_file = StringIO(response.text)
            resultlist = csv.DictReader(tmp_file)
            for row in resultlist:
                bug_defaults = {
                    'summary': row['short_desc'],
                    'status': row['bug_status'],
                    'severity': row['bug_severity'],
                }
                db_bug, created = Bug.objects.get_or_create(
                    alias=row['bug_id'],
                    tracker=self.tracker_name,
                    defaults=bug_defaults)
                if not created:
                    for attr, value in bug_defaults.iteritems():
                        setattr(db_bug, attr, value)
                    db_bug.save()

    def _update_jira_buglist(self,
                             bug_id_list,
                             username=None,
                             password=None,
                             **kwargs):
        import requests
        import json

        payload = json.dumps(
            {"jql": "issueKey in (%s)" % ','.join(str(x) for x in bug_id_list,),
             "fields": ["key", "summary", "priority", "status"]})
        headers = {'content-type': 'application/json'}
        # only 50 bugs is returned by default. Needs to be fixed later to fetch all
        response = requests.post(
            "%srest/api/2/search" % (self.tracker['url']),
            data=payload,
            headers=headers,
            auth=(username, password))
        if response.status_code == 200:
            resp_json = json.loads(response.text)
            for bug in resp_json['issues']:
                bug_defaults = {
                    'summary': bug['fields']['summary'],
                    'status': bug['fields']['status']['name'],
                    'severity': bug['fields']['priority']['name'],
                }
                db_bug, created = Bug.objects.get_or_create(
                    alias=bug['key'],
                    tracker=self.tracker_name,
                    defaults=bug_defaults)
                if not created:
                    for attr, value in bug_defaults.iteritems():
                        setattr(db_bug, attr, value)
                    db_bug.save()

    def _update_launchpad_buglist(self,
                                  bug_id_list,
                                  username=None,
                                  password=None,
                                  **kwargs):
        from launchpadlib.launchpad import Launchpad
        cachedir = "/tmp/launchpadcache"
        lp = Launchpad.login_anonymously('qa-reports.linaro.org',
                                 'production',
                                  cachedir,
                                  version='devel')
        for bug_id in bug_id_list:
            lp_bug = lp.bugs[int(bug_id)]
            lp_severity = ''
            lp_status = ''
            for task in lp_bug.bug_tasks:
                lp_severity += "%s: %s | " % (task.bug_target_display_name, task.importance)
                lp_status += "%s: %s | " % (task.bug_target_display_name, task.status)
            bug_defaults = {
                'summary': lp_bug.title,
                'status': lp_status,
                'severity': lp_severity,
            }
            db_bug, created = Bug.objects.get_or_create(
                alias=bug_id,
                tracker=self.tracker_name,
                defaults=bug_defaults)
            if not created:
                for attr, value in bug_defaults.iteritems():
                    setattr(db_bug, attr, value)
                db_bug.save()
