// SPDX-License-Identifier: MPL-2.0
// Copyright (C) 2019 - 2021 Gemeente Amsterdam
import * as Sentry from '@sentry/browser'
import { call, put, takeLatest } from 'redux-saga/effects'

import { showGlobalNotification } from 'containers/App/actions'
import { VARIANT_ERROR, TYPE_LOCAL } from 'containers/Notification/constants'
import { authCall, getErrorMessage } from 'shared/services/api/api'
import CONFIGURATION from 'shared/services/configuration/configuration'

import { fetchDepartmentsSuccess, fetchDepartmentsError } from './actions'
import { FETCH_DEPARTMENTS } from './constants'
import i18n from 'i18n'

export function* fetchDepartments() {
  try {
    const departments = yield call(authCall, CONFIGURATION.DEPARTMENTS_ENDPOINT)
    yield put(fetchDepartmentsSuccess(departments))
  } catch (error) {
    yield put(fetchDepartmentsError(error.message))

    yield put(
      showGlobalNotification({
        title: getErrorMessage(error),
        message: i18n.t('de-lijst-van-afdelingen-kon-niet-opgehaald-worden'),
        variant: VARIANT_ERROR,
        type: TYPE_LOCAL,
      })
    )

    yield call([Sentry, 'captureException'], error)
  }
}

export default function* watchDepartmentsSaga() {
  yield takeLatest(FETCH_DEPARTMENTS, fetchDepartments)
}
