# Process Model Diagram for Gharbhanda Management System

## Summary
This document describes the main process flows for registration, login, home browsing, applying, and landlord notification management.

## Mermaid Flowchart
```mermaid
flowchart TD
    A[Start] --> B[Open application]
    B --> C{User authenticated?}
    C -- No --> D[Login / Register page]
    D --> E{Select action}
    E -- Register --> F[Fill registration form]
    F --> G[Submit registration]
    G --> H[Create User + assign role]
    H --> I[Redirect to login page]
    E -- Login --> J[Enter username/password]
    J --> K[Authenticate credentials]
    K --> L{Valid user?}
    L -- No --> M[Show login error]
    L -- Yes --> N{User role}
    N -- Rentseeker --> O[Redirect to available homes]
    N -- Landlord --> P[Redirect to landlord home]

    subgraph Rentseeker flow
        O --> Q[Browse available home listings]
        Q --> R[View home details]
        R --> S[Click Apply]
        S --> T[Create Application record]
        T --> U[Show success message]
        U --> Q
    end

    subgraph Landlord flow
        P --> V[Show notifications / applications]
        V --> W[Review application list]
        W --> X[Optional: open profile or logout]
    end

    subgraph Common actions
        N --> Y[View profile]
        Y --> Z[Show profile page]
        Z --> X
    end

    X --> AA[Logout]
    AA --> AB[Return to login page]
    AB --> C
```

## Process Model Details

### 1. User authentication process
- User visits the app.
- If unauthenticated, the app displays `Login` / `Register`.
- Registration creates a Django `User`, assigns the selected `rentseeker` or `landlord` group, and redirects to login.
- Login authenticates credentials and routes the user based on their role.

### 2. Rentseeker process
- Rentseeker lands on `home.html`.
- They browse available homes loaded from `Home.objects.all()`.
- They can view details for a chosen house from `view_details`.
- Applying triggers `process_apply`, which stores an `Application` model record and returns to the home list.

### 3. Landlord process
- Landlord lands on `llhome`.
- The landlord sees `Application` records filtered by `request.user`.
- They can review applications and optionally view their `llprofile` or logout.

### 4. Common pages
- About page: `about.html`
- Contact page: `contact.html`
- Profile page: `profile.html` or `llprofile.html`

## How to view
- Open `process_model_diagram.md` in VS Code to preview the Mermaid diagram.
- Use the flowchart as a reference when drawing a hand-drawn or tool-based process modelling diagram.
