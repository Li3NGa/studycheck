import pytest
from studycheck.auth import hash_password,verify_password
from studycheck.session import AuthSessionStore
from studycheck.tenant import User
from studycheck.auth_middleware import authenticate_bearer,AuthenticationRequired

def test_password_round_trip():
    record=hash_password('correct-password')
    assert verify_password('correct-password',record)
    assert not verify_password('wrong-password',record)

def test_bearer_session_resolves_user():
    store=AuthSessionStore(); token=store.create('u1','t1')
    user=authenticate_bearer('Bearer '+token,store)
    assert user==User('u1','', 't1')

def test_invalid_bearer_is_rejected():
    with pytest.raises(AuthenticationRequired): authenticate_bearer('Bearer invalid',AuthSessionStore())
