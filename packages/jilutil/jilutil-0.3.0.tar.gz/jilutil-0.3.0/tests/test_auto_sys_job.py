from jilutil.auto_sys_job import AutoSysJob

jil_box_job = """/* ----------------- SAMPLE_BOX_JOB ----------------- */

insert_job: SAMPLE_BOX_JOB
alarm_if_fail: 1
date_conditions: 1
days_of_week: su,mo,tu,we,th,fr,sa
description: "Sample box job"
group: SOME_GROUP
job_type: BOX
owner: root@domain
permission: gx,ge,wx,we,mx,me
start_times: "20:00"
"""

def test_from_str():

    job = AutoSysJob.from_str(jil_box_job)

    assert isinstance(job, AutoSysJob)

    assert job['insert_job'] == 'SAMPLE_BOX_JOB'
    assert job['job_type'] == 'BOX'
    assert job['alarm_if_fail'] == '1'
    assert job['date_conditions'] == '1'
    assert job['days_of_week'] == 'su,mo,tu,we,th,fr,sa'
    assert job['description'] == 'Sample box job'
    assert job['group'] == 'SOME_GROUP'
    assert job['owner'] == 'root@domain'
    assert job['permission'] == 'gx,ge,wx,we,mx,me'
    assert job['start_times'] == '20:00'

def test_to_str():

    job = AutoSysJob('SAMPLE_BOX_JOB')
    job['job_type'] = 'BOX'
    job['alarm_if_fail'] = '1'
    job['date_conditions'] = '1'
    job['days_of_week'] = 'su,mo,tu,we,th,fr,sa'
    job['description'] = '"Sample box job"'
    job['group'] = 'SOME_GROUP'
    job['owner'] = 'root@domain'
    job['permission'] = 'gx,ge,wx,we,mx,me'
    job['start_times'] = '"20:00"'

    assert str(job) == jil_box_job
