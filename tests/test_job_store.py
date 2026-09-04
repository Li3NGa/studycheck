from studycheck.job_store import SQLiteJobStore

def test_job_store_round_trip(tmp_path):
    store = SQLiteJobStore(tmp_path / 'jobs.db')
    created = store.create('learning', {'user_id': 'u1'})
    assert created['status'] == 'queued'
    assert store.get(created['job_id'])['payload']['user_id'] == 'u1'
    done = store.update(created['job_id'], 'completed', {'user_id': 'u1', 'total': 8})
    assert done['status'] == 'completed'
    assert store.get(created['job_id'])['payload']['total'] == 8
