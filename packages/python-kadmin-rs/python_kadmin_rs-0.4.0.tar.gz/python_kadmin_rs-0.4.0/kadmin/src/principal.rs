//! kadm5 principal

use std::{os::raw::c_char, ptr::null_mut, time::Duration};

use chrono::{DateTime, Utc};
use kadmin_sys::*;
#[cfg(feature = "python")]
use pyo3::prelude::*;

use crate::{
    conv::{c_string_to_string, delta_to_dur, ts_to_dt},
    error::{Result, krb5_error_code_escape_hatch},
    kadmin::{KAdmin, KAdminImpl},
};

/// A kadm5 principal
#[derive(Debug)]
#[allow(dead_code)] // TODO: remove me once implemented
#[cfg_attr(feature = "python", pyclass(get_all))]
pub struct Principal {
    name: String,
    expire_time: Option<DateTime<Utc>>,
    last_password_change: Option<DateTime<Utc>>,
    password_expiration: Option<DateTime<Utc>>,
    max_life: Option<Duration>,
    modified_by: String,
    modified_at: Option<DateTime<Utc>>,
    // TODO: enum
    attributes: i32,
    kvno: u32,
    mkvno: u32,
    policy: Option<String>,
    // TODO: figure out what that does
    aux_attributes: i64,
    max_renewable_life: Option<Duration>,
    last_success: Option<DateTime<Utc>>,
    last_failed: Option<DateTime<Utc>>,
    fail_auth_count: u32,
    // TODO: key data
}

impl Principal {
    /// Create a [`Principal`] from [`_kadm5_principal_ent_t`]
    pub(crate) fn from_raw(kadmin: &KAdmin, entry: &_kadm5_principal_ent_t) -> Result<Self> {
        // TODO: make a function out of this
        let name = {
            let mut raw_name: *mut c_char = null_mut();
            let code = unsafe {
                krb5_unparse_name(kadmin.context.context, entry.principal, &mut raw_name)
            };
            krb5_error_code_escape_hatch(&kadmin.context, code)?;
            let name = c_string_to_string(raw_name)?;
            unsafe {
                krb5_free_unparsed_name(kadmin.context.context, raw_name);
            }
            name
        };
        let modified_by = {
            let mut raw_name: *mut c_char = null_mut();
            let code =
                unsafe { krb5_unparse_name(kadmin.context.context, entry.mod_name, &mut raw_name) };
            krb5_error_code_escape_hatch(&kadmin.context, code)?;
            let name = c_string_to_string(raw_name)?;
            unsafe {
                krb5_free_unparsed_name(kadmin.context.context, raw_name);
            }
            name
        };
        Ok(Self {
            name,
            expire_time: ts_to_dt(entry.princ_expire_time)?,
            last_password_change: ts_to_dt(entry.last_pwd_change)?,
            password_expiration: ts_to_dt(entry.pw_expiration)?,
            max_life: delta_to_dur(entry.max_life.into()),
            modified_by,
            modified_at: ts_to_dt(entry.mod_date)?,
            attributes: entry.attributes,
            kvno: entry.kvno,
            mkvno: entry.mkvno,
            policy: if !entry.policy.is_null() {
                Some(c_string_to_string(entry.policy)?)
            } else {
                None
            },
            aux_attributes: entry.aux_attributes,
            max_renewable_life: delta_to_dur(entry.max_renewable_life.into()),
            last_success: ts_to_dt(entry.last_success)?,
            last_failed: ts_to_dt(entry.last_failed)?,
            fail_auth_count: entry.fail_auth_count,
        })
    }

    /// Get the name of the principal
    pub fn name(&self) -> &str {
        &self.name
    }

    /// Change the password of the principal
    pub fn change_password<K: KAdminImpl>(&self, kadmin: &K, password: &str) -> Result<()> {
        kadmin.principal_change_password(&self.name, password)
    }
}
