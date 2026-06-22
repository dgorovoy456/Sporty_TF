# TEST PLAN

## Content
* [Overview](#overview)
* [Testing Types](#testing-types)
* [Automation Testing Tools](#automation-testing-tools)
* [API Testing Scenarios](#api-testing-scenarios)
* [UI Testing Scenarios](#ui-testing-scenarios)

---

### Overview
This document describes the manual and automated testing strategies and test specifications for the targeted validation suite.

### Testing Types
* Functional API Verification
* UI End-to-End Testing

### Automation Testing Tools
* **Base framework:** Pytest
* **API testing:** `requests` (Python library)
* **UI testing:** Selenium WebDriver

---

### API Testing Scenarios

#### 1. Test Upcoming Matches API

* **1.1** Test that a valid list of matches is returned for an authorized user.
  * **Pre-conditions:**
    * Valid `x-user-id` is configured.
  * **Test Steps:**
    1. Send a `GET` request to: `https://qae-assignment-tau.vercel.app/api/matches`
    2. Include the header: `x-user-id: <valid_x_user_id>`
    3. Observe the response status code.
    4. Observe the response payload list.
  * **Expected Result:**
    * The request completes with a `200` status code, and the payload contains the list of matches

* **1.2** Test that upcoming matches only are returned.
  * **Test Steps:**
    1. Send a `GET` request to: `https://qae-assignment-tau.vercel.app/api/matches`
    2. Include the header: `x-user-id: <valid_x_user_id>`
    3. Iterate through each returned match and parse its `kickoffDate`.
    4. Compare the `kickoffDate` against the current runtime system timestamp.
  * **Expected Result:**
    * Every single match returned contains a `kickoffDate` set strictly in the future. No historical matches are present.

* **1.3** Verify API security constraints for unauthorized or missing credentials.
  * **Test Steps:**
    1. Send a `GET` request to: `https://qae-assignment-tau.vercel.app/api/matches`
    2. Include the header with **INVALID** user: `x-user-id: <invalid_x_user_id>`
    3. Observe the response status code
    4. Observe the response payload
  * **Expected Result:**
    * The server rejects the call, returning a `401` status code, and `invalid_user_id` error payload.