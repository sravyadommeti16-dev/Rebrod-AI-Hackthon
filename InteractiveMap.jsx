import React, { useEffect, useRef } from 'react';

export default function InteractiveMap({ routes, blockedZones, center, shelters, hospitals }) {
  const mapRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const layersRef = useRef([]);

  useEffect(() => {
    // Initialize map on mount if Leaflet is loaded
    if (!mapInstanceRef.current && window.L && mapRef.current) {
      // Initialize centering on India default or Chennai
      const initialCenter = center || [13.0827, 80.2707];
      mapInstanceRef.current = window.L.map(mapRef.current).setView(initialCenter, 13);
      
      // Load dark tiles matching the sleek command center look
      window.L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 19
      }).addTo(mapInstanceRef.current);
    }

    // Cleanup on unmount
    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove();
        mapInstanceRef.current = null;
      }
    };
  }, []);

  // Update map contents whenever props alter
  useEffect(() => {
    const map = mapInstanceRef.current;
    const L = window.L;
    if (!map || !L) return;

    // Remove all old markers and vectors
    layersRef.current.forEach(layer => map.removeLayer(layer));
    layersRef.current = [];

    // Reset center and zoom
    if (center && Array.isArray(center) && center.length === 2) {
      map.setView(center, 13.5);
    }

    // Add user/reported location pin (blue glow indicator)
    if (center && Array.isArray(center) && center.length === 2) {
      const userIcon = L.divIcon({
        className: 'user-marker',
        html: `<div style="background:#007aff; width:16px; height:16px; border-radius:50%; border:3px solid white; box-shadow:0 0 12px #007aff; animation: blink 1s infinite alternate;"></div>`,
        iconSize: [16, 16],
        iconAnchor: [8, 8]
      });
      const userMarker = L.marker(center, { icon: userIcon })
        .bindPopup("<b>Reported Location (Origin)</b><br/>Active coordinates.")
        .addTo(map);
      layersRef.current.push(userMarker);
    }

    // Add hazard blocked circles (Red Zones)
    if (blockedZones && blockedZones.length > 0) {
      blockedZones.forEach(zone => {
        if (zone.latlng) {
          const circle = L.circle(zone.latlng, {
            color: '#ef4444',
            fillColor: '#ef4444',
            fillOpacity: 0.3,
            weight: 2,
            radius: zone.radius || 200
          })
            .bindPopup(`<b>🔴 HAZARD ZONE: ${zone.name}</b><br/>Status: Blocked / Inaccessible`)
            .addTo(map);
          layersRef.current.push(circle);
        }
      });
    }

    // Add shelters (Green Tent Markers)
    if (shelters && shelters.length > 0) {
      shelters.forEach(shelter => {
        if (shelter.latlng) {
          const shelterIcon = L.divIcon({
            className: 'shelter-marker',
            html: `<div style="background:#10b981; width:28px; height:28px; border-radius:50%; border:2px solid white; display:flex; align-items:center; justify-content:center; color:white; font-size:14px; box-shadow: 0 0 10px rgba(16,185,129,0.5);">⛺</div>`,
            iconSize: [28, 28],
            iconAnchor: [14, 14]
          });
          const marker = L.marker(shelter.latlng, { icon: shelterIcon })
            .bindPopup(`<b>⛺ Relief Camp: ${shelter.name}</b><br/>Occupancy: ${shelter.occupancy}<br/>Phone: ${shelter.phone}`)
            .addTo(map);
          layersRef.current.push(marker);
        }
      });
    }

    // Add hospitals (Red Cross Clinic Markers)
    if (hospitals && hospitals.length > 0) {
      hospitals.forEach(hosp => {
        if (hosp.latlng) {
          const hospIcon = L.divIcon({
            className: 'hospital-marker',
            html: `<div style="background:#ef4444; width:28px; height:28px; border-radius:50%; border:2px solid white; display:flex; align-items:center; justify-content:center; color:white; font-size:13px; box-shadow: 0 0 10px rgba(239,68,68,0.5);">🏥</div>`,
            iconSize: [28, 28],
            iconAnchor: [14, 14]
          });
          const marker = L.marker(hosp.latlng, { icon: hospIcon })
            .bindPopup(`<b>🏥 Hospital: ${hosp.name}</b><br/>Beds: ${hosp.icu_beds}<br/>Phone: ${hosp.phone}`)
            .addTo(map);
          layersRef.current.push(marker);
        }
      });
    }

    // Draw routing lines (green for primary, dotted orange for alternate routes)
    if (routes && routes.length > 0) {
      routes.forEach(route => {
        if (route.path && route.path.length > 0) {
          const isPrimary = route.type === 'primary';
          const polyline = L.polyline(route.path, {
            color: isPrimary ? '#10b981' : '#f97316',
            weight: isPrimary ? 6 : 4,
            opacity: 0.85,
            dashArray: isPrimary ? null : '8, 8'
          })
            .bindPopup(`<b>${route.name}</b><br/>Distance: ${route.distance}<br/>Time: ${route.duration}<br/>Rating: ${route.safety_rating}`)
            .addTo(map);
          layersRef.current.push(polyline);
        }
      });
    }

  }, [routes, blockedZones, center, shelters, hospitals]);

  return (
    <div className="main-map-container">
      <div ref={mapRef} style={{ height: '100%', width: '100%', borderRadius: '12px' }} />
    </div>
  );
}
