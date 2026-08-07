"""Simple password gate using Streamlit secrets."""

from __future__ import annotations

import hmac
import math
import time

import streamlit as st

AUTH_KEY = "authenticated"
FAILED_ATTEMPTS_KEY = "auth_failed_attempts"
LOCKED_UNTIL_KEY = "auth_locked_until"
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_SECONDS = 30


def get_configured_password() -> str | None:
    """Return app_password from secrets, or None if not configured."""
    try:
        secrets = st.secrets
    except Exception:
        return None
    try:
        password = secrets["app_password"]
    except Exception:
        return None
    if password is None or str(password).strip() == "":
        return None
    return str(password)


def is_authenticated() -> bool:
    return bool(st.session_state.get(AUTH_KEY, False))


def logout() -> None:
    st.session_state[AUTH_KEY] = False


def lockout_remaining(state, now: float | None = None) -> int:
    """Return remaining lockout seconds without mutating failed-attempt state."""
    now = time.monotonic() if now is None else now
    locked_until = float(state.get(LOCKED_UNTIL_KEY, 0.0))
    return math.ceil(locked_until - now) if locked_until > now else 0


def record_failed_login(state, now: float | None = None) -> int:
    """Record a failed attempt and return the new lockout duration, if any."""
    now = time.monotonic() if now is None else now

    # A lockout expiry starts a fresh window, but only when a new failed
    # attempt is actually recorded. Checking the lock status must be read-only
    # because Streamlit reruns the script before every form submission.
    locked_until = float(state.get(LOCKED_UNTIL_KEY, 0.0))
    if locked_until and locked_until <= now:
        state.pop(LOCKED_UNTIL_KEY, None)
        state[FAILED_ATTEMPTS_KEY] = 0

    attempts = int(state.get(FAILED_ATTEMPTS_KEY, 0)) + 1
    state[FAILED_ATTEMPTS_KEY] = attempts
    if attempts >= MAX_FAILED_ATTEMPTS:
        state[LOCKED_UNTIL_KEY] = now + LOCKOUT_SECONDS
        return LOCKOUT_SECONDS
    return 0


def clear_failed_logins(state) -> None:
    state.pop(FAILED_ATTEMPTS_KEY, None)
    state.pop(LOCKED_UNTIL_KEY, None)


def require_login(t) -> None:
    """Block until the user authenticates. Stops the script when not logged in."""
    if is_authenticated():
        return

    configured = get_configured_password()
    if configured is None:
        st.error(t("auth_secrets_missing"))
        st.info(t("auth_secrets_help"))
        st.stop()

    remaining = lockout_remaining(st.session_state)
    if remaining:
        st.warning(t("auth_locked", seconds=remaining))
        st.stop()

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown(f"### {t('login_title')}")
        st.caption(t("login_caption"))
        with st.form("login_form"):
            password = st.text_input(t("password"), type="password")
            submitted = st.form_submit_button(t("sign_in"), type="primary", width="stretch")

        if submitted:
            if hmac.compare_digest(password, configured):
                clear_failed_logins(st.session_state)
                st.session_state[AUTH_KEY] = True
                st.rerun()
            else:
                lockout = record_failed_login(st.session_state)
                if lockout:
                    st.warning(t("auth_locked", seconds=lockout))
                else:
                    st.error(t("auth_invalid"))

    st.stop()
