import streamlit as st
from streamlit.testing.v1 import AppTest

import src.auth as auth
from src.auth import (
    FAILED_ATTEMPTS_KEY,
    LOCKED_UNTIL_KEY,
    LOCKOUT_SECONDS,
    MAX_FAILED_ATTEMPTS,
    clear_failed_logins,
    lockout_remaining,
    record_failed_login,
)


def _login_probe():
    import src.auth as auth

    translations = {
        "auth_invalid": "Incorrect password.",
        "auth_locked": "Too many failed attempts. Try again in {seconds} seconds.",
    }
    auth.require_login(
        lambda key, **kwargs: translations.get(key, key).format(**kwargs)
        if kwargs
        else translations.get(key, key)
    )
    st.success("authenticated")


def test_failed_logins_trigger_and_expire_lockout():
    state = {}

    for _ in range(MAX_FAILED_ATTEMPTS - 1):
        # Mirrors require_login(): every rerun checks the lock before the next
        # form submission.
        assert lockout_remaining(state, now=100.0) == 0
        assert record_failed_login(state, now=100.0) == 0
    assert state[FAILED_ATTEMPTS_KEY] == MAX_FAILED_ATTEMPTS - 1

    assert lockout_remaining(state, now=100.0) == 0
    assert record_failed_login(state, now=100.0) == LOCKOUT_SECONDS
    assert state[LOCKED_UNTIL_KEY] == 100.0 + LOCKOUT_SECONDS
    assert lockout_remaining(state, now=100.0) == LOCKOUT_SECONDS
    assert lockout_remaining(state, now=130.0) == 0
    assert state[FAILED_ATTEMPTS_KEY] == MAX_FAILED_ATTEMPTS

    # The first failed attempt after expiry starts a fresh window.
    assert record_failed_login(state, now=130.0) == 0
    assert state[FAILED_ATTEMPTS_KEY] == 1


def test_successful_login_reset_removes_throttle_state():
    state = {FAILED_ATTEMPTS_KEY: 3, LOCKED_UNTIL_KEY: 120.0}

    clear_failed_logins(state)

    assert state == {}


def test_require_login_accumulates_attempts_across_streamlit_reruns(monkeypatch):
    monkeypatch.setattr(auth, "get_configured_password", lambda: "correct-password")
    app = AppTest.from_function(_login_probe, default_timeout=5).run()

    for attempt in range(MAX_FAILED_ATTEMPTS):
        app.text_input[0].set_value("wrong-password")
        app.button[0].click()
        app.run()
        if attempt < MAX_FAILED_ATTEMPTS - 1:
            assert app.error, f"attempt {attempt + 1} did not reach the login handler"

    assert any("Too many failed attempts" in warning.value for warning in app.warning)
    assert app.session_state[auth.FAILED_ATTEMPTS_KEY] == MAX_FAILED_ATTEMPTS
