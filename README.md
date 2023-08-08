## Note
This is a documentation for API which was developed for job test task from Hummer Systems Co

# API Documentation

## Overview

This API provides functionalities for user authentication and profile management. It includes:

- Sending authentication codes to phone numbers.
- Validating received authentication codes.
- Retrieving profile information, including referral details.
- Activating referral codes.

## Endpoints

### 1. Authentication

**Endpoint**: `/api/auth/`
**Methods**: `POST`

#### POST

**Request Parameters**:

- `phone_number`: The phone number to send the auth code to.
- `auth_code`: The received auth code for authentication.

If `auth_code` is provided, it will check for authentication. If `phone_number` is provided, it will send an authentication code to the phone number.

**Responses**:

- **200 OK**:
  - If authentication is successful: `{'auth_status': 'success'}`
  - If auth code is sent successfully: `{'auth_code_sending_status': 'success'}`
- **403 FORBIDDEN**: If the received auth code is invalid: `{'auth_status': 'failure'}`
- **400 BAD REQUEST**: If neither `phone_number` nor `auth_code` is provided: `{'error': 'Phone number or auth code is required'}`

### 2. ProfileView

**Endpoint**: `/api/profile/`
**Methods**: `GET`, `POST`

#### GET

Retrieves profile information and referral details.

**Responses**:

- **200 OK**: Returns user's profile data including `phone_number`, `own_referral_code`, `activated_referral_code`, and `referrals` - array of referral`s phone numbers.
- **403 FORBIDDEN**: If the user is not authenticated: `{'error': 'You are not authorized'}`

#### POST

Activates a referral code for the authenticated user.

**Request Parameters**:

- `referral_code`: The referral code to activate.

**Responses**:

- **200 OK**: If the referral code is successfully activated: `{'message': 'success'}`
- **403 FORBIDDEN**: If the user is not authenticated: `{'error': 'You are not authorized'}`
- **400 BAD REQUEST**: Possible error messages:
  - If the referral code is already activated: `{'error': 'The referral code has already been activated'}`
  - If no referral code is provided: `{'error': 'Referral code is required'}`
  - If referral code format is wrong: `{'error': 'The format of referral code is wrong'}`
  - If the provided referral code doesn't exist: `{'error': 'Customer with referral code you sent is not exists'}`
  - If a user tries to activate their own code: `{'error': 'You can not activate your own referral code'}`

### 3. MainView

**Endpoint**: `/`
**Methods**: `GET`
  
#### GET

Serves the main template for rendering web interface.

**Responses**:

- **200 OK**: Renders the `index.html` template with the given context.

## Thank you for attention!
