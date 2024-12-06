"""AutoSys JIL Utility (https://github.com/mscribellito/JIL-Utility)"""
import re
from collections import UserDict


class AutoSysJob(UserDict):
    r"""Class that represents a job within AutoSys and its attributes

    Regex pattern for matching job start line:
    >>> re.match(AutoSysJob.job_start_regex, 'insert_job: FOO\n\nbar: baz').group(1)
    'FOO'
    """

    default_attributes = {
        'insert_job': '',
        'job_type': '',
        'box_name': '',
        'command': '',
        'machine': '',
        'owner': '',
        'permission': '',
        'date_conditions': '',
        'days_of_week': '',
        'start_times': '',
        'condition': '',
        'description': '',
        'std_out_file': '',
        'std_err_file': '',
        'alarm_if_fail': '',
        'group': '',
        'application': '',
        'send_notification': '',
        'notification_msg': '',
        'success_codes': '',
        'notification_emailaddress': '',
        'auto_delete': '',
        'box_terminator': '',
        'chk_files': '',
        'exclude_calendar': '',
        'job_load': '',
        'job_terminator': '',
        'max_exit_status': '',
        'max_run_alarm': '',
        'min_run_alarm': '',
        'n_retrys': '',
        'priority': '',
        'profile': '',
        'run_window': '',
        'term_run_time': ''
    }

    job_name_comment = '/* ----------------- {} ----------------- */'
    job_start_regex = '\\s*insert_job\\s*:\\s*([a-zA-Z0-9\\.\\#_-]{1,64})\\s*'


    def __init__(self, job_name = ''):
        """Instantiates a new instance"""

        super().__init__()
        self.job_name = job_name
        self.data['insert_job'] = job_name

    @property
    def attributes(self):
        """Returns attributes"""

        return self.data

    def __str__(self):
        """Returns string representation"""

        atts = self.data.copy()

        # insert special job name in comment format
        job_str = self.job_name_comment.format(atts['insert_job']) + '\n\n'

        # add special insert_job & job_type attributes
        job_str += 'insert_job: {}\n'.format(atts['insert_job'])
        del atts['insert_job']

        # iterate over attribute:value pairs in alphabetical order
        for attribute, value in sorted(atts.items()):
            if not value:
                continue
            # append att:val pair to job string
            job_str += '{}: {}\n'.format(attribute, value)

        return job_str

    @classmethod
    def from_str(cls, jil: str):
        r"""Creates a new AutoSysJob from a string

        ```pycon
        >>> AutoSysJob.from_str('')
        {'insert_job': ''}
        >>> AutoSysJob.from_str(None)
        {'insert_job': ''}
        >>> AutoSysJob.from_str('insert_job: TEST.ECHO   job_type: BOX \n')
        {'insert_job': 'TEST.ECHO', 'job_type': 'BOX'}
        >>> AutoSysJob.from_str('insert_job: TEST.ECHO \n repeated_field: value \n repeated_field: value')
        {'insert_job': 'TEST.ECHO', 'repeated_field': ['value', 'value']}
        >>> AutoSysJob.from_str("insert_job: TEST.ECHO \n foo: bar 'baz' \n bop: 'qux'")
        {'insert_job': 'TEST.ECHO', 'foo': "bar 'baz'", 'bop': 'qux'}
        >>> AutoSysJob.from_str('insert_job: TEST.ECHO \n foo: bar "baz" \n bop: "qux"')
        {'insert_job': 'TEST.ECHO', 'foo': 'bar "baz"', 'bop': 'qux'}
        >>> AutoSysJob.from_str('''insert_job: TEST.ECHO \n foo: "bar" "baz" \n bop: "qux 'bonk'"''')
        {'insert_job': 'TEST.ECHO', 'foo': '"bar" "baz"', 'bop': "qux 'bonk'"}
        >>> AutoSysJob.from_str('insert_job: TEST.ECHO \n foo: \n bop: "qux"')
        {'insert_job': 'TEST.ECHO', 'foo': '', 'bop': 'qux'}

        ```
        """
        job = cls()

        if not jil:
            return job

        # force job_type onto a new line
        jil = jil.replace('job_type', '\njob_type', 1)
        jil = jil.replace('\r\n', '\n')

        # split lines and strip line if not empty
        lines = [line.strip() for line in jil.split('\n') if line.strip() != '']

        multiline_comment_mode = False
        attribute_to_values = {}
        for line in lines:
            # check if line is a comment
            if line.startswith('/*') or line.startswith('#'):
                multiline_comment_mode = line.startswith('/*') and '*/' not in line
                continue

            if multiline_comment_mode:
                multiline_comment_mode = '*/' not in line
                continue

            # remove inline comments at the end of the line
            line = re.sub(r"(/\*.+/*)", '', line).strip()

            try:
                # get the attribute:value pair
                attribute, value = line.split(':', 1)
                attribute = attribute.strip()
                value = value.strip()

                # remove single or double quotes if the whole string is wrapped with them
                if (
                    isinstance(value, str) and value
                    and (value[0] in ('"', "'") and value[-1] in ('"', "'"))
                    and (value.count('"') == 2 or value.count("'") == 2)
                ):
                    value = value[1:-1]

                attribute_to_values.setdefault(attribute, []).append(value)
            except ValueError:
                continue

        attribute_to_values = {
            k: v if len(v) > 1 else v[0]
            for k, v in attribute_to_values.items()
        }

        job.update(attribute_to_values)
        job.job_name = job['insert_job']

        return job
