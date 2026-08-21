/**
 * PACT Geospatial Visualization Engine (OpenStreetMap / Leaflet).
 * Renders multi-tiered disaster spatial layers:
 *  - Provider stockpiles & relief depots
 *  - Victim SOS coordinates (unmasked or 2km zero-knowledge grid)
 *  - Cascading $geoNear search radiuses & route trajectories
 */

class CrisisMap {
  constructor(containerId = "crisisMapContainer") {
    this.containerId = containerId;
    this.map = null;
    this.depotLayer = null;
    this.victimLayer = null;
    this.searchRingsLayer = null;
    this.routeLayer = null;
    this.depots = [];

    this.initMap();
  }

  initMap() {
    if (typeof L === "undefined") {
      console.warn("Leaflet not loaded yet. Map initialization deferred.");
      return;
    }

    const elem = document.getElementById(this.containerId);
    if (!elem) {
      console.error(`Map container #${this.containerId} not found.`);
      return;
    }

    // Default center on Tamil Nadu (Chennai corridor)
    const defaultCenter = [13.0827, 80.2707];

    this.map = L.map(this.containerId, {
      center: defaultCenter,
      zoom: 11,
      zoomControl: true,
      attributionControl: false
    });

    // Clean OpenStreetMap default tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      attribution: '© OpenStreetMap contributors'
    }).addTo(this.map);

    // Initialize dedicated layer groups
    this.searchRingsLayer = L.layerGroup().addTo(this.map);
    this.routeLayer = L.layerGroup().addTo(this.map);
    this.depotLayer = L.layerGroup().addTo(this.map);
    this.victimLayer = L.layerGroup().addTo(this.map);

    console.log("[MAP] PACT OpenStreetMap Engine initialized.");
  }

  /**
   * Updates map view center & zoom.
   */
  setCenter(lat, lon, zoom = 12) {
    if (this.map) {
      this.map.setView([lat, lon], zoom);
    }
  }

  /**
   * Sets & renders provider relief depots.
   */
  setDepots(depotsList) {
    if (!this.map || !this.depotLayer) return;
    this.depotLayer.clearLayers();
    this.depots = depotsList;

    depotsList.forEach(d => {
      const loc = d.loc || d.location || {};
      const coords = loc.coordinates || [80.2707, 13.0827];
      const lon = coords[0];
      const lat = coords[1];
      const name = d.provider_name || d.name || "Relief Depot";
      const pid = d.provider_id || "DEPOT";
      const inventory = d.inventory || {};

      let badgeLabel = "DEPOT";
      let borderColor = "#6B5D4F";
      if (pid.includes("HOSPITAL") || pid.includes("MEDICAL")) {
        badgeLabel = "MED";
        borderColor = "#F62440";
      } else if (pid.includes("NGO") || pid.includes("ALPHA")) {
        badgeLabel = "NGO";
        borderColor = "#196D34";
      } else if (pid.includes("NDRF") || pid.includes("RESCUE")) {
        badgeLabel = "DRF";
        borderColor = "#8A5B07";
      } else if (pid.includes("CSR")) {
        badgeLabel = "CSR";
        borderColor = "#175494";
      }

      const depotIcon = L.divIcon({
        className: 'custom-depot-marker',
        html: `
          <div style="
            background: #FFF2DB;
            border: 2px solid ${borderColor};
            border-radius: 6px;
            width: 32px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            font-weight: 700;
            color: #2B2119;
            box-shadow: 0 1px 3px rgba(43,33,25,0.15);
            cursor: pointer;
          ">${badgeLabel}</div>
        `,
        iconSize: [32, 24],
        iconAnchor: [16, 12]
      });

      const itemsList = Object.entries(inventory)
        .map(([k, v]) => `<div style="display:flex; justify-content:space-between; font-family:var(--font-mono); font-size:10px; color:#6B5D4F; padding:2px 0; border-bottom:1px solid #EBDDC0;"><span>${k.replace('_', ' ').toUpperCase()}</span><strong style="color:#2B2119">${v}</strong></div>`)
        .join('');

      const popupContent = `
        <div style="font-family:var(--font-sans); font-size:11px; color:#2B2119; min-width:200px; padding:4px;">
          <div style="font-weight:700; color:${borderColor}; font-size:12px; margin-bottom:2px;">[${badgeLabel}] ${name}</div>
          <div style="font-family:var(--font-mono); font-size:9px; color:#6B5D4F; margin-bottom:8px;">ID: ${pid} · [${lat.toFixed(4)}, ${lon.toFixed(4)}]</div>
          <div style="font-family:var(--font-sans); font-size:10px; font-weight:700; color:#2B2119; margin-bottom:4px; text-transform:uppercase;">Stockpiled Reserves</div>
          <div style="display:flex; flex-direction:column;">
            ${itemsList || '<span style="color:#6B5D4F">Active supplies</span>'}
          </div>
        </div>
      `;

      const marker = L.marker([lat, lon], { icon: depotIcon })
        .bindPopup(popupContent, { className: 'pact-dark-popup' });

      this.depotLayer.addLayer(marker);
    });
  }

  /**
   * Adds an emergency victim SOS marker.
   */
  addVictim(lat, lon, uid = "SOS", situation = "Emergency", isMasked = false) {
    if (!this.map || !this.victimLayer) return;

    const label = isMasked ? `GRID: ${uid}` : uid;

    const victimIcon = L.divIcon({
      className: 'custom-victim-marker',
      html: `
        <div style="
          background: #F62440;
          border: 2px solid #ffffff;
          border-radius: 4px;
          width: 32px;
          height: 22px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 9px;
          font-weight: 800;
          color: #ffffff;
          box-shadow: 0 2px 6px rgba(246,36,64,0.4);
          cursor: pointer;
        ">${label.substring(0, 4)}</div>
      `,
      iconSize: [32, 22],
      iconAnchor: [16, 11]
    });

    const popupContent = `
      <div style="font-family:var(--font-sans); font-size:11px; color:#2B2119; min-width:180px; padding:4px;">
        <div style="font-weight:700; color:#F62440; font-size:12px; margin-bottom:2px;">Target Incident: ${uid}</div>
        <div style="font-size:10px; color:#6B5D4F; margin-bottom:4px;">Type: ${situation}</div>
        <div style="font-family:var(--font-mono); font-size:9px; color:#6B5D4F; margin-bottom:6px;">GPS: [${lat.toFixed(4)}, ${lon.toFixed(4)}]</div>
        <div style="font-size:9px; font-weight:600; color:${isMasked ? '#8A5B07' : '#196D34'};">
          ${isMasked ? 'Zero-Knowledge 2km Grid Mask Active' : 'Verified Exact Coordinates'}
        </div>
      </div>
    `;

    const marker = L.marker([lat, lon], { icon: victimIcon })
      .bindPopup(popupContent, { className: 'pact-dark-popup' })
      .addTo(this.victimLayer);

    marker.openPopup();
    this.map.panTo([lat, lon]);
  }

  /**
   * Visualizes expanding geospatial search rings.
   */
  triggerGeoSearch(lat, lon, maxRadiusKm = 25) {
    if (!this.map || !this.searchRingsLayer) return;
    this.searchRingsLayer.clearLayers();

    const radiuses = [maxRadiusKm * 0.4, maxRadiusKm * 0.7, maxRadiusKm];
    radiuses.forEach((rKm, idx) => {
      const circle = L.circle([lat, lon], {
        radius: rKm * 1000,
        color: '#F62440',
        weight: 1.5,
        fillColor: '#FFE5BF',
        fillOpacity: 0.08 + (idx * 0.04),
        dashArray: '4, 4'
      }).addTo(this.searchRingsLayer);

      circle.bindTooltip(`Tier ${idx + 1}: ${rKm.toFixed(0)} km search perimeter`, {
        permanent: false,
        direction: 'top',
        className: 'pact-tooltip'
      });
    });

    setTimeout(() => {
      if (this.searchRingsLayer) {
        this.searchRingsLayer.clearLayers();
      }
    }, 12000);
  }

  /**
   * Draws tactical dispatch routes between assigned depots and victim.
   */
  drawDispatchPlan(planAllocations, victimLat, victimLon) {
    if (!this.map || !this.routeLayer) return;
    this.routeLayer.clearLayers();

    planAllocations.forEach(alloc => {
      const pLat = alloc.provider_lat || (victimLat + (Math.random() * 0.06 - 0.03));
      const pLon = alloc.provider_lon || (victimLon + (Math.random() * 0.06 - 0.03));

      const polyline = L.polyline([[pLat, pLon], [victimLat, victimLon]], {
        color: '#F62440',
        weight: 3,
        opacity: 0.8,
        dashArray: '6, 6'
      }).addTo(this.routeLayer);

      polyline.bindTooltip(`ETA: ~${alloc.eta_hours || 1.0}h | Dist: ${alloc.distance_km || 12} km`, {
        permanent: true,
        direction: 'center',
        className: 'pact-tooltip'
      });
    });
  }

  clearVictims() {
    if (this.victimLayer) this.victimLayer.clearLayers();
    if (this.routeLayer) this.routeLayer.clearLayers();
    if (this.searchRingsLayer) this.searchRingsLayer.clearLayers();
  }
}
