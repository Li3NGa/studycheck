from studycheck.jobs import LearningJobRunner, SQLiteJobStore


def test_job_lifecycle_and_persistence(tmp_path):
    store = SQLiteJobStore(str(tmp_path / 'jobs.db'))
    job = store.create('u1')
    done = LearningJobRunner(store, lambda user_id: {'user_id': user_id, 'total': 3}).run(job.job_id)
    assert done.status == 'completed'
    assert done.result == {'user_id': 'u1', 'total': 3}
    assert store.get(job.job_id).result == done.result


def test_job_failure_is_persisted(tmp_path):
    store = SQLiteJobStore(str(tmp_path / 'jobs.db'))
    job = store.create('u2')
    failed = LearningJobRunner(store, lambda _: (_ for _ in ()).throw(RuntimeError('boom'))).run(job.job_id)
    assert failed.status == 'failed'
    assert failed.error == 'boom'
