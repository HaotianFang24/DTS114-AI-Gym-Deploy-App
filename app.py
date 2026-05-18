from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from uuid import uuid4
from datetime import datetime, timezone

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# In-memory "databases"
# -----------------------------
members_db = []
trainers_db = []
classes_db = []
bookings_db = []
enquiries_db = []
payments_db = []

ALLOWED_BOOKING_STATUSES = {"new", "in progress", "confirmed", "closed", "cancelled"}


# -----------------------------
# Helpers
# -----------------------------
def now_iso():
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix=None):
    uid = str(uuid4())
    return f"{prefix}_{uid}" if prefix else uid


def json_error(message, status=400, **extra):
    payload = {"error": message}
    if extra:
        payload.update(extra)
    return jsonify(payload), status


def require_json():
    if not request.is_json:
        return None, json_error("Request must be JSON", 400)
    data = request.get_json(silent=True)
    if data is None:
        return None, json_error("Invalid JSON body", 400)
    if not isinstance(data, dict):
        return None, json_error("JSON body must be an object", 400)
    return data, None


def validate_required_fields(data, fields):
    missing = []
    for f in fields:
        if f not in data or data.get(f) is None or (isinstance(data.get(f), str) and not data.get(f).strip()):
            missing.append(f)
    if missing:
        return False, missing
    return True, []


def find_by_id(db_list, record_id):
    for item in db_list:
        if item.get("id") == record_id:
            return item
    return None


# -----------------------------
# Seed data
# -----------------------------
def seed_data():
    members_db.clear()
    trainers_db.clear()
    classes_db.clear()
    bookings_db.clear()
    enquiries_db.clear()
    payments_db.clear()

    # Trainers
    t1 = {
        "id": new_id("trainer"),
        "name": "Alex Carter",
        "email": "alex.carter@gymdemo.local",
        "phone": "+1-555-0101",
        "bio": "Strength & conditioning coach focused on safe technique and progressive overload.",
        "specialties": ["Strength Training", "Conditioning", "Mobility"],
        "availability": [
            {"day": "Monday", "from": "07:00", "to": "12:00"},
            {"day": "Wednesday", "from": "16:00", "to": "20:00"},
            {"day": "Friday", "from": "07:00", "to": "11:00"},
        ],
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    t2 = {
        "id": new_id("trainer"),
        "name": "Priya Singh",
        "email": "priya.singh@gymdemo.local",
        "phone": "+1-555-0102",
        "bio": "Yoga & Pilates instructor specializing in stress reduction and core stability.",
        "specialties": ["Yoga", "Pilates", "Breathwork"],
        "availability": [
            {"day": "Tuesday", "from": "08:00", "to": "13:00"},
            {"day": "Thursday", "from": "17:00", "to": "20:00"},
            {"day": "Saturday", "from": "09:00", "to": "12:00"},
        ],
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    t3 = {
        "id": new_id("trainer"),
        "name": "Marco Alvarez",
        "email": "marco.alvarez@gymdemo.local",
        "phone": "+1-555-0103",
        "bio": "HIIT and functional training coach with a focus on sustainable fitness habits.",
        "specialties": ["HIIT", "Functional Training", "Fat Loss"],
        "availability": [
            {"day": "Monday", "from": "17:00", "to": "20:00"},
            {"day": "Thursday", "from": "07:00", "to": "10:00"},
            {"day": "Sunday", "from": "10:00", "to": "12:00"},
        ],
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    trainers_db.extend([t1, t2, t3])

    # Members
    m1 = {
        "id": new_id("member"),
        "name": "Jamie Lee",
        "email": "jamie.lee@example.com",
        "phone": "+1-555-0201",
        "membership_type": "Standard",
        "status": "active",
        "join_date": "2025-01-12",
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    m2 = {
        "id": new_id("member"),
        "name": "Sam Patel",
        "email": "sam.patel@example.com",
        "phone": "+1-555-0202",
        "membership_type": "Premium",
        "status": "active",
        "join_date": "2024-10-03",
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    m3 = {
        "id": new_id("member"),
        "name": "Taylor Nguyen",
        "email": "taylor.nguyen@example.com",
        "phone": "+1-555-0203",
        "membership_type": "Student",
        "status": "paused",
        "join_date": "2025-03-27",
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    members_db.extend([m1, m2, m3])

    # Classes
    c1 = {
        "id": new_id("class"),
        "name": "Strength Foundations",
        "description": "A beginner-friendly strength session focusing on form and compound movements.",
        "trainer_id": t1["id"],
        "trainer_name": t1["name"],
        "date": "2026-06-03",
        "start_time": "07:30",
        "end_time": "08:30",
        "capacity": 12,
        "status": "scheduled",
        "location": "Main Floor",
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    c2 = {
        "id": new_id("class"),
        "name": "Vinyasa Yoga Flow",
        "description": "A dynamic yoga class linking breath to movement for strength and mobility.",
        "trainer_id": t2["id"],
        "trainer_name": t2["name"],
        "date": "2026-06-04",
        "start_time": "18:00",
        "end_time": "19:00",
        "capacity": 20,
        "status": "scheduled",
        "location": "Studio A",
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    c3 = {
        "id": new_id("class"),
        "name": "HIIT Express",
        "description": "Fast-paced interval training to boost fitness and burn calories.",
        "trainer_id": t3["id"],
        "trainer_name": t3["name"],
        "date": "2026-06-05",
        "start_time": "12:15",
        "end_time": "12:45",
        "capacity": 16,
        "status": "scheduled",
        "location": "Functional Zone",
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    classes_db.extend([c1, c2, c3])

    # Bookings
    b1 = {
        "id": new_id("booking"),
        "member_name": m1["name"],
        "email": m1["email"],
        "class_id": c1["id"],
        "class_name": c1["name"],
        "notes": "First time attending strength class.",
        "status": "new",
        "assigned_trainer_id": c1["trainer_id"],
        "assigned_trainer_name": c1["trainer_name"],
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "audit": [
            {"at": now_iso(), "action": "created", "details": {"status": "new"}}
        ],
    }
    b2 = {
        "id": new_id("booking"),
        "member_name": m2["name"],
        "email": m2["email"],
        "class_id": c2["id"],
        "class_name": c2["name"],
        "notes": "Recovering from a wrist strain; any modifications?",
        "status": "in progress",
        "assigned_trainer_id": c2["trainer_id"],
        "assigned_trainer_name": c2["trainer_name"],
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "audit": [
            {"at": now_iso(), "action": "created", "details": {"status": "new"}},
            {"at": now_iso(), "action": "status_changed", "details": {"from": "new", "to": "in progress"}},
        ],
    }
    bookings_db.extend([b1, b2])

    # Enquiries
    e1 = {
        "id": new_id("enquiry"),
        "name": "Jordan Kim",
        "email": "jordan.kim@example.com",
        "subject": "Trial session",
        "message": "Do you offer a free trial class for beginners?",
        "status": "new",
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    e2 = {
        "id": new_id("enquiry"),
        "name": "Casey Morgan",
        "email": "casey.morgan@example.com",
        "subject": "Membership options",
        "message": "What’s included in the Premium membership and can I pause it?",
        "status": "new",
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    enquiries_db.extend([e1, e2])

    # Payments (non-goal but required list/endpoint)
    p1 = {
        "id": new_id("payment"),
        "member_id": m2["id"],
        "member_name": m2["name"],
        "amount": 59.99,
        "currency": "USD",
        "method": "card",
        "reference": "DEMO-INV-1001",
        "status": "paid",
        "paid_at": "2026-05-01T09:15:00+00:00",
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    p2 = {
        "id": new_id("payment"),
        "member_id": m1["id"],
        "member_name": m1["name"],
        "amount": 39.99,
        "currency": "USD",
        "method": "cash",
        "reference": "DEMO-INV-1002",
        "status": "paid",
        "paid_at": "2026-05-03T18:05:00+00:00",
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    payments_db.extend([p1, p2])


seed_data()


# -----------------------------
# Endpoints
# -----------------------------
@app.get("/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "service": "Gym Management System API",
            "time": now_iso(),
            "counts": {
                "members": len(members_db),
                "trainers": len(trainers_db),
                "classes": len(classes_db),
                "bookings": len(bookings_db),
                "enquiries": len(enquiries_db),
                "payments": len(payments_db),
            },
        }
    ), 200


@app.get("/members")
def get_members():
    return jsonify(members_db), 200


@app.get("/trainers")
def get_trainers():
    return jsonify(trainers_db), 200


@app.get("/classes")
def get_classes():
    return jsonify(classes_db), 200


@app.get("/bookings")
def get_bookings():
    return jsonify(bookings_db), 200


@app.post("/bookings")
def create_booking():
    data, err = require_json()
    if err:
        return err

    required = ["member_name", "email", "class_id", "notes"]
    ok, missing = validate_required_fields(data, required)
    if not ok:
        return json_error("Missing required fields", 400, missing=missing)

    class_id = str(data["class_id"]).strip()
    cls = find_by_id(classes_db, class_id)
    if not cls:
        return json_error("Class not found", 404, class_id=class_id)

    booking = {
        "id": new_id("booking"),
        "member_name": str(data["member_name"]).strip(),
        "email": str(data["email"]).strip(),
        "class_id": class_id,
        "class_name": cls.get("name"),
        "notes": str(data["notes"]).strip(),
        "status": "new",
        "assigned_trainer_id": cls.get("trainer_id"),
        "assigned_trainer_name": cls.get("trainer_name"),
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "audit": [{"at": now_iso(), "action": "created", "details": {"status": "new"}}],
    }
    bookings_db.append(booking)
    return jsonify(booking), 201


@app.patch("/bookings/<booking_id>/status")
def update_booking_status(booking_id):
    data, err = require_json()
    if err:
        return err

    ok, missing = validate_required_fields(data, ["status"])
    if not ok:
        return json_error("Missing required fields", 400, missing=missing)

    booking = find_by_id(bookings_db, booking_id)
    if not booking:
        return json_error("Booking not found", 404, booking_id=booking_id)

    new_status = str(data["status"]).strip().lower()
    if new_status not in ALLOWED_BOOKING_STATUSES:
        return json_error(
            "Invalid status",
            400,
            allowed_statuses=sorted(ALLOWED_BOOKING_STATUSES),
            received=new_status,
        )

    old_status = booking.get("status")
    if old_status != new_status:
        booking["status"] = new_status
        booking["updated_at"] = now_iso()
        booking.setdefault("audit", []).append(
            {"at": now_iso(), "action": "status_changed", "details": {"from": old_status, "to": new_status}}
        )

    return jsonify(booking), 200


@app.get("/enquiries")
def get_enquiries():
    return jsonify(enquiries_db), 200


@app.post("/enquiries")
def create_enquiry():
    data, err = require_json()
    if err:
        return err

    required = ["name", "email", "subject", "message"]
    ok, missing = validate_required_fields(data, required)
    if not ok:
        return json_error("Missing required fields", 400, missing=missing)

    enquiry = {
        "id": new_id("enquiry"),
        "name": str(data["name"]).strip(),
        "email": str(data["email"]).strip(),
        "subject": str(data["subject"]).strip(),
        "message": str(data["message"]).strip(),
        "status": "new",
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    enquiries_db.append(enquiry)
    return jsonify(enquiry), 201


@app.get("/payments")
def get_payments():
    return jsonify(payments_db), 200


# -----------------------------
# Error handlers
# -----------------------------
@app.errorhandler(404)
def not_found(_):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(405)
def method_not_allowed(_):
    return jsonify({"error": "Method not allowed"}), 405


@app.errorhandler(500)
def internal_error(_):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
