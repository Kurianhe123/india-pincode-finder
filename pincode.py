from geopy.geocoders import Nominatim

def get_pincode(place):
    geolocator = Nominatim(user_agent="pincode_app")
    location = geolocator.geocode(place, addressdetails=True)

    if location:
        address = location.raw.get("address", {})
        return address.get("postcode", "Pincode not found")
    else:
        return "Location not found"

place = input("Enter location: ")

if place == "":
    print("Please enter a location")
else:
    pincode = get_pincode(place)
    print("Pincode:", pincode)
