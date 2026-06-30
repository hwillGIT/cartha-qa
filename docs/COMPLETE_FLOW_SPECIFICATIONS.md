# Cartha App — Complete Flow Specifications

**Status:** Comprehensive UI/UX flow specifications from business analysis  
**Date:** 2026-06-30  
**Purpose:** Define WHAT the app should do (before testing IF it does it)  
**Audience:** Developers, QA, Product Managers

---

## Table of Contents

1. [Authentication Flows](#authentication-flows)
2. [Watch Feature](#watch-feature)
3. [Bible Feature](#bible-feature)
4. [Groups Feature](#groups-feature)
5. [Meet Feature](#meet-feature)
6. [Moments Feature](#moments-feature)
7. [Messages Feature](#messages-feature)
8. [Community Feature](#community-feature)
9. [Profile & Settings](#profile--settings)
10. [Navigation & Cross-Feature](#navigation--cross-feature)

---

## Authentication Flows

### AF-1: Sign Up (New User)

**Entry Point:** App launch (not logged in) → "Sign Up" button  
**Users:** New users without Cartha account

**Flow:**

```
1. User taps "Sign Up" button
   → SignUp screen displays

2. Screen shows:
   - Email input field (placeholder: "you@example.com")
   - Password input field (with strength indicator)
   - Confirm password field
   - "Terms of Service" + "Privacy Policy" links (clickable)
   - "Create Account" button (disabled until valid input)
   - "Already have account?" link → Sign In flow

3. User enters email
   → Real-time validation: valid email format check
   → If invalid: error message below field "Invalid email format"
   → If valid: remove error message

4. User enters password
   → Real-time strength indicator:
     🔴 Weak (< 6 chars)
     🟡 Medium (6-11 chars, no special chars)
     🟢 Strong (12+ chars, mixed case, numbers, special chars)
   → Error if < 6 chars: "Password must be at least 6 characters"

5. User confirms password
   → Real-time check: Does it match first password?
   → If mismatch: error "Passwords don't match"
   → If match: remove error

6. User taps "Create Account"
   → Loading state: "Creating account..." spinner
   → API call: POST /auth/signup with {email, password}
   
   **Success (2xx):**
   → Next screen: "Verify Your Email"
   → Message: "We've sent a verification link to {email}. Check your inbox."
   → Button: "Open Email App" (opens default email client)
   → Button: "Already Verified?" (if user already clicked link)
   → Countdown timer: "Resend verification in 30s"
   
   **Failure (400):**
   → Error message: "Email already in use" (if email exists)
   → Error message: "Password doesn't meet requirements" (if server validation fails)
   → User can correct and retry
   
   **Failure (5xx):**
   → Generic error: "Something went wrong. Please try again."
   → Retry button
   → Back button

7. User verifies email (via link)
   → Email link: cartha.com/verify?token=XXX
   → Link valid for 24 hours
   → After click, user redirected to app
   → If using web: prompt to "Open in Cartha App"
   
8. User returns to "Verify Your Email" screen
   → Taps "Already Verified?"
   → App checks if email is verified via API
   
   **If verified:**
   → Success: "Email verified!"
   → Auto-advance to profile setup (AF-2)
   
   **If not verified:**
   → Error: "Verification link not yet clicked. Check your email."
   → Show "Resend Verification" option

---

### AF-2: Sign Up (Profile Setup)

**Entry Point:** After email verification (AF-1 step 8)  
**Users:** New users with verified email

**Flow:**

```
1. Profile Setup screen displays

2. Screen shows:
   - Full Name input (placeholder: "John Doe")
   - Profile Photo upload button
     - Camera icon + "Add Photo" button
     - Shows selected photo or placeholder avatar
   - Birthday picker (MM/DD/YYYY)
   - Gender selector (Male / Female / Non-binary / Prefer not to say)
   - Bio text field (max 150 chars, counter shown)
   - "Save Profile" button
   - "Skip for now" link

3. User fills in name
   → Validation: min 2 chars, max 50 chars
   → If < 2: error "Name too short"
   → If > 50: warning "Name truncated to 50 chars"

4. User taps "Add Photo"
   → Camera / Photo Library picker
   → User selects image
   → Image crops to 1:1 square (with manual adjustments)
   → Preview shown in circular frame
   → "Save Photo" / "Cancel" buttons

5. User selects birthday
   → Date picker: Year (1940-2020), Month (1-12), Day (1-31)
   → Age calculated and shown: "Age: 25 years"
   → Validation: Must be 13+ years old
   → If < 13: error "You must be at least 13 years old"

6. User selects gender
   → Radio buttons: Male / Female / Non-binary / Prefer not to say
   → Can change selection anytime

7. User enters bio
   → Text input, max 150 chars
   → Character counter: "42/150 characters"
   → Supports basic text (no special formatting)

8. User taps "Save Profile"
   → Loading: "Saving profile..." spinner
   → API call: POST /users/profile with {name, birthday, gender, bio, photo_url}
   
   **Success (2xx):**
   → Auto-advance to onboarding carousel (AF-3)
   → Profile saved
   
   **Failure (400):**
   → Field-specific error: "Name is required"
   → User can fix and retry
   
   **Failure (5xx):**
   → Generic error: "Failed to save profile. Try again."

9. "Skip for now" option
   → User can skip profile setup
   → Advances to onboarding carousel (AF-3)
   → Profile can be completed later in settings

---

### AF-3: Onboarding Carousel

**Entry Point:** After sign up completion or on first app launch (new user)  
**Users:** New users, first time in app

**Flow:**

```
1. Onboarding carousel displays with 5-6 screens

2. Screen 1: "Welcome to Cartha"
   - Title: "Welcome to Cartha"
   - Image: App logo / happy person
   - Description: "Connect with your faith community, watch Christian content, study the Bible together."
   - Buttons: "Next" / "Skip"

3. Screen 2: "Watch"
   - Title: "Watch Christian Content"
   - Image: Watch feature screenshot
   - Description: "Browse inspiring videos, sermons, and teachings from trusted Christian creators."
   - Buttons: "Next" / "Skip"

4. Screen 3: "Bible"
   - Title: "Study the Bible Together"
   - Image: Bible feature screenshot
   - Description: "Read scripture, join Bible studies, and discuss with your community."
   - Buttons: "Next" / "Skip"

5. Screen 4: "Groups"
   - Title: "Connect in Groups"
   - Image: Groups feature screenshot
   - Description: "Join groups with your church, small group, or community."
   - Buttons: "Next" / "Skip"

6. Screen 5: "Meet"
   - Title: "Audio & Video Rooms"
   - Image: Meet feature screenshot
   - Description: "Join live audio rooms, prayer sessions, and video conversations."
   - Buttons: "Next" / "Skip"

7. Screen 6: "Ready to Go!"
   - Title: "You're All Set!"
   - Image: Cartha logo / celebration
   - Description: "You're ready to connect with your faith community."
   - Button: "Let's Go!" (advances to home)
   - Alternative: "Explore Cartha" or "Start Watching"

8. "Skip" on any screen
   → Advances directly to home (BottomNav)
   → User can always re-watch onboarding via Settings → Help → Onboarding

---

### AF-4: Sign In (Existing User)

**Entry Point:** App launch (not logged in) → "Sign In" button  
**Users:** Existing users with Cartha account

**Flow:**

```
1. Sign In screen displays

2. Screen shows:
   - Email input (placeholder: "you@example.com")
   - Password input (hidden text, eye icon to toggle visibility)
   - "Forgot Password?" link
   - "Sign In" button (disabled until valid input)
   - "Don't have account?" link → Sign Up flow

3. User enters email
   → Real-time validation: valid email format check

4. User enters password
   → Hidden text input with eye icon to toggle visibility

5. User taps "Sign In"
   → Loading: "Signing in..." spinner
   → API call: POST /auth/signin with {email, password}
   
   **Success (2xx):**
   → JWT token stored securely (encrypted storage)
   → User redirected to home (BottomNav)
   → If user was on a gated route: redirect to that route
   
   **Failure (401):**
   → Error message: "Email or password incorrect"
   → User can retry
   → "Forgot Password?" visible
   
   **Failure (403):**
   → If account suspended: "Your account has been suspended. Contact support."
   → Support link provided
   
   **Failure (5xx):**
   → Generic error: "Something went wrong. Please try again."

6. "Forgot Password?" flow
   → User enters email
   → App sends reset link to email
   → User clicks link and sets new password
   → User signs in with new password
   → (See AF-5 below)

---

### AF-5: Forgot Password

**Entry Point:** Sign In screen → "Forgot Password?" link  
**Users:** Users who forgot password

**Flow:**

```
1. "Forgot Password?" screen displays

2. Screen shows:
   - Email input (placeholder: "you@example.com")
   - Description: "Enter your email and we'll send a password reset link."
   - "Send Reset Link" button
   - "Back to Sign In" link

3. User enters email
   → Real-time validation: valid email format

4. User taps "Send Reset Link"
   → Loading: "Sending reset link..." spinner
   → API call: POST /auth/forgot-password with {email}
   
   **Success (2xx):**
   → Confirmation screen: "Check your email"
   → Message: "We've sent a password reset link to {email}."
   → Sub-message: "Link expires in 1 hour."
   → Button: "Open Email App"
   → Button: "Back to Sign In"
   
   **Failure (404):**
   → Still show success message (don't reveal if email exists)
   → Prevents account enumeration attacks
   
   **Failure (5xx):**
   → Error: "Failed to send reset link. Try again."

5. User clicks reset link in email
   → Link: cartha.com/reset-password?token=XXX
   → Token valid for 1 hour
   → If expired: "Reset link expired. Request a new one."

6. Password Reset screen displays
   - New password input
   - Confirm password input
   - Password strength indicator
   - "Reset Password" button

7. User enters new password
   → Strength indicator shown
   → Must be 6+ chars, preferably strong

8. User taps "Reset Password"
   → Loading: "Resetting password..." spinner
   → API call: POST /auth/reset-password with {token, password}
   
   **Success (2xx):**
   → Success screen: "Password reset!"
   → Message: "Your password has been updated. Sign in with your new password."
   → Button: "Sign In"
   → Auto-redirect to Sign In after 3s
   
   **Failure (400 - Token expired):**
   → Error: "Reset link expired. Request a new one."
   → Button: "Back to Forgot Password"
   
   **Failure (5xx):**
   → Generic error: "Failed to reset password. Try again."

---

### AF-6: Session Management & Token Refresh

**Context:** User is signed in, token may expire  
**Automatic:** Happens in background without user interaction

**Flow:**

```
1. User signs in
   → JWT token received (e.g., 24h expiry)
   → Refresh token stored (e.g., 30d expiry)

2. While user is in app:
   → Token used for API calls
   → 5 minutes before expiry: automatic refresh
   → API call: POST /auth/refresh with {refresh_token}
   
   **Success (2xx):**
   → New token issued
   → Old token discarded
   → User continues uninterrupted
   
   **Failure (401):**
   → Refresh token invalid/expired
   → User signed out
   → Redirect to Sign In screen
   → Message: "Session expired. Please sign in again."

3. If token expires mid-action:
   → API call fails with 401
   → App catches error
   → User redirected to Sign In screen
   → Message: "Your session expired. Please sign in again."
   → After sign in: user redirected back to where they were
   
4. Sign Out:
   → User taps "Sign Out" in Settings
   → Confirmation: "Are you sure?"
   → Token deleted from device
   → API call: POST /auth/logout (optional, for server tracking)
   → Redirect to Sign In screen

---

## Watch Feature

### WF-1: Browse Videos (Home Feed)

**Entry Point:** App home, BottomNav → "Watch"  
**Users:** Any user (signed in or anonymous)

**Flow:**

```
1. Watch home screen displays

2. Screen layout:
   - Header: "Watch" title
   - Search bar: "Search videos, creators, topics..."
   - Category carousel (horizontal scroll):
     - All, Sermons, Music, Testimonies, Teachings, Worship, Kids
   - Video feed (vertical scroll):
     - Each video card shows:
       * Thumbnail image
       * Title (max 2 lines)
       * Creator name + verified badge (if applicable)
       * Duration (e.g., "12:34")
       * Watch count (e.g., "1.2K views")
       * Favorite button (heart icon)

3. User scrolls through feed
   → Videos load in batches (pagination)
   → Loading state: skeleton loaders or spinners
   → Infinite scroll: more videos load as user scrolls

4. User selects category
   → Filter feed to show only that category
   → Selected category highlighted
   → Feed updates with new videos
   → Scroll position resets to top
   → "All" shows unfiltered content

5. User taps on video card
   → Navigation to Video Player (WF-2)
   → Video ID/slug passed in route
   → Example: /watch/video/sermon-on-the-mount-123

6. User taps search bar
   → Navigation to Video Search (WF-3)
   → Search screen displays

7. User taps favorite button (heart)
   → Heart fills in (liked)
   → Heart empties (unliked)
   → API call: PUT /videos/{id}/favorite
   
   **Success:**
   → State updates immediately
   → Counter increments/decrements
   
   **Failure (not logged in):**
   → Show sign-in modal
   → "Sign in to save favorites"
   
   **Failure (network):**
   → Show error toast: "Failed to save favorite"
   → Allow retry

8. Empty state (no videos):
   → If category has no videos: "No videos in this category"
   → Button: "Explore all videos"
   → Or: "More content coming soon"

---

### WF-2: Watch Video (Player)

**Entry Point:** From Video Feed (WF-1) → tap video  
**Route:** /watch/video/{id}  
**Users:** Any user

**Flow:**

```
1. Video Player screen displays
   - Full-screen video player (CanvasKit/WebGL on Flutter Web)
   - Play/pause button
   - Progress bar with seek functionality
   - Duration shown (e.g., "12:34 / 45:00")
   - Volume control
   - Full-screen button
   - More options menu (...)

2. Video metadata displayed:
   - Title
   - Creator name + avatar + follow button
   - Description (collapsible, "Show more" / "Show less")
   - Like/favorite button
   - Share button
   - Comment count
   - Watch count

3. User plays video
   → Video streams from server
   → Playback quality auto-selects based on network
   → User can select quality: Auto, 1080p, 720p, 480p, 360p

4. User pauses/resumes
   → State saved (timestamp)
   → If user leaves and returns: resume from saved timestamp
   → Message: "Resume from 5:23?" / "Start from beginning?"

5. User seeks (drags progress bar)
   → Playback jumps to position
   → Scrubbing frame shown (optional)
   → If seeking past downloaded: loading indicator

6. User taps full-screen
   → Video expands to full screen
   → Orientation: auto-rotates to landscape
   → Controls hide after 3s of inactivity (tap to show)

7. Video ends
   → Play button shows over frame
   → "Up Next: {next_video}" card appears after 5s
   → Auto-plays next video after 10s countdown
   → "Cancel" button to stop auto-play
   → Related videos carousel shown below

8. User taps more menu (...)
   → Options:
     - Download (if available)
     - Add to playlist
     - Report video
     - Share
     - Close

9. User taps follow (creator)
   → If not logged in: show sign-in modal
   → If logged in:
     - Button changes to "Following"
     - API call: POST /creators/{id}/follow
     - Success: confirmation notification
     - Failure: error toast

10. User taps like/favorite
    → Same as WF-1 step 7

11. User taps share
    → Share sheet with:
      - Copy link
      - Share via Messages / iMessage / WhatsApp / Email
      - Share to social media (if installed)

12. Comments section (below video)
    → Shows top comments
    → "Load more comments" button
    → If not logged in: "Sign in to comment"
    → If logged in:
      - Comment input field
      - User can reply to comments
      - Nested threads (optional)

---

### WF-3: Search Videos

**Entry Point:** From Watch home (WF-1) → tap search bar  
**Route:** /watch/search  
**Users:** Any user

**Flow:**

```
1. Search screen displays
   - Search input field (focused by default, keyboard open)
   - Recent searches (if any) displayed as chips
   - Popular searches or categories (fallback if no input)

2. User types search query
   → Real-time search suggestions appear (debounced 300ms)
   → Suggestions show:
     - Video titles
     - Creator names
     - Topic tags
   → Loading state: spinner or skeleton loaders

3. User taps suggestion or presses "Search"
   → Results page displays
   → Results show:
     - Matching videos (most relevant first)
     - Matching creators
     - Matching topics/tags
   → Results count: "Found 42 videos"

4. User filters results
   → Filter options:
     - Category (dropdown)
     - Date range (This week / Month / Year / All time)
     - Duration (Short < 5m, Medium 5-15m, Long > 15m)
     - Sorted by: Relevance, Latest, Most watched, Trending
   → Selected filters shown as chips (dismissible)

5. User scrolls through results
   → Pagination: load more as scrolling
   → Each result is a video card (same as WF-1)

6. User taps video result
   → Navigate to Video Player (WF-2)

7. No results found
   → Message: "No videos found for '{query}'"
   → Suggestions: "Try a different search" / "Browse categories"

8. Recent searches
   → Saved locally on device
   → User can clear individual searches (x button)
   → User can clear all (Settings → Clear search history)

---

## Bible Feature

### BF-1: Browse Books

**Entry Point:** App home, BottomNav → "Bible"  
**Users:** Any user

**Flow:**

```
1. Bible home screen displays

2. Screen layout:
   - Header: "Bible"
   - Translation selector: "King James Version" (dropdown)
   - Search bar: "Search books, chapters, verses..."
   - Book grid (2-3 columns):
     - Each book card shows:
       * Book name (e.g., "Genesis")
       * Chapter count (e.g., "50 chapters")
       * Icon or color-coded category (OT/NT)

3. Available translations:
   - King James Version (KJV)
   - New King James Version (NKJV)
   - English Standard Version (ESV)
   - New American Standard Bible (NASB)
   - The Message (MSG)
   - Other popular translations (user selectable)

4. User selects translation
   → All displayed books/verses change to new translation
   → Selection persisted (saved in local storage)
   → API call optional (if syncing preferences)

5. User scrolls through books
   → Books organized by:
     - Old Testament (39 books)
     - New Testament (27 books)
   → Sections collapsible / expandable

6. User searches for book
   → Type book name (e.g., "Genesis" or "Gen")
   → Auto-complete suggestions
   → Filter books in real-time
   → User taps suggestion or presses enter
   → Navigate to that book (BF-2)

7. User taps on book card
   → Navigate to Chapters view (BF-2)
   → Route: /bible/{book_slug}
   → Example: /bible/genesis

---

### BF-2: View Book / Chapters

**Entry Point:** From Books grid (BF-1) → tap book  
**Route:** /bible/{book_slug}  
**Users:** Any user

**Flow:**

```
1. Book / Chapters screen displays

2. Screen layout:
   - Header: Book name (e.g., "Genesis")
   - Translation selector (same as BF-1)
   - Chapter grid (2-3 columns):
     - Each chapter card shows:
       * Chapter number
       * Verse count (e.g., "50 verses")
   - Back button to Books grid

3. User taps chapter
   → Navigate to Chapter/Verse view (BF-3)
   → Route: /bible/{book_slug}/{chapter}
   → Example: /bible/genesis/1

4. User can also search within book
   → Search bar: "Search this book..."
   → Results show matching verses with highlights

5. Book info sidebar (optional, swipe left)
   → Book description
   → Author (if known)
   → Writing period
   → Theme/subject

---

### BF-3: Read Chapter / Verses

**Entry Point:** From Chapters grid (BF-2) → tap chapter  
**Route:** /bible/{book_slug}/{chapter}  
**Users:** Any user

**Flow:**

```
1. Chapter / Verses screen displays

2. Screen layout:
   - Header: "Genesis 1" (book + chapter)
   - Translation selector
   - Chapter navigation: "< Previous" | Chapter selector | "Next >"
   - Verses displayed in readable format:
     * Verse number (e.g., "1")
     * Verse text
     * Highlight on selected verse (if tapped)

3. User reads verses
   → All verses visible in one scroll view
   → Font size adjustable (Settings → Text Size)
   → Color scheme adjustable: Light / Dark (Settings)
   → Line spacing adjustable (Settings)

4. User taps on verse
   → Verse highlights
   → Verse options menu:
     - Bookmark (add/remove)
     - Highlight color (yellow, blue, pink, green)
     - Add note
     - Share verse
     - Copy to clipboard
   → Menu appears as overlay or bottom sheet

5. User bookmarks verse
   → Bookmark icon fills in
   → Bookmarks saved to user account (if logged in)
   → Or saved locally (if not logged in)
   → Bookmark list accessible from Settings

6. User highlights verse
   → Select color
   → Verse text highlights in that color
   → Highlighting saved to user account
   → "Show/hide highlights" toggle

7. User adds note to verse
   → Taps "Add note" option
   → Modal/sheet opens:
     - Text input for note
     - "Save" / "Cancel" buttons
   → Note saved and associated with verse
   → Indicator on verse shows it has note (icon)
   → Note visible when tapping verse again

8. User shares verse
   → Share sheet with:
     - Copy verse text
     - Share via Messages / Email / Social media
   → Shared text includes: verse text, reference, translation name

9. User switches chapters
   → Taps "Previous" or "Next" buttons
   → New chapter loads
   → Scroll position resets to top
   → Or saved position if returning

10. User switches translation
    → All verses switch to new translation
    → Same chapter position maintained

11. Search within chapter
    → Search bar: "Search this chapter..."
    → Results highlight matching verses
    → User can jump to result

12. Bible study mode (optional)
    → Pop-up definitions for theological terms
    → Cross-references to related verses
    → Commentary snippets (if available)
    → Prayer prompts

---

### BF-4: Bookmarks & Notes

**Entry Point:** Settings → Bible → Bookmarks / My Notes  
**Route:** /bible/bookmarks, /bible/notes  
**Users:** Logged-in users

**Flow:**

```
1. Bookmarks screen displays
   - List of bookmarked verses
   - Each item shows:
     * Verse reference (e.g., "Genesis 1:1")
     * Verse text (truncated)
     * Date bookmarked
     * Delete button (x)

2. User scrolls through bookmarks
   → Organized by:
     - Date added (newest first)
     - Or by book (Genesis, Exodus, etc.)
     - User selectable sorting

3. User taps bookmark
   → Navigate to that verse (BF-3)
   → Verse highlighted/selected

4. User deletes bookmark
   → Taps x button
   → Confirmation: "Remove bookmark?"
   → Bookmark removed

5. My Notes screen displays
   - List of verses with notes
   - Each item shows:
     * Verse reference
     * Note preview (first 50 chars)
     * Date created

6. User taps note
   → Navigate to verse (BF-3)
   → Note displayed in sidebar

7. User edits note
   → Taps note text
   → Modal opens with full note text
   → Edit note content
   → "Save" / "Cancel" buttons

---

## Groups Feature

### GF-1: Browse Groups (Home)

**Entry Point:** App home, BottomNav → "Messages" (or tab within)  
**Route:** /groups (or /messages/groups)  
**Users:** Logged-in users

**Flow:**

```
1. Groups home screen displays

2. Screen layout:
   - Header: "Groups" or "My Groups"
   - "Join a Group" button
   - "Create Group" button (if user is admin)
   - Tabs: "My Groups" | "Discover"
   - Group list:
     - Each group card shows:
       * Group name
       * Group avatar/icon
       * Member count (e.g., "234 members")
       * Unread message count (if any)
       * Last message preview
       * Mute/unmute toggle

3. "My Groups" tab
   → Shows groups user is member of
   → Sorted by: Pinned (first), most recent activity
   → User can pin/unpin groups
   → Swipe to reveal options: Pin / Mute / Leave

4. "Discover" tab
   → Shows groups user can join
   → Categories or search
   → Each group shows: name, member count, description, "Join" button

5. User taps group
   → Navigate to Group Chat (GF-2)
   → Group messages displayed

6. User taps "Join a Group" button
   → Navigate to Join Group (GF-3)

7. User taps "Create Group" button (if admin)
   → Navigate to Create Group (GF-4)

8. Empty state (no groups)
   → Message: "You haven't joined any groups yet"
   → Button: "Join a Group" / "Create Group"

---

### GF-2: Group Chat

**Entry Point:** From Groups home (GF-1) → tap group  
**Route:** /groups/{group_id}  
**Users:** Group members

**Flow:**

```
1. Group Chat screen displays

2. Screen layout:
   - Header: Group name, Group settings button (...)
   - Message history (infinite scroll up = earlier messages)
   - Message input field:
     * Text input
     * Send button
     * Attach media button (photo, video, file)
   - Each message shows:
     * Sender avatar + name
     * Message text
     * Timestamp
     * Reaction emojis (if any)
     * Edit/delete buttons (for own messages)

3. User sends message
   → Type message text
   → Tap "Send" or press Enter
   → Loading state: sending indicator
   → Message appears in chat immediately (optimistic update)
   → API call: POST /groups/{id}/messages
   
   **Success:**
   → Message confirmed (checkmark)
   → Timestamp shows sent time
   
   **Failure:**
   → Error: "Failed to send message. Retry?" button
   → User can retry

4. User deletes message (own message only)
   → Long press or three-dot menu
   → Confirmation: "Delete message?"
   → Message replaced with "This message was deleted"
   → Deleted for all group members

5. User edits message (own message)
   → Tap message → "Edit" option
   → Message text becomes editable
   → "Save" / "Cancel" buttons
   → Edited indicator "(edited)" shown

6. User reacts to message
   → Long press message → emoji picker
   → Select emoji
   → Reaction appears below message
   → Tap emoji to remove reaction

7. User scrolls up (earlier messages)
   → Messages load in batches
   → Pagination: load older messages as scrolling
   → Loading indicator: "Loading older messages..."

8. User mentions someone
   → Type "@" in message
   → Auto-complete list of group members
   → Select member
   → @mention inserted, tagged user notified

9. Group settings (... menu)
   → Options:
     - Group Info (name, description, members)
     - Mute group (notifications off)
     - Pin/Unpin group
     - Leave group
     - Report group (if not admin)
     - Delete group (if admin)

10. Notifications
    → Default: On (user gets notified on new messages)
    → Can mute group or mute all notifications in Settings
    → Notification shows: group name + message preview

11. Unread messages
    → Badge count on group card (GF-1)
    → Badge shows unread message count
    → Badge clears when user opens group

---

### GF-3: Join Group (by Code)

**Entry Point:** From Groups home (GF-1) → "Join a Group" button  
**Route:** /groups/join  
**Users:** Logged-in users

**Flow:**

```
1. Join Group screen displays

2. Screen layout:
   - Header: "Join a Group"
   - Text: "Ask your group leader for the group code."
   - Group code input field (placeholder: "Enter code")
   - "Join" button (disabled until valid code entered)
   - "Discover Groups" button (navigate to GF-1 Discover tab)

3. User enters group code
   → Validation: code format (alphanumeric, case-insensitive)
   → Real-time validation: code length check
   → If invalid format: "Invalid code format"

4. User taps "Join"
   → Loading: "Joining group..." spinner
   → API call: POST /groups/join with {code}
   
   **Success (2xx):**
   → Success screen: "Welcome to {group_name}!"
   → Group icon shown
   → Member count: "You're now 1 of {N} members"
   → Button: "Go to Group" (navigates to GF-2)
   → Button: "Back" (returns to Groups home)
   
   **Failure (404):**
   → Error: "Group code not found"
   → Sub-message: "Check the code and try again"
   → Retry button
   
   **Failure (400):**
   → Error: "You're already a member of this group"
   → Button: "Go to Group"
   
   **Failure (403):**
   → Error: "You can't join this group"
   → Sub-message: "Ask your group leader for permission"
   
   **Failure (5xx):**
   → Generic error: "Failed to join group. Try again."

5. Deep-link: Sharing group code
   → URL: /groups/join?code=GROUPCODE
   → Or: /groups/GROUPCODE (simplified)
   → If user not logged in: redirect to sign-in, then join flow
   → If already member: show "Already a member" message

---

### GF-4: Create Group (Admin Only)

**Entry Point:** From Groups home (GF-1) → "Create Group" button  
**Route:** /groups/create  
**Users:** Specific user roles (can create groups)

**Flow:**

```
1. Create Group screen displays

2. Screen layout:
   - Header: "Create Group"
   - Group name input (placeholder: "e.g., Sunday Small Group")
   - Group description input (placeholder: "What's this group about?")
   - Group avatar upload
   - Privacy selector: Public / Private
   - Category selector (optional)
   - "Create" button

3. User enters group name
   → Validation: min 2 chars, max 50 chars
   → Real-time character counter

4. User enters description
   → Optional field
   → Max 500 chars
   → Character counter

5. User uploads avatar
   → Camera / Photo library
   → Image crops to 1:1 square
   → Preview shown

6. User selects privacy
   → Public: Anyone can discover and request to join
   → Private: Only invited members
   → Radio buttons

7. User selects category (optional)
   → Dropdown: Church, Small Group, Bible Study, Prayer, Worship, Kids, etc.

8. User taps "Create"
   → Loading: "Creating group..." spinner
   → API call: POST /groups with {name, description, avatar, privacy, category}
   
   **Success (2xx):**
   → Success screen: "Group created!"
   → Group code displayed (copy to clipboard button)
   → Message: "Share this code with members to invite them"
   → Button: "Go to Group" (navigates to GF-2)
   → Button: "Copy Code & Share" (opens share sheet)
   
   **Failure (400):**
   → Field-specific error: "Group name is required"
   → User can fix and retry
   
   **Failure (5xx):**
   → Generic error: "Failed to create group. Try again."

---

## Meet Feature

### MF-1: Meet Home

**Entry Point:** App home, BottomNav → "Meet"  
**Route:** /meet  
**Users:** Logged-in users

**Flow:**

```
1. Meet home screen displays

2. Screen layout:
   - Header: "Meet"
   - "Create Room" button (prominent)
   - "Browse Rooms" button
   - Active rooms section:
     * "Active Now" header
     * List of live rooms:
       - Room name
       - Participant count (e.g., "12 in room")
       - "Join" button
   - Recent rooms section:
     * "Your Rooms" or "Recent"
     * List of rooms user has been in:
       - Room name
       - Participant count
       - Date last visited
       - "Join" button

3. User taps "Create Room"
   → Navigate to Create Room (MF-2)

4. User taps "Browse Rooms"
   → Navigate to Browse Rooms (MF-3)

5. User taps "Join" on active room
   → Navigate to Room (MF-4)
   → Permissions check: request microphone, camera access

6. Empty state
   → If no active or recent rooms:
   → Message: "No rooms available. Create one or browse available rooms."
   → Buttons: "Create Room" / "Browse Rooms"

---

### MF-2: Create Room

**Entry Point:** From Meet home (MF-1) → "Create Room"  
**Route:** /meet/create  
**Users:** Logged-in users

**Flow:**

```
1. Create Room screen displays
   - Must be logged in to access
   - If logged out: show sign-in modal

2. Screen layout:
   - Room name input (placeholder: "Prayer Room", "Bible Study")
   - Room type selector:
     * Audio only
     * Video (optional)
     * Prayer circle
   - Privacy selector: Public / Private (group only)
   - Max participants selector (optional): unlimited / 5 / 10 / 25 / 50
   - Description (optional)
   - "Create" button

3. User enters room name
   → Validation: min 2 chars, max 50 chars

4. User selects room type
   → Audio: audio conference room
   → Video: audio + video capabilities
   → Prayer: audio circle (special UI)

5. User selects privacy
   → Public: anyone can join
   → Private: only group members invited

6. User sets max participants
   → Unlimited (default)
   → Or fixed number (capped)

7. User taps "Create"
   → Loading: "Creating room..." spinner
   → API call: POST /meet/rooms with {name, type, privacy, max_participants}
   
   **Success (2xx):**
   → Success: room created
   → Redirect to Room (MF-4)
   → User is room owner (can manage settings)
   → Room is live (can invite others immediately)
   
   **Failure (5xx):**
   → Error: "Failed to create room. Try again."

---

### MF-3: Browse Rooms

**Entry Point:** From Meet home (MF-1) → "Browse Rooms"  
**Route:** /meet/rooms  
**Users:** Logged-in users

**Flow:**

```
1. Browse Rooms screen displays

2. Screen layout:
   - Header: "Browse Rooms"
   - Filter options:
     * Room type: Audio / Video / Prayer / All
     * Sort by: Active now, Most participants, Newest
   - Room list:
     * Each room shows:
       - Room name
       - Room icon/avatar
       - Participant count (e.g., "5 people")
       - Room type badge (Audio / Video / Prayer)
       - "Join" button

3. User filters rooms
   → Select filter option
   → List updates to show matching rooms
   → Selected filter highlighted

4. User sorts rooms
   → Select sort option
   → List re-sorts

5. User taps "Join"
   → Permissions check: request microphone, camera
   → Navigate to Room (MF-4)

6. User scrolls to load more
   → Pagination: load more rooms as scrolling
   → Loading state: spinners

7. Empty state
   → If no rooms: "No rooms available right now"
   → Message: "Check back later or create your own room"
   → Button: "Create Room"

---

### MF-4: In Room (Audio/Video Call)

**Entry Point:** From Join Room actions (MF-1, MF-3)  
**Route:** /meet/room/{room_id}  
**Users:** Invited participants

**Flow:**

```
1. Room screen displays

2. Screen layout (for audio):
   - Header: Room name
   - Participant list:
     * Each participant shows:
       - Avatar + name
       - Status: Speaking, Muted, etc.
     * Participant count total
   - Your controls at bottom:
     * Microphone toggle (on/off)
     * Camera toggle (if video room)
     * More options (...): Settings, Screen share, etc.
     * Leave button (red)

3. Screen layout (for video):
   - Video grid or dominant speaker view
   - Each participant video:
     * Name overlay
     * Speaking indicator
     * Mute indicator (mic icon if muted)
   - Your video (smaller, in corner)
   - Controls same as audio

4. User joins room
   → Loading: "Connecting..." spinner
   → Microphone/camera requested (permissions)
   → WebRTC connection established (LiveKit or similar)
   → User audio/video enabled by default
   → User appears in participant list

5. User mutes microphone
   → Tap mic button
   → Button turns gray/off
   → Other participants see "Muted" indicator
   → User can still hear

6. User disables camera (video room)
   → Tap camera button
   → Camera turns off
   → Still audio
   → Video placeholder (avatar) shown

7. User unmutes/enables
   → Tap button again
   → Enabled
   → Indicator cleared

8. User shares screen (if available)
   → Tap "Screen share" option
   → Confirmation: "Share your screen?"
   → Screen stream enabled
   → Other participants see shared screen
   → Large view of shared content
   → Your camera in corner

9. User raises hand
   → Tap "Hand" icon
   → Room host notified
   → User's hand shown to others

10. Participants join/leave
    → Real-time updates in participant list
    → Notification: "{name} joined" / "{name} left"

11. User leaves room
    → Tap "Leave" button
    → Confirmation: "Leave room?"
    → Disconnect from call
    → Return to Meet home (MF-1)
    → Or back button

12. Room is full
    → If max participants reached: "Room is full"
    → User cannot join
    → Can wait for slot or try different room

13. Network issues
    → Connection drops: "Reconnecting..." spinner
    → After 10s: "Connection lost. Try again?" with Rejoin button
    → User can rejoin

14. Room ends (host leaves)
    → If room had "max participants", room closes when host leaves
    → Message: "Room has ended"
    → Button: "Back to Meet"

---

## Moments Feature

### MoF-1: Moments Home (Feed)

**Entry Point:** App home, BottomNav → "Moments"  
**Route:** /moments  
**Users:** Logged-in users

**Flow:**

```
1. Moments home screen displays (feed)

2. Screen layout:
   - Header: "Moments"
   - "Create Moment" button (prominent, camera icon)
   - Stories carousel (if stories available)
   - Moments feed (vertical scroll):
     * Each moment shows:
       - Creator avatar + name
       - Time posted (e.g., "2 hours ago")
       - Moment image/video
       - Caption text
       - Like count (e.g., "42 likes")
       - Comment count (e.g., "8 comments")
       - Share button
       - More options (...)

3. User scrolls through moments
   → Load more moments as scrolling
   → Pagination
   → Loading spinners

4. User taps "Create Moment"
   → Navigate to Create Moment (MoF-2)

5. User likes moment
   → Tap heart icon
   → Heart fills in (liked)
   → Like count increments
   → API call: PUT /moments/{id}/like
   → If not logged in: sign-in modal

6. User comments on moment
   → Tap comment icon
   → Navigate to Moment Detail (MoF-3)
   → Comment input auto-focused

7. User shares moment
   → Tap share button
   → Share sheet with:
     - Copy link
     - Share via Messages / Email / Social
   → Shared content: moment image + caption + creator name

8. More options (...):
   → If own moment:
     - Edit
     - Delete
     - View analytics
   → If others' moment:
     - Report
     - Block user
     - Mute user

9. Empty state
   → If no moments: "No moments to show"
   → Message: "Create your first moment or follow others"
   → Buttons: "Create Moment" / "Find People to Follow"

---

### MoF-2: Create Moment

**Entry Point:** From Moments home (MoF-1) → "Create Moment"  
**Route:** /moments/create  
**Users:** Logged-in users

**Flow:**

```
1. Create Moment screen displays
   - Must be logged in

2. Screen layout:
   - Media picker:
     * Camera button (take photo/video)
     * Photo library button (select from library)
     * Canvas (preview of selected media)
   - Caption input field (placeholder: "Share your moment...")
   - Privacy selector: Public / Private / Close friends only
   - "Share" button (disabled until media selected)
   - "Cancel" button

3. User taps camera
   → Camera app opens (native)
   → User takes photo or records video
   → Video max 30s or custom limit
   → Returns to Create Moment screen
   → Media shown in preview

4. User taps photo library
   → Photo picker (native)
   → User selects media from library
   → Returns to Create Moment screen
   → Media shown in preview

5. User can edit media (optional)
   → Crop image
   → Add filters
   → Trim video
   → Rotate

6. User enters caption
   → Text input, max 500 chars
   → Character counter
   → Supports hashtags (#topic) and @mentions

7. User selects privacy
   → Public: Everyone can see
   → Private: Only close friends
   → Close friends only: Only selected close friends
   → Radio buttons

8. User tags location (optional)
   → Tap "Add location" button
   → Location picker (map or search)
   → Location added to moment

9. User taps "Share"
   → Loading: "Uploading..." spinner
   → Video upload (if video): progress bar shown
   → API call: POST /moments with {media, caption, privacy, location, tags}
   
   **Success (2xx):**
   → Success: "Moment shared!"
   → Return to Moments home (MoF-1)
   → New moment appears in feed
   
   **Failure (413 - Too large):**
   → Error: "File too large. Max {size}MB."
   
   **Failure (5xx):**
   → Error: "Failed to upload. Try again?"
   → Retry button
   → Save locally (draft) option

---

### MoF-3: Moment Detail

**Entry Point:** From Moments feed (MoF-1) → tap moment  
**Route:** /moments/{moment_id}  
**Users:** Any user

**Flow:**

```
1. Moment detail screen displays

2. Screen layout:
   - Large moment image/video player
   - Moment metadata:
     * Creator avatar + name + follow button
     * Time posted
     * Caption
     * Location (if added)
     * Like count
     * Comment count
   - Like button
   - Comment section:
     * Existing comments (newest first)
     * "Load more comments" button
     * Comment input field (if logged in)

3. User taps like
   → Same as MoF-1 step 5

4. User views comments
   → Comments displayed with:
     - Commenter avatar + name
     - Comment text
     - Time posted
     - Like button
     - Reply button

5. User comments
   → Tap comment input field
   → Type comment
   → Tap "Post"
   → Loading: sending indicator
   → Comment appears (optimistic update)
   → API call: POST /moments/{id}/comments
   
   **Success:**
   → Comment confirmed
   
   **Failure:**
   → Error: "Failed to post comment. Retry?"

6. User replies to comment
   → Tap "Reply" on comment
   → Reply input field opens (with @mention)
   → User types reply
   → Tap "Post"
   → Reply nested under original comment

7. User deletes own comment
   → Tap ... on own comment
   → "Delete comment" option
   → Confirmation: "Delete?"
   → Comment deleted

8. User follows creator
   → Tap "Follow" button
   → Button changes to "Following"
   → API call: POST /users/{id}/follow

9. Share moment
   → Same as MoF-1 step 7

---

## Messages Feature

### MF-1: Conversations Home

**Entry Point:** App home, BottomNav → "Messages"  
**Route:** /messages  
**Users:** Logged-in users

**Flow:**

```
1. Messages home screen displays

2. Screen layout:
   - Header: "Messages" or "Inbox"
   - "New message" button (compose icon)
   - Conversation list (vertical scroll):
     * Each conversation shows:
       - User avatar
       - User name
       - Last message preview
       - Time (e.g., "2 mins ago")
       - Unread badge (count, if any)
       - Mute toggle

3. User taps conversation
   → Navigate to Chat (MF-2)
   → Messages displayed

4. User taps "New message"
   → Navigate to Compose (MF-3)

5. User swipes conversation (left)
   → Options appear:
     - Pin/Unpin conversation
     - Mute/Unmute
     - Delete

6. User sorts conversations
   → Filter: All / Unread
   → Sort: Recent / Alphabetical / Unread first

7. Search conversations
   → Tap search bar
   → Type name or message keyword
   → Results shown

---

### MF-2: Direct Message Chat

**Entry Point:** From Conversations (MF-1) → tap conversation  
**Route:** /messages/{user_id}  
**Users:** Logged-in users

**Flow:**

```
1. Chat screen displays

2. Screen layout:
   - Header: User name, options menu (...)
   - Message history (scroll up = earlier messages)
   - Message input field:
     * Text input
     * Attach button (media, files)
     * Send button
   - Each message shows:
     * Sender avatar
     * Message text
     * Timestamp
     * Read receipt (1 checkmark = sent, 2 = delivered, filled = read)

3. User sends message
   → Same as GF-2 step 3

4. User sees read receipts
   → 1 checkmark: message sent
   → 2 checkmarks: message delivered to user's device
   → 2 filled checkmarks (blue): message read

5. Typing indicator
   → User sees "User is typing..." when other person types
   → Disappears when person stops typing

6. Photo/media messages
   → User taps attach button
   → Selects photo / video / file
   → Media attached to message
   → User can preview before sending
   → "Send" button sends media + optional caption

7. Sticker/GIF messages (optional)
   → Tap GIF button (if available)
   → Search/browse GIFs
   → Select GIF
   → Sends as media message

8. Delete/Edit message (own messages)
   → Same as GF-2 steps 4-5

9. User blocks/reports
   → Tap ... menu
   → Options:
     - Block user (no more messages)
     - Report user
     - Delete conversation

---

### MF-3: Compose New Message

**Entry Point:** From Conversations (MF-1) → "New message"  
**Route:** /messages/compose  
**Users:** Logged-in users

**Flow:**

```
1. Compose screen displays

2. Screen layout:
   - "To:" field (search/select user)
   - Message input field
   - "Send" button (disabled until recipient selected)

3. User taps "To:" field
   → List of recent contacts
   → Search box to find users
   → User searches for name
   → Results shown with avatars
   → User taps to select

4. User enters message
   → Type message text

5. User taps "Send"
   → Loading: "Sending..." spinner
   → API call: POST /messages with {recipient_id, text}
   
   **Success:**
   → Message sent
   → Redirect to Chat (MF-2) with that user
   → Message appears in conversation
   
   **Failure:**
   → Error: "Failed to send message. Try again?"
   → Message saved as draft
   → User can retry

---

## Navigation & Cross-Feature

### NF-1: Bottom Navigation (BottomNav)

**Context:** Main app navigation, available on most screens  
**Persistent:** Visible on home screens of each feature

**Tabs:**
1. **Watch** → /watch (WF-1)
2. **Bible** → /bible (BF-1)
3. **Moments** → /moments (MoF-1)
4. **Meet** → /meet (MF-1)
5. **Messages** → /messages (MF-1)

**Behavior:**
- Current tab highlighted (color + bold text)
- Tap tab → navigate to that feature home
- Long-press tab → show tab info / quick actions
- Tab icon shows badge (unread count) if applicable

---

### NF-2: Deep-Linking

**Context:** Share links to specific content  
**Scheme:** `app://cartha.com/{route}` or `https://cartha.com/{route}`

**Examples:**

```
/watch/video/sermon-on-mount                → Watch video
/watch/clips/{clip_id}                        → Watch clip

/bible/genesis                                → Genesis book
/bible/genesis/1                              → Genesis chapter 1
/bible/genesis/1:1-10                         → Genesis 1:1-10 (verses)

/groups/{group_id}                            → Group chat
/groups/join?code=GROUPCODE                   → Join group

/meet/room/{room_id}                          → Join meeting room
/meet/create                                  → Create new room

/moments/{moment_id}                          → View moment
/moments/create                               → Create moment

/messages/{user_id}                           → Chat with user
/messages/compose                             → Compose new message

/profile/{user_id}                            → User profile
/settings                                     → Settings
```

**Deep-Link Behavior:**

```
IF user not logged in:
  → Show sign-in screen
  → On successful sign-in: navigate to deep-link destination

IF user logged in:
  → Navigate directly to content
  → If content not found: show error (e.g., "Group not found")
  → If not authorized: show error (e.g., "You can't access this")

IF deep-link is gated (e.g., /plan, /meet/create):
  → If not logged in: show sign-in modal
  → If logged in: check permissions
  → If allowed: navigate to content
  → If not allowed: show error
```

---

### NF-3: Error Handling (Global)

**Invalid Routes:**
```
User navigates to /invalid-route
→ Show in-app 404 page:
  - Title: "Page not found"
  - Description: "We couldn't find that page."
  - Image/icon: 404 illustration
  - Button: "Go Home"
→ NOT redirect to domain
```

**Network Errors:**
```
API call fails (no internet):
→ Show error toast: "No internet connection. Check your network."
→ Retry button
→ Option to continue offline (if cached data available)
```

**Auth Errors:**
```
Token expires:
→ Auto-logout user
→ Redirect to sign-in screen
→ Message: "Your session expired. Please sign in again."

User not authorized (403):
→ Show error message: "You don't have permission to access this."
→ Option: "Go back" / "Contact support"
```

**Feature Not Ready:**
```
If feature not fully implemented (e.g., /meet/rooms):
→ Dead-end route
→ NOT silent fallback to home
→ Show message: "This feature is coming soon. Check back later!"
→ Button: "Explore other features" (back button)
```

---

## Summary

**Total Flows Documented:** 50+

| Feature | Flows | Routes |
|---------|-------|--------|
| Authentication | 6 | /auth/signup, /auth/signin, /auth/forgot-password, /auth/reset-password, /auth/verify |
| Watch | 3 | /watch, /watch/video/{id}, /watch/search, /watch/clips/{id} |
| Bible | 4 | /bible, /bible/{book}, /bible/{book}/{chapter}, /bible/bookmarks, /bible/notes |
| Groups | 4 | /groups, /groups/{id}, /groups/join, /groups/create |
| Meet | 4 | /meet, /meet/create, /meet/rooms, /meet/room/{id} |
| Moments | 3 | /moments, /moments/create, /moments/{id} |
| Messages | 3 | /messages, /messages/{user_id}, /messages/compose |
| Navigation | 3 | BottomNav, Deep-linking, Error handling |

---

**Next Steps:**

1. ✅ Review all flows with product team
2. ✅ Confirm behavior with business stakeholders
3. ✅ Update specs based on feedback
4. ✅ Create test cases for each flow
5. ✅ Verify app matches specs (QA validation)
6. ✅ Document any deviations as "Known Differences"

**Document Version:** 1.0  
**Last Updated:** 2026-06-30  
**Audience:** Development, QA, Product Management
