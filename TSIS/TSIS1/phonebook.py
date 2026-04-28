# phonebook.py — TSIS 1: Extended Contact Management
# Builds on Practice 7 & 8; adds groups, multi-phone, email,
# birthday, sort, paginated browse, JSON export/import.

import csv
import json
import os
from connect import get_connection


# ──────────────────────────────────────────────────────────────
# DISPLAY HELPER
# ──────────────────────────────────────────────────────────────

def fmt_contact(row):
    """
    Accepts a 7-tuple:
      (id, username, phone, email, birthday, group_name, extra_phones)
    and prints a formatted one-liner.
    """
    cid, name, phone, email, birthday, group_name, extra = row
    parts = [f"ID:{cid:>4}  {name:<22}"]
    if phone:
        parts.append(f"📞 {phone}")
    if extra:
        parts.append(f"[{extra}]")
    if email:
        parts.append(f"✉  {email}")
    if birthday:
        parts.append(f"🎂 {birthday}")
    if group_name:
        parts.append(f"👥 {group_name}")
    print("  " + "  |  ".join(parts))


# ──────────────────────────────────────────────────────────────
# 1. SEARCH BY PATTERN  (DB function: search_contacts)
#    Matches: name, primary phone, email, all phones table rows
# ──────────────────────────────────────────────────────────────

def search_by_pattern(pattern):
    conn = get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
            rows = cur.fetchall()
        print(f"\n── Search: '{pattern}' ──  ({len(rows)} result(s))")
        if not rows:
            print("  No matches found.")
        for row in rows:
            fmt_contact(row)
    except Exception as e:
        print(f"  Search error: {e}")
    finally:
        conn.close()


# ──────────────────────────────────────────────────────────────
# 2. ADD / UPDATE CONTACT  (DB procedure: insert_or_update_contact)
#    Also persists email, birthday, group via UPDATE after upsert.
# ──────────────────────────────────────────────────────────────

def upsert_contact(name, phone, email=None, birthday=None, group_name=None):
    conn = get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            # Practice-8 procedure handles the upsert on phone conflict
            cur.execute("CALL insert_or_update_contact(%s, %s)", (name, phone))

            # Extended fields
            gid = _resolve_group(cur, group_name) if group_name else None
            cur.execute(
                """UPDATE contacts
                   SET email    = COALESCE(%s, email),
                       birthday = COALESCE(%s::DATE, birthday),
                       group_id = COALESCE(%s, group_id)
                   WHERE phone = %s""",
                (email or None, birthday or None, gid, phone),
            )
            conn.commit()
        print(f"  ✓ Contact '{name}' saved.")
    except Exception as e:
        conn.rollback()
        print(f"  Upsert error: {e}")
    finally:
        conn.close()


# ──────────────────────────────────────────────────────────────
# 3. ADD PHONE NUMBER  (DB procedure: add_phone)
# ──────────────────────────────────────────────────────────────

def add_phone(contact_name, phone, phone_type="mobile"):
    conn = get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("CALL add_phone(%s, %s, %s)", (contact_name, phone, phone_type))
            conn.commit()
        print(f"  ✓ Added {phone} ({phone_type}) to '{contact_name}'.")
    except Exception as e:
        conn.rollback()
        print(f"  Error: {e}")
    finally:
        conn.close()


# ──────────────────────────────────────────────────────────────
# 4. MOVE TO GROUP  (DB procedure: move_to_group)
# ──────────────────────────────────────────────────────────────

def move_to_group(contact_name, group_name):
    conn = get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("CALL move_to_group(%s, %s)", (contact_name, group_name))
            conn.commit()
        print(f"  ✓ '{contact_name}' → group '{group_name}'.")
    except Exception as e:
        conn.rollback()
        print(f"  Error: {e}")
    finally:
        conn.close()


# ──────────────────────────────────────────────────────────────
# 5. FILTER BY GROUP
# ──────────────────────────────────────────────────────────────

def filter_by_group(group_name):
    conn = get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT c.id, c.username, c.phone, c.email, c.birthday,
                          g.name,
                          STRING_AGG(ph.phone || ' (' || COALESCE(ph.type,'?') || ')', ', ')
                   FROM contacts c
                   LEFT JOIN groups  g  ON c.group_id   = g.id
                   LEFT JOIN phones  ph ON c.id         = ph.contact_id
                   WHERE g.name ILIKE %s
                   GROUP BY c.id, c.username, c.phone, c.email, c.birthday, g.name
                   ORDER BY c.username""",
                (group_name,),
            )
            rows = cur.fetchall()
        print(f"\n── Group: {group_name} ──  ({len(rows)} contact(s))")
        if not rows:
            print("  No contacts in this group.")
        for row in rows:
            fmt_contact(row)
    except Exception as e:
        print(f"  Filter error: {e}")
    finally:
        conn.close()


# ──────────────────────────────────────────────────────────────
# 6. SEARCH BY EMAIL  (partial match)
# ──────────────────────────────────────────────────────────────

def search_by_email(fragment):
    conn = get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT c.id, c.username, c.phone, c.email, c.birthday,
                          g.name,
                          STRING_AGG(ph.phone || ' (' || COALESCE(ph.type,'?') || ')', ', ')
                   FROM contacts c
                   LEFT JOIN groups  g  ON c.group_id   = g.id
                   LEFT JOIN phones  ph ON c.id         = ph.contact_id
                   WHERE c.email ILIKE %s
                   GROUP BY c.id, c.username, c.phone, c.email, c.birthday, g.name
                   ORDER BY c.username""",
                (f"%{fragment}%",),
            )
            rows = cur.fetchall()
        print(f"\n── Email search: '{fragment}' ──  ({len(rows)} result(s))")
        if not rows:
            print("  No matches.")
        for row in rows:
            fmt_contact(row)
    except Exception as e:
        print(f"  Email search error: {e}")
    finally:
        conn.close()


# ──────────────────────────────────────────────────────────────
# 7. PAGINATED BROWSE  (uses existing get_contacts_paged + sort)
#    Console loop: [n]ext  [p]rev  [q]uit
# ──────────────────────────────────────────────────────────────

# Sort options: user key → (SQL ORDER BY expression, label)
_SORT = {
    "1": ("c.username",   "name"),
    "2": ("c.birthday",   "birthday"),
    "3": ("c.created_at", "date added"),
}

def browse_contacts():
    print("\n  Sort by:  1) Name   2) Birthday   3) Date Added")
    sort_key   = input("  Choice [1]: ").strip() or "1"
    sort_col, sort_label = _SORT.get(sort_key, ("c.username", "name"))

    try:
        per_page = int(input("  Contacts per page [10]: ").strip() or "10")
    except ValueError:
        per_page = 10

    page = 0
    conn = get_connection()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM contacts")
            total = cur.fetchone()[0]

        total_pages = max(1, (total + per_page - 1) // per_page)

        while True:
            offset = page * per_page
            with conn.cursor() as cur:
                cur.execute(
                    f"""SELECT c.id, c.username, c.phone, c.email, c.birthday,
                               g.name,
                               STRING_AGG(ph.phone || ' (' || COALESCE(ph.type,'?') || ')', ', ')
                        FROM contacts c
                        LEFT JOIN groups  g  ON c.group_id = g.id
                        LEFT JOIN phones  ph ON c.id       = ph.contact_id
                        GROUP BY c.id, c.username, c.phone,
                                 c.email, c.birthday, g.name, c.created_at
                        ORDER BY {sort_col} NULLS LAST
                        LIMIT %s OFFSET %s""",
                    (per_page, offset),
                )
                rows = cur.fetchall()

            print(
                f"\n── Page {page + 1}/{total_pages}"
                f"  ({total} contacts, sorted by {sort_label}) ──"
            )
            if not rows:
                print("  (empty)")
            for row in rows:
                fmt_contact(row)

            print("\n  [n] Next  [p] Prev  [q] Quit")
            cmd = input("  > ").strip().lower()

            if cmd == "n":
                if page < total_pages - 1:
                    page += 1
                else:
                    print("  Already on the last page.")
            elif cmd == "p":
                if page > 0:
                    page -= 1
                else:
                    print("  Already on the first page.")
            elif cmd == "q":
                break
            else:
                print("  Unknown command.")

    except Exception as e:
        print(f"  Browse error: {e}")
    finally:
        conn.close()


# ──────────────────────────────────────────────────────────────
# 8. BULK IMPORT FROM CSV  (Practice-8 proc + extended fields)
#    Extended CSV columns: username, phone, email, birthday,
#                          group, phone_type
# ──────────────────────────────────────────────────────────────

def insert_from_csv(file_path):
    if not os.path.exists(file_path):
        print(f"  File not found: {file_path}")
        return

    names, phones, emails, birthdays, groups, phone_types = [], [], [], [], [], []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            headers   = set(reader.fieldnames or [])
            extended  = bool(headers & {"email", "birthday", "group", "phone_type"})

            for row in reader:
                name  = (row.get("username") or row.get("name", "")).strip()
                phone = row.get("phone", "").strip()
                if not name or not phone:
                    continue
                names.append(name)
                phones.append(phone)
                if extended:
                    emails.append(row.get("email", "").strip() or None)
                    birthdays.append(row.get("birthday", "").strip() or None)
                    groups.append(row.get("group", "").strip() or None)
                    phone_types.append(row.get("phone_type", "mobile").strip() or "mobile")

    except Exception as e:
        print(f"  CSV read error: {e}")
        return

    if not names:
        print("  No valid rows in CSV.")
        return

    conn = get_connection()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                "CALL bulk_insert_with_validation(%s, %s, NULL)", (names, phones)
            )
            result = cur.fetchone()
            conn.commit()

        if result and result[0]:
            print(f"  Warnings:\n  {result[0]}")
        else:
            print(f"  ✓ {len(names)} contact(s) processed via CSV.")

        if extended:
            with conn.cursor() as cur:
                for i, name in enumerate(names):
                    try:
                        gid      = _resolve_group(cur, groups[i]) if groups[i] else None
                        email    = emails[i]    if i < len(emails)    else None
                        birthday = birthdays[i] if i < len(birthdays) else None
                        cur.execute(
                            """UPDATE contacts
                               SET email    = COALESCE(%s, email),
                                   birthday = COALESCE(%s::DATE, birthday),
                                   group_id = COALESCE(%s, group_id)
                               WHERE phone = %s""",
                            (email, birthday, gid, phones[i]),
                        )
                    except Exception:
                        pass
            conn.commit()
            print("  ✓ Extended fields (email / birthday / group) updated.")

    except Exception as e:
        conn.rollback()
        print(f"  CSV import error: {e}")
    finally:
        conn.close()


# ──────────────────────────────────────────────────────────────
# 9. EXPORT TO JSON
# ──────────────────────────────────────────────────────────────

def export_to_json(file_path="contacts_export.json"):
    conn = get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT c.id, c.username, c.phone, c.email,
                          c.birthday::TEXT, c.created_at::TEXT,
                          g.name AS group_name
                   FROM contacts c
                   LEFT JOIN groups g ON c.group_id = g.id
                   ORDER BY c.username"""
            )
            col_names = [d[0] for d in cur.description]
            contacts  = cur.fetchall()

            result = []
            for row in contacts:
                contact = dict(zip(col_names, row))
                cur.execute(
                    "SELECT phone, type FROM phones WHERE contact_id = %s ORDER BY id",
                    (contact["id"],),
                )
                contact["phones"] = [
                    {"phone": r[0], "type": r[1]} for r in cur.fetchall()
                ]
                result.append(contact)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2, default=str)

        print(f"  ✓ {len(result)} contact(s) exported → '{file_path}'")
    except Exception as e:
        print(f"  Export error: {e}")
    finally:
        conn.close()


# ──────────────────────────────────────────────────────────────
# 10. IMPORT FROM JSON  (duplicate: skip or overwrite)
# ──────────────────────────────────────────────────────────────

def import_from_json(file_path="contacts_export.json"):
    if not os.path.exists(file_path):
        print(f"  File not found: {file_path}")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            contacts = json.load(f)
    except Exception as e:
        print(f"  JSON read error: {e}")
        return

    conn = get_connection()
    if not conn:
        return

    added = updated = skipped = 0
    try:
        for c in contacts:
            name     = (c.get("username") or "").strip()
            phone    = c.get("phone") or None
            email    = c.get("email") or None
            birthday = c.get("birthday") or None
            group_nm = c.get("group_name") or None
            extra_ph = c.get("phones", [])

            if not name:
                continue

            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id FROM contacts WHERE username = %s LIMIT 1", (name,)
                )
                existing = cur.fetchone()

                if existing:
                    ans = input(
                        f"  Duplicate: '{name}' exists. [s]kip / [o]verwrite? "
                    ).strip().lower()
                    if ans != "o":
                        skipped += 1
                        continue
                    gid = _resolve_group(cur, group_nm)
                    cur.execute(
                        """UPDATE contacts
                           SET phone    = COALESCE(%s, phone),
                               email    = COALESCE(%s, email),
                               birthday = COALESCE(%s::DATE, birthday),
                               group_id = COALESCE(%s, group_id)
                           WHERE username = %s""",
                        (phone, email, birthday, gid, name),
                    )
                    contact_id = existing[0]
                    updated += 1
                else:
                    gid = _resolve_group(cur, group_nm)
                    cur.execute(
                        """INSERT INTO contacts (username, phone, email, birthday, group_id)
                           VALUES (%s, %s, %s, %s::DATE, %s)
                           RETURNING id""",
                        (name, phone, email, birthday, gid),
                    )
                    contact_id = cur.fetchone()[0]
                    added += 1

                # Additional phone numbers
                for p in extra_ph:
                    p_num  = p.get("phone")
                    p_type = p.get("type")
                    if p_num:
                        cur.execute(
                            "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                            (contact_id, p_num, p_type),
                        )

            conn.commit()

        print(
            f"  ✓ Import done — added: {added}, overwritten: {updated}, skipped: {skipped}."
        )
    except Exception as e:
        conn.rollback()
        print(f"  Import error: {e}")
    finally:
        conn.close()


# ──────────────────────────────────────────────────────────────
# 11. DELETE CONTACT  (DB procedure: delete_contact_proc)
# ──────────────────────────────────────────────────────────────

def delete_contact(target):
    conn = get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("CALL delete_contact_proc(%s)", (target,))
            conn.commit()
        print(f"  ✓ Deleted contact matching '{target}'.")
    except Exception as e:
        conn.rollback()
        print(f"  Delete error: {e}")
    finally:
        conn.close()


# ──────────────────────────────────────────────────────────────
# INTERNAL HELPER
# ──────────────────────────────────────────────────────────────

def _resolve_group(cur, group_name):
    """Insert group if missing, return its id (or None if no name given)."""
    if not group_name:
        return None
    cur.execute(
        "INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
        (group_name,),
    )
    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    row = cur.fetchone()
    return row[0] if row else None


# ──────────────────────────────────────────────────────────────
# MAIN MENU
# ──────────────────────────────────────────────────────────────

MENU = """
╔══════════════════════════════════════════╗
║     PhoneBook — TSIS 1 Extended          ║
╠══════════════════════════════════════════╣
║  1.  Search  (name / phone / email)      ║
║  2.  Add / Update contact                ║
║  3.  Add phone number to a contact       ║
║  4.  Move contact to a group             ║
║  5.  Filter by group                     ║
║  6.  Search by email                     ║
║  7.  Browse all contacts (sort + pages)  ║
║  8.  Bulk import from CSV                ║
║  9.  Export all contacts to JSON         ║
║  10. Import contacts from JSON           ║
║  11. Delete contact                      ║
║  0.  Exit                                ║
╚══════════════════════════════════════════╝"""


def main():
    while True:
        print(MENU)
        choice = input("  Select: ").strip()

        if choice == "1":
            q = input("  Query (name / phone / email fragment): ").strip()
            search_by_pattern(q)

        elif choice == "2":
            name     = input("  Name: ").strip()
            phone    = input("  Primary phone: ").strip()
            email    = input("  Email       (Enter to skip): ").strip() or None
            birthday = input("  Birthday YYYY-MM-DD (Enter to skip): ").strip() or None
            group    = input("  Group  Family/Work/Friend/Other/new  (Enter to skip): ").strip() or None
            upsert_contact(name, phone, email, birthday, group)

        elif choice == "3":
            name  = input("  Contact name: ").strip()
            phone = input("  Phone number: ").strip()
            ptype = input("  Type  home/work/mobile  [mobile]: ").strip() or "mobile"
            add_phone(name, phone, ptype)

        elif choice == "4":
            name  = input("  Contact name: ").strip()
            group = input("  Group name (created if new): ").strip()
            move_to_group(name, group)

        elif choice == "5":
            group = input("  Group name: ").strip()
            filter_by_group(group)

        elif choice == "6":
            frag = input("  Email fragment (e.g. 'gmail'): ").strip()
            search_by_email(frag)

        elif choice == "7":
            browse_contacts()

        elif choice == "8":
            path = input("  CSV path [contacts.csv]: ").strip() or "contacts.csv"
            insert_from_csv(path)

        elif choice == "9":
            path = input("  Output path [contacts_export.json]: ").strip() or "contacts_export.json"
            export_to_json(path)

        elif choice == "10":
            path = input("  JSON path [contacts_export.json]: ").strip() or "contacts_export.json"
            import_from_json(path)

        elif choice == "11":
            target = input("  Name or primary phone to delete: ").strip()
            delete_contact(target)

        elif choice == "0":
            print("  Goodbye!")
            break

        else:
            print("  Unknown option — try again.")


if __name__ == "__main__":
    main()
