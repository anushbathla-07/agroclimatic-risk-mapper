// AgroClimatic Risk Mapper — shared sample data + deterministic "mock risk engine"
// Swap AGRO_DATA and computeRisk() internals for real API calls once the backend is ready.

const AGRO_DATA = {
  states: {
    'Punjab':         ['Ludhiana', 'Amritsar', 'Patiala'],
    'Maharashtra':    ['Nagpur', 'Nashik', 'Pune'],
    'Uttar Pradesh':  ['Lucknow', 'Kanpur', 'Varanasi'],
    'Madhya Pradesh': ['Indore', 'Bhopal', 'Jabalpur'],
    'Bihar':          ['Patna', 'Gaya', 'Muzaffarpur'],
    'Karnataka':      ['Belagavi', 'Mysuru', 'Hubballi'],
    'Rajasthan':      ['Jodhpur', 'Bikaner', 'Kota'],
    'Tamil Nadu':     ['Coimbatore', 'Madurai', 'Salem'],
  },
  crops: ['Wheat', 'Rice', 'Cotton', 'Sugarcane', 'Soybean', 'Bajra', 'Ragi', 'Maize'],
  diseases: {
    Wheat:     ['Rust', 'Powdery Mildew', 'Loose Smut'],
    Rice:      ['Blast', 'Bacterial Blight', 'Sheath Rot'],
    Cotton:    ['Bollworm', 'Leaf Curl Virus', 'Wilt'],
    Sugarcane: ['Red Rot', 'Smut', 'Borer Infestation'],
    Soybean:   ['Rust', 'Pod Blight', 'Yellow Mosaic'],
    Bajra:     ['Downy Mildew', 'Ergot', 'Smut'],
    Ragi:      ['Blast', 'Leaf Spot', 'Rust'],
    Maize:     ['Stalk Rot', 'Leaf Blight', 'Fall Armyworm'],
  },
  stages: ['Sowing', 'Vegetative', 'Flowering', 'Grain Fill', 'Maturity'],
};

// ---- Deterministic seeded "randomness" so the same inputs always produce the same demo result ----
function hashString(str) {
  let h = 0;
  for (let i = 0; i < str.length; i++) { h = (h << 5) - h + str.charCodeAt(i); h |= 0; }
  return h;
}
function mulberry32(seed) {
  return function () {
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function pick(rand, arr) { return arr[Math.floor(rand() * arr.length)]; }

function levelFromScore(score) {
  if (score >= 66) return 'high';
  if (score >= 34) return 'mod';
  return 'low';
}

const LEVEL_LABEL = { low: 'Low Risk', mod: 'Moderate Risk', high: 'High Risk' };
const LEVEL_COLOR = { low: '#3FD68A', mod: '#E7B65C', high: '#FF6B57' };

// Main entry point: computes a full mock report for a state + village + crop combo.
function computeRisk(state, village, crop) {
  const rand = mulberry32(hashString(`${state}|${village}|${crop}`));

  const score = Math.floor(rand() * 100);
  const level = levelFromScore(score);

  const temp = Math.round(20 + rand() * 16);
  const rain = Math.round(rand() * 60);
  const humidity = Math.round(35 + rand() * 50);

  const moisture = Math.round(15 + rand() * 65);
  const ph = (5.2 + rand() * 2.3).toFixed(1);
  const fertility = Math.round(40 + rand() * 55);

  const diseaseList = AGRO_DATA.diseases[crop] || ['General Stress'];
  const diseaseName = pick(rand, diseaseList);
  const diseaseProb = Math.round(10 + rand() * 80);
  const stage = pick(rand, AGRO_DATA.stages);

  const alerts = [];
  if (level === 'high') {
    alerts.push({ level: 'high', text: `Irrigation recommended within 48 hours — soil moisture trending low for ${crop.toLowerCase()}.` });
    alerts.push({ level: 'high', text: `Scout for ${diseaseName.toLowerCase()} this week — conditions favor outbreak.` });
  } else if (level === 'mod') {
    alerts.push({ level: 'mod', text: `Monitor field conditions closely over the next 3–5 days.` });
    alerts.push({ level: 'mod', text: `Keep an eye out for early signs of ${diseaseName.toLowerCase()}.` });
  } else {
    alerts.push({ level: 'low', text: `Conditions are stable. Maintain regular monitoring.` });
  }

  return {
    state, village, crop, score, level,
    weather: { temp, rain, humidity },
    soil: { moisture, ph, fertility },
    disease: { name: diseaseName, prob: diseaseProb, stage },
    alerts,
  };
}

// Used by prediction.html — ranks all known diseases for a crop given state + growth stage.
function predictDiseases(crop, state, stage) {
  const list = AGRO_DATA.diseases[crop] || ['General Stress'];
  return list
    .map((name) => {
      const rand = mulberry32(hashString(`${crop}|${state}|${stage}|${name}`));
      return { name, prob: Math.round(5 + rand() * 90) };
    })
    .sort((a, b) => b.prob - a.prob);
}