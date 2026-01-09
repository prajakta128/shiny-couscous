const express = require("express");
const fs = require("fs");
const cors = require("cors");

const app = express();
app.use(cors());

const hospitals = JSON.parse(fs.readFileSync("hospitals.json", "utf-8"));

// Haversine formula to calculate distance between two points
function getDistance(lat1, lon1, lat2, lon2) {
  const R = 6371; // km
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * Math.PI / 180) *
    Math.cos(lat2 * Math.PI / 180) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2);
  return R * (2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a)));
}

app.get("/get-hospitals", (req, res) => {
  const userLat = parseFloat(req.query.lat);
  const userLng = parseFloat(req.query.lng);

  // Sort hospitals by distance
  const nearby = hospitals
    .map(h => ({
      ...h,
      distance: getDistance(userLat, userLng, h.lat, h.lng)
    }))
    .sort((a, b) => a.distance - b.distance)
    .slice(0, 5); // Top 5 nearest hospitals

  res.json(nearby);
});

app.listen(5000, () => console.log("Server running on http://localhost:5000"));
