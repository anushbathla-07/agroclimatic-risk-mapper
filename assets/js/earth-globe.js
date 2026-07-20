// AgroClimatic Risk Mapper — Live 3D Risk Globe (Hero)
// Requires the importmap in index.html (three + three/addons).
// IMPORTANT: this uses ES modules — open the page via Live Server (http://),
// not by double-clicking the file (file:// will not load modules).
//
// This version fetches real Indian state boundaries at runtime and paints
// them directly onto the globe (fill + outline + name), instead of using
// plain point markers. Only 8 states have curated sample data (crop, exact
// risk factor); the rest get a demo-only risk level so the whole map reads
// as "complete". Swap SAMPLE_REGIONS + the demo levels for a real API once
// the backend is ready.

const container = document.getElementById('earth-globe');
const tooltip = document.getElementById('globe-tooltip');

if (container && tooltip) {
  loadGlobe();
}

async function loadGlobe() {
  try {
    const THREE = await import('three');
    const { OrbitControls } = await import('three/addons/controls/OrbitControls.js');
    init(THREE, OrbitControls);
  } catch (err) {
    console.error('Globe failed to load:', err);
    showFallback();
  }
}

function showFallback() {
  container.innerHTML = `
    <div style="
      width:100%; height:100%; display:flex; align-items:center; justify-content:center;
      border-radius:50%; border:1px dashed rgba(255,255,255,0.2);
      color:#92AEA2; font-family:'IBM Plex Mono', monospace; font-size:0.75rem;
      text-align:center; padding:20px;">
      Globe couldn't load. Make sure you're viewing this via Live Server (http://), not by opening the file directly.
    </div>`;
}

const STATE_GEOJSON_URL = 'https://raw.githubusercontent.com/geohacker/india/master/state/india_state.geojson';

const LEVEL_HEX = { low: '#9FE6B8', mod: '#F2C879', high: '#FF9E8A' };
const LEVEL_LABEL = { low: 'Low risk', mod: 'Moderate risk', high: 'High risk' };

// ---- Curated sample data for a few states (crop + specific factor) ----
const SAMPLE_REGIONS = {
  'Punjab':         { crop: 'Wheat',     risk: 38, level: 'low',  factor: 'Canal-fed, stable moisture' },
  'Maharashtra':    { crop: 'Cotton',    risk: 71, level: 'high', factor: 'Rainfall deficit −22%' },
  'Uttar Pradesh':  { crop: 'Sugarcane', risk: 54, level: 'mod',  factor: 'Rising pest activity' },
  'Madhya Pradesh': { crop: 'Soybean',   risk: 62, level: 'mod',  factor: 'Soil moisture below average' },
  'Bihar':          { crop: 'Rice',      risk: 66, level: 'mod',  factor: 'Delayed monsoon onset' },
  'Karnataka':      { crop: 'Ragi',      risk: 33, level: 'low',  factor: 'Favorable soil conditions' },
  'Rajasthan':      { crop: 'Bajra',     risk: 78, level: 'high', factor: 'Heat stress, low rainfall' },
  'Tamil Nadu':     { crop: 'Rice',      risk: 45, level: 'low',  factor: 'Normal seasonal pattern' },
};

// Deterministic placeholder level for states without curated data, so the
// whole map is filled in (clearly a demo — swap for real data later).
function demoLevel(name) {
  let sum = 0;
  for (let i = 0; i < name.length; i++) sum += name.charCodeAt(i);
  const levels = ['low', 'mod', 'high'];
  return levels[sum % 3];
}

// ---- Equirectangular projection helpers (matches the sphere's own UV mapping) ----
function project(lon, lat, w, h) {
  return [(lon + 180) / 360 * w, (90 - lat) / 180 * h];
}

function drawRing(ctx, ring, w, h) {
  ring.forEach(([lon, lat], i) => {
    const [x, y] = project(lon, lat, w, h);
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.closePath();
}

function ringsOf(geometry) {
  return geometry.type === 'Polygon' ? [geometry.coordinates] : geometry.coordinates;
}

// Ray-casting point-in-ring test, done in lon/lat space directly.
function pointInRing(lon, lat, ring) {
  let inside = false;
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const [xi, yi] = ring[i];
    const [xj, yj] = ring[j];
    const hit = (yi > lat) !== (yj > lat) && lon < ((xj - xi) * (lat - yi)) / (yj - yi) + xi;
    if (hit) inside = !inside;
  }
  return inside;
}

function pointInFeature(lon, lat, geometry) {
  let inside = false;
  ringsOf(geometry).forEach((polygon) => {
    polygon.forEach((ring) => {
      if (pointInRing(lon, lat, ring)) inside = !inside;
    });
  });
  return inside;
}

function bboxOf(geometry) {
  let minLon = 180, maxLon = -180, minLat = 90, maxLat = -90;
  ringsOf(geometry).forEach((polygon) => {
    polygon.forEach((ring) => {
      ring.forEach(([lon, lat]) => {
        if (lon < minLon) minLon = lon;
        if (lon > maxLon) maxLon = lon;
        if (lat < minLat) minLat = lat;
        if (lat > maxLat) maxLat = lat;
      });
    });
  });
  return { minLon, maxLon, minLat, maxLat };
}

// ---- Build the canvas texture: filled + outlined states + name labels ----
async function buildStateOverlay(THREE) {
  const w = 4096, h = 2048;
  const canvas = document.createElement('canvas');
  canvas.width = w;
  canvas.height = h;
  const ctx = canvas.getContext('2d');

  const res = await fetch(STATE_GEOJSON_URL);
  if (!res.ok) throw new Error('Boundary fetch failed: ' + res.status);
  const geo = await res.json();

  if (document.fonts && document.fonts.ready) {
    try { await document.fonts.ready; } catch (e) { /* ignore */ }
  }

  const features = geo.features.map((f) => ({
    name: f.properties.NAME_1,
    geometry: f.geometry,
    bbox: bboxOf(f.geometry),
  }));

  features.forEach((feature) => {
    const curated = SAMPLE_REGIONS[feature.name];
    const level = curated ? curated.level : demoLevel(feature.name);
    const hex = LEVEL_HEX[level];

    ctx.beginPath();
    ringsOf(feature.geometry).forEach((polygon) => {
      polygon.forEach((ring) => drawRing(ctx, ring, w, h));
    });
    ctx.fillStyle = hexToRgba(hex, 0.42);
    ctx.fill('evenodd');
    ctx.lineWidth = 2.5;
    ctx.strokeStyle = 'rgba(235,245,240,0.7)';
    ctx.stroke();

    // approximate centroid from the largest ring, for label placement
    let best = null, bestLen = 0;
    ringsOf(feature.geometry).forEach((polygon) => {
      const ring = polygon[0];
      if (ring.length > bestLen) { bestLen = ring.length; best = ring; }
    });
    let sx = 0, sy = 0;
    best.forEach(([lon, lat]) => {
      const [x, y] = project(lon, lat, w, h);
      sx += x; sy += y;
    });
    feature.labelX = sx / best.length;
    feature.labelY = sy / best.length;
    feature.pixelWidth = ((feature.bbox.maxLon - feature.bbox.minLon) / 360) * w;
  });

  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.shadowColor = 'rgba(4,10,8,0.85)';
  ctx.shadowBlur = 8;
  ctx.fillStyle = 'rgba(255,255,255,0.95)';
  features.forEach((feature) => {
    const size = Math.max(16, Math.min(34, feature.pixelWidth / 6));
    ctx.font = `600 ${size}px Inter, Arial, sans-serif`;
    ctx.fillText(feature.name, feature.labelX, feature.labelY);
  });

  const texture = new THREE.CanvasTexture(canvas);
  texture.needsUpdate = true;
  return { texture, features };
}

function hexToRgba(hex, alpha) {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return `rgba(${r},${g},${b},${alpha})`;
}

function init(THREE, OrbitControls) {
  const RADIUS = 2;

  // ---- Scene basics ----
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
  camera.position.set(0, 0, 5.6);

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  container.appendChild(renderer.domElement);

  // ---- Controls: drag to rotate, no scroll-zoom hijack ----
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;
  controls.enablePan = false;
  controls.enableZoom = false;
  controls.minPolarAngle = 0.3;
  controls.maxPolarAngle = Math.PI - 0.3;

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  controls.autoRotate = !reduceMotion;
  controls.autoRotateSpeed = 0.5;

  let resumeTimer = null;
  controls.addEventListener('start', () => {
    controls.autoRotate = false;
    if (resumeTimer) clearTimeout(resumeTimer);
  });
  controls.addEventListener('end', () => {
    if (reduceMotion) return;
    resumeTimer = setTimeout(() => { controls.autoRotate = true; }, 2200);
  });

  // ---- Bright, even lighting so the whole globe stays clearly visible ----
  scene.add(new THREE.AmbientLight(0xdfeeff, 0.95));
  const sun = new THREE.DirectionalLight(0xffffff, 0.55);
  sun.position.set(5, 3, 5);
  scene.add(sun);
  const fill = new THREE.DirectionalLight(0x9fd0ff, 0.35);
  fill.position.set(-4, -2, -3);
  scene.add(fill);

  // ---- Earth — natural sky-blue oceans + green land, kept bright ----
  const loader = new THREE.TextureLoader();
  const earthTexture = loader.load(
    'https://threejs.org/examples/textures/planets/earth_atmos_2048.jpg',
    undefined,
    undefined,
    () => console.warn('Earth texture failed to load — check network access.')
  );
  const earthGeo = new THREE.SphereGeometry(RADIUS, 64, 64);
  const earthMat = new THREE.MeshPhongMaterial({
    map: earthTexture,
    color: 0xcfe9e4,   // light blue-green tint — brightens without washing out the map
    specular: 0x6fb8e0,
    shininess: 10,
  });
  const earth = new THREE.Mesh(earthGeo, earthMat);
  scene.add(earth);

  // ---- Soft blue atmosphere glow ----
  const glowGeo = new THREE.SphereGeometry(RADIUS * 1.05, 64, 64);
  const glowMat = new THREE.ShaderMaterial({
    uniforms: {},
    vertexShader: `
      varying vec3 vNormal;
      void main() {
        vNormal = normalize(normalMatrix * normal);
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragmentShader: `
      varying vec3 vNormal;
      void main() {
        float intensity = pow(0.58 - dot(vNormal, vec3(0.0, 0.0, 1.0)), 3.0);
        vec3 glowColor = vec3(0.29, 0.62, 0.95);
        gl_FragColor = vec4(glowColor, 1.0) * intensity;
      }
    `,
    blending: THREE.AdditiveBlending,
    side: THREE.BackSide,
    transparent: true,
  });
  scene.add(new THREE.Mesh(glowGeo, glowMat));

  // ---- State boundary overlay (filled + outlined + labelled), loaded async ----
  let stateFeatures = [];
  buildStateOverlay(THREE)
    .then(({ texture, features }) => {
      stateFeatures = features;
      const overlayGeo = new THREE.SphereGeometry(RADIUS * 1.004, 96, 96);
      const overlayMat = new THREE.MeshBasicMaterial({ map: texture, transparent: true, depthWrite: false });
      scene.add(new THREE.Mesh(overlayGeo, overlayMat));
    })
    .catch((err) => {
      console.warn('State boundaries could not be loaded (offline or blocked):', err);
    });

  // ---- Hover: raycast the globe itself, convert the hit point back to lon/lat,
  // then test it against the real state polygons (bbox pre-filter for speed) ----
  const raycaster = new THREE.Raycaster();
  const pointer = new THREE.Vector2();
  let pointerActive = false;

  function vectorToLatLon(point) {
    const n = point.clone().normalize();
    const lat = 90 - (Math.acos(n.y) * 180) / Math.PI;
    const lon = (Math.atan2(n.z, -n.x) * 180) / Math.PI - 180;
    return { lat, lon: ((lon + 540) % 360) - 180 };
  }

  function onPointerMove(event) {
    const rect = renderer.domElement.getBoundingClientRect();
    pointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    pointer.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
    pointerActive = true;
    lastClientX = event.clientX;
    lastClientY = event.clientY;
  }
  let lastClientX = 0, lastClientY = 0;

  function checkHover() {
    if (!pointerActive || stateFeatures.length === 0) return;
    raycaster.setFromCamera(pointer, camera);
    const hit = raycaster.intersectObject(earth)[0];
    if (!hit) { hideTooltip(); return; }

    const { lat, lon } = vectorToLatLon(hit.point);
    const match = stateFeatures.find((f) =>
      lon >= f.bbox.minLon && lon <= f.bbox.maxLon &&
      lat >= f.bbox.minLat && lat <= f.bbox.maxLat &&
      pointInFeature(lon, lat, f.geometry)
    );

    if (match) {
      showTooltip(match.name, lastClientX, lastClientY);
      container.style.cursor = 'pointer';
    } else {
      hideTooltip();
      container.style.cursor = 'grab';
    }
  }

  function showTooltip(name, x, y) {
    const curated = SAMPLE_REGIONS[name];
    const level = curated ? curated.level : demoLevel(name);
    tooltip.hidden = false;
    tooltip.style.left = `${x}px`;
    tooltip.style.top = `${y}px`;
    tooltip.querySelector('.globe-tooltip-region').textContent = name;
    tooltip.querySelector('.globe-tooltip-crop').textContent = curated ? curated.crop : 'Sample data';
    const riskVal = curated ? curated.risk : 30 + (name.length * 7) % 60;
    tooltip.querySelector('.globe-tooltip-risk-value').textContent = `${riskVal} · ${LEVEL_LABEL[level]}`;
    tooltip.querySelector('.globe-tooltip-risk-value').style.color = LEVEL_HEX[level];
    tooltip.querySelector('.globe-tooltip-factor').textContent = curated ? curated.factor : 'Demo value — connect a real feed for live data';
  }

  function hideTooltip() {
    tooltip.hidden = true;
    pointerActive = false;
  }

  renderer.domElement.addEventListener('pointermove', onPointerMove);
  renderer.domElement.addEventListener('pointerleave', () => { pointerActive = false; hideTooltip(); });

  // ---- Resize handling ----
  function resize() {
    const size = container.clientWidth;
    if (size === 0) return;
    renderer.setSize(size, size);
    camera.aspect = 1;
    camera.updateProjectionMatrix();
  }
  window.addEventListener('resize', resize);
  resize();

  // ---- Animate (hover check runs here, capped to frame rate — cheap & smooth) ----
  function animate() {
    requestAnimationFrame(animate);
    checkHover();
    controls.update();
    renderer.render(scene, camera);
  }
  animate();
}