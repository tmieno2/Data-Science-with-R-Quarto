# The submission form

An Apps Script web app that replaces the old Dropbox file request. A student
opens one URL, gives their name and email, picks the assignment from a dropdown
and uploads their files. Each file is written into a Google Drive folder, which
the repository reaches through a symlink at `assignments/submission` (the
repository itself lives on local disk; see `CLAUDE.md` at the repository root).
Each file lands in

```
assignments/submission/<year>/<assignment>/
```

which is exactly the tree `assignments/sort-submissions.R` produces, so grading
is unchanged. The repository lives on local disk and `assignments/submission`
is a symlink into that Drive folder, so a file uploaded through the form syncs
down and appears there with no further step — the same property the Dropbox
request had, without a sync client watching the rest of the course.

| File | What it is |
|---|---|
| `Code.gs` | Server side: validation, Drive writes, log, receipt email |
| `Form.html` | The page students see |
| `Materials.gs` | Publishing the year's materials folder — see below |
| `appsscript.json` | Manifest — scopes, timezone, deployment access |
| `test-helpers.js` | `node assignments/webform/test-helpers.js` |

---

## What it guarantees

These are the behaviours worth not breaking. Each one exists because of a way
this can go wrong.

**Nothing is ever overwritten.** A file whose canonical name is already taken
becomes `_v2`, `_v3`, … The grader takes the highest version and the log says
when each arrived. Student work is not in version control and cannot be
recovered if lost, so the form has no path that destroys a file.

**Files are renamed to the convention, server side.** Whatever a student calls
their upload, it is stored as `Mieno_assignment_1.qmd` — the name the
assignments ask for and `sort-submissions.R` reads. Under Dropbox this
depended on students getting it right.

**No deadline is enforced, deliberately.** The binding deadline is the one
printed in the assignment. The form stays open and every upload is timestamped
in the log, so lateness stays a grading decision rather than a locked door.
Do not add a cutoff here.

**An unconfigured form refuses to open.** `doGet` checks that the destination
folder is set and reachable before rendering anything, so a deployment that was
never `setup()`-ed turns students away at the door instead of letting them fill
in a form and upload files that have nowhere to go.

**A failed log write or receipt email never fails an upload.** Both are wrapped
so a student watching the page is never told their work did not arrive when it
did.

**Uploads are serialised through a script lock**, so two students submitting at
the same moment cannot race on folder creation or on the uniqueness check that
keeps one submission from landing on another's name.

**A submission must contain a `.qmd` and the `.html` rendered from it, with the
same name before the extension** (`report.qmd` and `report.html`, as Quarto
names them). Every `.qmd` needs its `.html` and every `.html` its `.qmd`; an
`.rmd` or `.htm` is not accepted at all. The Submit button stays disabled and
the page says which file is missing until that holds. This is enforced in the
browser rather than on the server on purpose: the server handles one file per
request, so by the time it could notice a missing `.html` the `.qmd` would
already be stored and the student would be left with a half-submission.

---

## This course's deployment

Created and deployed on 2026-10-21, in use from Fall 2026:

| | |
|---|---|
| Apps Script project | *Data Science assignment submission*, script id `1tZ7GeBfpMscYi800Q_hulquuZbxlyB5XqyzYLdPxvSY9RQrg6-1YEUgx` |
| Deployment id | `AKfycbzY-DxWZIrZQdBGxogL5JJ_zUJfio_4pdO5FAUmD8yHZQu-bfsTz9DoLq4zbnqC370Tjw` |
| `/exec` URL | `submission.url` in `course-dates.json` |
| Destination folder | `submission.drive_folder_id` in `course-dates.json`, also `DEFAULT_FOLDER_ID` in `Code.gs` |

`.clasp.json` (gitignored, local to this machine) points clasp at the project.
`.claspignore` limits a push to the four files the script needs:
`test-helpers.js` uses Node's `require` and would break every request if it
were pushed. `appsscript.json` sets *Execute as: Me* and *Who has access:
Anyone*, so a deployment needs no settings chosen by hand. "Anyone" means
anonymous, which is required: students should not need a Google account to
hand in work.

### Run `setup()` once — the form refuses to open until you do

Open the project (`clasp open-script` from this folder), select `setup` from
the function dropdown and **Run** it. The values in it are already correct for
this course:

```js
SUBMISSION_FOLDER_ID: DEFAULT_FOLDER_ID,          // the Drive submission folder
MATERIALS_ROOT_ID: DEFAULT_MATERIALS_ROOT_ID,     // see Materials.gs
COURSE_YEAR: '2026',
SEND_RECEIPT: 'true'
```

It prompts for authorisation the first time (your own script asking for your
own Drive), then prints what `checkSetup()` found. Before that the `/exec` URL
answers HTTP 403. Script Properties are read on every request, so `setup()`
takes effect on reload, with no redeploy.

Then submit a test file as yourself and check it lands in
`assignments/submission/<year>/<assignment>/`.

### Changing the code later

```sh
cd assignments/webform
clasp push
clasp redeploy AKfycbzY-DxWZIrZQdBGxogL5JJ_zUJfio_4pdO5FAUmD8yHZQu-bfsTz9DoLq4zbnqC370Tjw
```

`redeploy` updates the existing deployment, which keeps the same `/exec` URL.
`clasp deploy` instead mints a **new** URL and silently orphans the one printed
in every assignment students already have.

---

## Publishing the materials folder

`Materials.gs` is the other direction: `Code.gs` takes work in, this puts work
out. The build writes `assignments/students/<year>/` and Drive syncs it, but a
synced folder is still private. Run **`shareMaterials()`** from the editor and
it makes that year readable by anyone with the link, then prints the link and
the year to paste into the `materials` block of `course-dates.json`.

It refuses rather than shares if the folder contains anything students must not
have. Before flipping sharing it walks the whole tree and rejects any file or
folder named like a key, solution, answer, submission, roster or grade, plus
any `.qmd` still carrying a `::: {.answer}` block — the case a name check alone
misses, because such a file looks perfectly innocent from its filename. A link
handed out cannot be recalled once an answer key has been downloaded, so the
check runs first and the share only happens if it comes back clean.

It shares the **year folder and never its parent**. Sharing
`assignments/students/` would let a student wander into another year and
download the wrong assignment.

Two companions:

- `materialsStatus()` — which years exist and which are shared, changing nothing
- `unshareMaterialsFor('2026')` — withdraw the link. Not the moment the term
  ends: a student finishing late work still needs the files.

The gate is covered by `test-helpers.js`, which runs the real scan over the
real folders on disk — it confirms this year's materials pass and that
`assignments/keys/` is refused.

---

## Rolling the course to a new year

1. Edit the `term` block of `course-dates.json` and rebuild the assignments.
2. Set `COURSE_YEAR` to the new year in *Project Settings → Script Properties*
   (or edit `setup()` and rerun it), then `checkSetup()`.
3. Run `shareMaterials()` and paste its two lines into the `materials` block of
   `course-dates.json`.

Submissions then file under the new year, and the new year's materials are
downloadable. Step 3 is the one that used to be a manual trip through the Share
dialog and got forgotten.

If you forget step 2, the fallback in `courseYear_()` derives the year from the
date on the assumption that the course runs in the fall — so work is misfiled
only if you also change terms. Set the property.

---

## The log

`submission-log`, a Sheet in the root of `assignments/submission/`, gets a row
per file: timestamp, year, assignment, name, email, stored filename, the name
the student uploaded it under, size, and a link.

This is what answers "did it go through", "when", and "which version am I
grading". It is inside `assignments/submission/`, which `.gitignore` excludes,
so it can never be committed — it contains student names and emails.

## Receipts

The student gets a confirmation email listing what was stored. Turn it off by
setting `SEND_RECEIPT` to `false`.

Consumer Gmail allows 100 recipients a day, which a deadline-night rush could
approach. If the quota is hit the upload still succeeds and the page tells the
student to screenshot it instead.

---

## Limits and what happens at them

| | |
|---|---|
| Per file | 25 MB, checked in the browser and again on the server |
| Per submission | 8 files |
| Accepted | `.qmd .html .pdf .r .ipynb .zip` |
| Required | a `.qmd` and an `.html` with the same name before the extension, for every one of either |

Files upload one at a time, in sequence, because a single request carrying all
of them would hit the payload limit. A failure part-way keeps everything
already stored and offers to submit the rest; retrying does not re-upload what
already landed.

Submissions count against **your** Drive storage, not the student's.

---

## When something goes wrong

Run **`selfTest()`** from the editor. It walks the whole server-side path with a
tiny file — properties, folder, year, destination, naming, validation, the Drive
write, the log — and prints either `OK` for every step or `FAILED HERE` with the
real message and stack at the first one that breaks. It trashes its test file
before returning.

That splits the two cases that look identical from the student's side:

- **The form shows "not accepting submissions yet"** — `setup()` has not been
  run, or the folder id it holds cannot be opened. The grey line at the bottom
  of that page says which. Run `setup()`, reload.
- **`selfTest()` fails** — the problem is configuration or permissions. The step
  it stops at says which. A wrong `SUBMISSION_FOLDER_ID` stops it at *root
  folder*; a missing scope stops it at *create file* or *log sheet*.
- **`selfTest()` passes but submitting fails** — the problem is the upload
  request, not the server. Almost always a file too large to travel in one
  `google.script.run` call; the page names the file and its size for that
  reason. Check *Executions* in the Apps Script editor for the matching entry.

After changing anything, remember it is *Deploy → Manage deployments → edit →
Version: New version*. Editing the code alone does not change what the deployed
`/exec` URL serves, so a fix can look like it did nothing.

## Editing the assignment list

`ASSIGNMENTS` at the top of `Code.gs`. Each `id` becomes a folder name, so it
must match the ids used in `course-dates.json` and by `sort-submissions.R`
(`assignment-1`, …, `final-project`). Push, then deploy a **new version** of
the existing deployment.
