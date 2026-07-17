# Gharbhanda Management System - Use Case Diagram

## Actors
- **Guest**
- **Rentseeker** (authenticated user with `rentseeker` role)
- **Landlord** (authenticated user with `landlord` role)
- **Admin** (Django admin portal)

## Main Use Cases
- Register
- Login
- Logout
- Browse available homes
- View home details
- Apply for home
- Add rent listing
- View landlord notifications
- View profile
- View about page
- View contact page

## Mermaid Use Case Diagram
```mermaid
usecaseDiagram
    actor Guest
    actor Rentseeker
    actor Landlord
    actor Admin

    Guest --> (Browse available homes)
    Guest --> (View home details)
    Guest --> (Register)
    Guest --> (Login)
    Guest --> (View about page)
    Guest --> (View contact page)

    Rentseeker --> (Browse available homes)
    Rentseeker --> (View home details)
    Rentseeker --> (Apply for home)
    Rentseeker --> (View profile)
    Rentseeker --> (Logout)

    Landlord --> (Add rent listing)
    Landlord --> (View landlord notifications)
    Landlord --> (View profile)
    Landlord --> (Logout)

    Admin --> (Manage models via Django admin)
```

## Notes from your project
- Registration can create either a `rentseeker` or `landlord` role.
- Login redirects rentseekers to `home.html` and landlords to `llhome`.
- Rentseekers can apply for housing through `process_apply`.
- Landlords can view applications/notifications on `llhome`.
- `profile` and `llprofile` pages display logged-in user details.
- Static pages include `about` and `contact`.

## How to use this
1. Open `use_case_diagram.md` in VS Code.
2. Copy the Mermaid diagram into a Markdown preview or diagram tool.
3. Adjust actor labels or use cases to match any extra app features.
