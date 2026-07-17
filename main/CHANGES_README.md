# What I changed in your project

I kept your app name (`pyapp`), project name (`pyproject`), and model names —
this is your project, restructured and extended, not a rewrite from scratch.

## Bugs fixed

1. **`viewhtml.html`** mixed `house.title` with `vd.location/price/description`
   — only `vd` was ever passed in, so half the page was silently blank. Now
   everything uses `vd` consistently.
2. **Hardcoded WhatsApp number** in `home.html` / `viewhtml.html` — every
   house contacted the same phone number regardless of landlord. Now each
   house shows its *own* landlord's number (`house.landlord.phone`), built at
   registration time.
3. **`add` view's image-upload loop** had `return redirect(...)` indented
   *inside* the `for img in image:` loop — broke silently if 0 photos were
   uploaded. Fixed indentation.
4. **`llhome` view** queried `Application.objects.filter(user=request.user)`
   — but `request.user` there is the *landlord*, and `Application.user` is
   the *roomseeker* who applied, so this always returned nothing. Landlord
   listings and notifications are now two separate, correct views:
   `llhome` (their own houses) and `notify` (applications on those houses).
5. **`notify.html`** was empty; **`not1/2/3.html`** were unused duplicate
   experiments — removed.
6. Removed the standalone `roomseeker` model, which stored its own separate
   hashed password and was **never actually used for login** (real auth
   always went through Django's `User` + Groups). Replaced with
   `RoomSeekerProfile` (same pattern as `landlord`), so it actually holds
   useful data (phone) and shows up properly in admin.

## Features added

**Models** (`pyapp/models.py`)
- `landlord.phone` — used for the WhatsApp/call contact buttons
- `RoomSeekerProfile.phone` — collected at registration
- `Application.status` (`pending` / `accepted` / `declined`)
- `Application.landlord_read` / `seeker_read` — power the notification badges
- `Home.is_available`, `Home.created_at`

**Roomseeker**
- Price filter (`min_price`/`max_price`) + text search on `home.html`
- "Already applied" badge, duplicate applications blocked
- Dynamic WhatsApp + phone contact buttons per house (real landlord number)
- New **My Applications** page (`/my-applications`) — shows pending/accepted/
  declined status for everything they've applied to, with a WhatsApp link to
  message the landlord once accepted

**Landlord**
- `llhome` now correctly shows only *their own* houses
- New **Notifications** page (`/notify`) — every application on their
  houses, with **Accept / Decline** buttons right there
- Sidebar notification badge (unread pending-application count), via
  `pyapp/context_processors.py`

**Admin**
- `landlord`, `RoomSeekerProfile`, `Application`, `Home` all registered with
  useful `list_display`/`list_filter`/`search_fields` so you can manage
  roomseekers, landlords, houses, and applications from `/admin/`
- `HomeImage` shows as an inline on the `Home` admin page

## Setup

```bash
cd project1
python -m venv venv
source venv/bin/activate        # venv\Scripts\activate on Windows
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser   # for /admin/
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`.

**Note:** I reset the migration history to a single clean `0001_initial.py`
(your old migrations had an auto-field type mismatch from Django version
changes that broke SQLite table rebuilds). This means starting from a fresh
database — if you have real data in your current `db.sqlite3` you want to
keep, let me know and I can write a data-preserving migration path instead.

## Testing done

I ran a full scripted walkthrough against a live server: register landlord +
roomseeker (with phones) → landlord adds house → roomseeker filters by price
→ views detail (sees correct dynamic contact) → applies → landlord sees
notification and Accepts → roomseeker's My Applications shows "Accepted" +
WhatsApp link. All working end-to-end.
