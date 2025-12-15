from flask import Flask, render_template, request
import requests

app = Flask(__name__, template_folder="templates")

def get_pincodes_from_india_post(place):
    url = f"https://api.postalpincode.in/postoffice/{place}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data or data[0]["Status"] != "Success":
            return []

        results = []
        for office in data[0]["PostOffice"]:
            results.append({
                "name": office["Name"],
                "district": office["District"],
                "state": office["State"],
                "pincode": office["Pincode"]
            })
        return results

    except requests.exceptions.RequestException:
        return None   # API / network issue


@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    error = ""

    if request.method == "POST":
        place = request.form.get("place", "").strip()

        if not place:
            error = "Please enter a place name"
        else:
            data = get_pincodes_from_india_post(place)

            if data is None:
                error = "India Post server is temporarily unavailable. Please try again later."
            elif not data:
                error = "No PIN codes found for this place"
            else:
                results = data

    return render_template("index.html", results=results, error=error)


if __name__ == "__main__":
    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


