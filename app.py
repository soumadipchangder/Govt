from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")  # Path to JSON key
firebase_admin.initialize_app(cred)
db = firestore.client()

# Route for data entry page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Collect data from form
        food_data = {
            "Rice": request.form.get("rice"),
            "Musur Dal": request.form.get("musur_dal"),
            "Mustard Oil": request.form.get("mustard_oil"),
            "Iodised Salt": request.form.get("iodised_salt"),
            "RTE Packet": request.form.get("rte_packet"),
            "timestamp": datetime.utcnow()  # Store timestamp for sorting
        }

        # Store in Firestore with a unique auto-generated ID
        db.collection("food_distribution").add(food_data)
        
        return redirect(url_for("index"))

    return render_template("index.html")

# Route for admin panel to view all stored data
@app.route("/admin")
def admin():
    docs = db.collection("food_distribution").order_by("timestamp", direction=firestore.Query.DESCENDING).stream()
    food_data = [{**doc.to_dict(), "id": doc.id} for doc in docs]  # Store document ID

    return render_template("admin.html", food_data=food_data)

if __name__ == "__main__":
    app.run(debug=True)
