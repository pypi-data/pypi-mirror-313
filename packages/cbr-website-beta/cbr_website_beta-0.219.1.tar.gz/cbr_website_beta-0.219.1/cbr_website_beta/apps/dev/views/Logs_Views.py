import textwrap

from cbr_website_beta.utils.IP_Data                             import IP_Data
from osbot_aws.aws.dynamo_db.domains.DyDB__Table_With_Timestamp import DyDB__Table_With_Timestamp
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import timestamp_to_str, timestamp_utc_now_less_delta, timestamp_utc_now, date_time_now, \
    list_set
from osbot_utils.utils.Str import safe_str, html_encode

#MAX_CLOUD_WATCH_FETCH = 10000
LOGS_TO_FILTER_OUT   = ['/dev/api-log-data', '/dev/api-log-headers','/dev/request-logs']
LOG_FIELD__PATH__MAX_SIZE = 40

class Logs_Views:

    def api_log_data_today(self, dydb : DyDB__Table_With_Timestamp, env=None, fields=None, hours=None, ignore=None):
        index_name = 'date'
        index_value = date_time_now(date_time_format='%Y-%m-%d')
        return self.api_log_data(dydb=dydb, index_name=index_name, index_value=index_value, env=env,fields=fields, hours=hours, ignore=ignore)

    def api_log_data(self, dydb : DyDB__Table_With_Timestamp, index_name, index_value, env=None, fields=None, hours:int=5, ignore=None):
        documents =  self.logs_from_dydb_timestream(dydb=dydb, index_name=index_name, index_value=index_value, hours=hours, env=env)
        logs      = self.enrich_log_entries_html(documents, env)
        filtered_logs = []                                                              # Initialize a list to hold the filtered logs
        for log in logs:                                                                # Loop through each log entry
            if ignore and any(value in log.get(key) for key, value in ignore.items()):  # Check if any key in the ignore dict matches and should be excluded
                continue                                                                # Skip this log entry
            if fields:
                filtered_log = {field: log.get(field) for field in fields}              # Filter out the required fields from each log
                filtered_logs.append(filtered_log)                                      # Add the filtered log to the list
            else:
                filtered_logs.append(log)
        return filtered_logs                                                            # Return the filtered logs

    # @xray_trace("in request logs")
    # def request_logs(self):
    #     return render_template(**self.request_logs__data())


    # todo: double check all this code for XSS, since there are a lot of places where we are rendering html
    def create_link__request_logs(self, key, value, text , partition):
        return f'<a href="#" onclick="load_data_from_index(event, \'{key}\',\'{value}\');">{text}</a>'

    def create_link__user_info(self, username):
        if username:
            return f"<a href='/web/dev/current-user/{username}'>👤</a>"                                  # todo: check for XSS here
        return ''

    def create_html__user_name(self, user_name):
        wrapped_user_name = textwrap.wrap(user_name, width=30)
        html_user_name = '<br>'.join(wrapped_user_name)
        return f"<b>{html_user_name}</b>"

    def enrich_log_entries_html(self, documents, env):
        logs = []
        for log in documents:
            if log:
                timestamp = log.get('timestamp')
                user      = log.get('user'     )
                referer   = log.get('referer'  )
                user_name = log.get('user_name')
                if user_name is None:
                    if user == 'NA':
                        user = None

                    #log['ip_address'] = self.create_link__request_logs('ip_address', log.get('ip_address'), log.get('ip_address'), env)
                    if 'ip_address' in log:
                        log['ip_info'   ] = f"<a href='/web/dev/logs/ip-address?ip_address={log['ip_address']}&env={env}&hours=24'>🕵️‍♂️</a>"
                    #log['path'      ] = self.create_link__request_logs('path'      , log.get('path'      ), log.get('path'      ), env)
                    if user:
                        log['user_name' ] = (self.create_html__user_name(user)                                 +  ' ' +            # todo: refactor into better table (use capabilities of table JS API used)
                                             self.create_link__request_logs('user', user, '📈', env) +  ' ' +           # todo: check for XSS here
                                             self.create_link__user_info(user))                                                    # todo: check for XSS here
                    else:
                        log['user_name' ] = '<i>(anonymous)</i>'
                if referer:
                    if 'localhost' in referer:
                        log['referer'   ] = 'localhost'
                    if 'thecyberboardroom.com' in referer:
                        log['referer'] = 'tcb_website'
                log['when'      ] = timestamp_to_str(timestamp, date_time_format="%d %b %H:%M.%S")                                                                  # todo: shouldn't this be stored in the data?
                log['env'       ] = env
                if log.get('path'):
                    if len(log.get('path', '')) > LOG_FIELD__PATH__MAX_SIZE:                                                           # protect the path variable
                        log['path'] = log.get('path', '')[0:LOG_FIELD__PATH__MAX_SIZE] + f" ...({len(log.get('path', ''))})"
                    log['path'] = html_encode(log.get('path'))

                logs.append(log)
        return list(reversed(logs))

    def logs_from_dydb_timestream_today(self, dydb : DyDB__Table_With_Timestamp, hours=5, env=None):
        date_today = date_time_now(date_time_format='%Y-%m-%d')
        index_name = 'date'
        index_value = date_today
        return self.logs_from_dydb_timestream(dydb=dydb, index_name=index_name, index_value=index_value, hours=hours, env=env)


    def logs_from_dydb_timestream(self, dydb : DyDB__Table_With_Timestamp, index_name, index_value, hours=5, env=None):
        timestamp_start   = timestamp_utc_now_less_delta(hours=hours)     # get timestamp for last n hours
        timestamp_end     = timestamp_utc_now()
        kwargs            = dict(index_name      = index_name     ,
                                 index_value     = index_value    ,
                                 timestamp_start = timestamp_start,
                                 timestamp_end   = timestamp_end  )
        documents         = dydb.query_index_by_timestamp(**kwargs)

        documents = sorted(documents, key=lambda x: int(x['timestamp']), reverse=False)     # make sure the results are sorted by timestamp
        return documents


    def get_ip_address_data(self, ip_address):
        ip_data = IP_Data()
        return ip_data.request_get(ip_address)