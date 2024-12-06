from jilutil.jil_parser import JilParser


def test_jil_parser_parse_jobs_from_str(project_root):
    actual = JilParser(None).parse_jobs_from_str("")
    assert actual == {'jobs': []}

    actual = JilParser(None).parse_jobs_from_str("insert_job: JOB_NAME\n")
    assert actual == {'jobs': [{'insert_job': 'JOB_NAME'}]}


def test_jil_parser_parse_jobs_from_str_one_dot_jil(project_root):
    actual = JilParser(None).parse_jobs_from_str(
        (project_root / "tests/one.jil").read_text()
    )
    assert actual == {'jobs': [{
        'command': 'echo "Hello World"',
        'insert_job': 'TEST.ECHO',
        'job_type': 'CMD',
        'machine': 'orasvr19',
        'owner': 'waadm'
    }, {
        'insert_job': 'ft_job',
        'job_type': 'FT',
        'machine': 'unixagt',
        'owner': 'julian',
        'watch_file': '/PAYROL/payrol.input',
        'watch_file_type': 'EXIST'
    }, {
        'insert_job': 'ft_job',
        'job_type': 'FT',
        'machine': 'ftagt',
        'owner': 'julian',
        'watch_file': r'c:\data\monthly.log',
        'watch_file_type': 'GENERATE',
        'watch_no_change': '2'
    }, {
        'insert_job': 'fw_job',
        'job_type': 'FW',
        'machine': 'winagent',
        'owner': 'julian',
        'watch_file': r'c:\tmp\watch_file.log',
        'watch_file_min_size': '10000',
        'watch_interval': '90'
    }, {
        'command': 'echo "Simple Job Creation"',
        'insert_job': 'TEST.ECHO.UNX.CD',
        'job_type': 'CMD',
        'machine': 'orasvr19',
        'owner': 'waadm',
        'std_err_file': '/tmp/$AUTO_JOB_NAME.err',
        'std_out_file': '/tmp/$AUTO_JOB_NAME.out'
    }]}


def test_jil_parser_parse_jobs_from_str_two_dot_jil(project_root):
    actual = JilParser(None).parse_jobs_from_str(
        (project_root / "tests/two.jil").read_text()
    )
    assert actual == {'jobs': [{
        'command': '/root/backup.sh',
        'date_conditions': '1',
        'days_of_week': 'all',
        'insert_job': 'prodbackup',
        'machine': 'prod1',
        'owner': 'root',
        'start_times': '22:00',
        'term_run_time': '600'
    }, {
        'command': '/root/backup.sh && curl -sm 30 k.wdt.io/123abc/backupdb',
        'date_conditions': '1',
        'days_of_week': 'all',
        'insert_job': 'prodbackup',
        'machine': 'prod1',
        'owner': 'root',
        'start_times': '22:00',
        'term_run_time': '600'
    }]}


def test_jil_parser_parse_jobs_from_str_three_dot_jil(project_root):
    actual = JilParser(None).parse_jobs_from_str(
        (project_root / "tests/three.jil").read_text()
    )
    assert actual == {'jobs': [{
        'alarm_if_fail': '1',
        'command': '/path/to/watch_done_file.sh',
        'date_conditions': 'y',
        'days_of_week': 'all',
        'description': 'Watch for .done file arrival',
        'insert_job': 'WATCH_DONE_FILE',
        'job_type': 'CMD',
        'machine': 'hostname',
        'max_run_alarm': '600',
        'owner': 'autosys_user',
        'permission': 'gx,ge,wx',
        'profile': '/home/autosys_user/.profile',
        'start_times': '00:00',
        'std_err_file': '/path/to/logs/WATCH_DONE_FILE.err',
        'std_out_file': '/path/to/logs/WATCH_DONE_FILE.out'
    }]}


def test_jil_parser_parse_jobs_from_str_four_dot_jil(project_root):
    actual = JilParser(None).parse_jobs_from_str(
        (project_root / "tests/four.jil").read_text()
    )
    assert actual == {'jobs': [{
        'command': '$HOME/POST',
        'condition': 'success(EOD_watch)',
        'insert_job': 'EOD_post',
        'job_type': 'cmd',
        'machine': 'prod'
    }, {
        'command': 'sleep 10',
        'condition': 'success(test_sample_01,12.00) AND '
                     'failure(test_sample_02,24.00) AND '
                     'success(test_sample_03)',
        'insert_job': 'test_sample_04',
        'machine': 'localhost'
    }]}
