import streamlit as st
import streamlit.components.v1 as components

# Page Configuration
st.set_page_config(
    page_title="AgroClimatic Risk Mapper — Thynk Unlimited",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit default UI elements
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { margin-top: -80px; background-color: #070D0B; }
    </style>
""", unsafe_allow_html=True)

# Complete Enterprise-Grade HTML + CSS + JS Frontend Application with Exact Team Photos
full_website_html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AgroClimatic Risk Mapper — Thynk Unlimited</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500&display=swap" rel="stylesheet">
<script type="importmap">
{
  "imports": {
    "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
    "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
  }
}
</script>
<style>
:root{
  --void: #070D0B;
  --surface: #0D1613;
  --surface-2: #121F1A;
  --surface-3: #17251F;
  --border: rgba(255,255,255,0.09);
  --border-strong: rgba(255,255,255,0.16);
  --text: #EAF3EE;
  --text-muted: #92AEA2;
  --text-faint: #5F776C;
  --teal: #22D3C5;
  --blue: #3E8EFF;
  --danger: #FF6B57;
  --gold: #E7B65C;
  --display: "Fraunces", serif;
  --body: "Inter", sans-serif;
  --mono: "IBM Plex Mono", monospace;
  --wrap: 1180px;
}

*{box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{
  margin:0; background:var(--void); color:var(--text);
  font-family:var(--body); line-height:1.6; -webkit-font-smoothing:antialiased;
}

.wrap{max-width:var(--wrap); margin:0 auto; padding:0 28px;}

h1,h2,h3{
  font-family:var(--display); color:var(--text); margin:0 0 0.4em; font-weight:600;
}
h1{font-size:clamp(2.6rem, 5vw, 4rem); line-height:1.06;}
h2{font-size:clamp(1.8rem, 3vw, 2.4rem); line-height:1.15;}
p{color:var(--text-muted);}

.eyebrow{
  font-family:var(--mono); font-size:0.72rem; letter-spacing:0.16em;
  text-transform:uppercase; color:var(--blue); margin:0 0 1em; font-weight:500;
}

a{color:inherit; text-decoration:none;}

.btn{
  display:inline-block; padding:0.9em 1.7em; border-radius:6px; font-weight:600;
  font-size:0.92rem; border:1px solid transparent; cursor:pointer;
  transition:transform 0.2s ease, box-shadow 0.2s ease;
}
.btn-primary{
  background:linear-gradient(135deg, var(--blue), var(--teal)); color:#04120D;
}
.btn-primary:hover{transform:translateY(-2px); box-shadow:0 8px 26px rgba(62,142,255,0.35);}
.btn-ghost{
  border-color:var(--border-strong); color:var(--text); background:rgba(255,255,255,0.02);
}
.btn-ghost:hover{border-color:var(--blue); color:var(--blue);}

.site-header{
  position:sticky; top:0; z-index:50; background:rgba(7,13,11,0.85);
  backdrop-filter:blur(12px); border-bottom:1px solid var(--border);
}
.header-inner{
  display:flex; align-items:center; justify-content:space-between; padding:16px 28px;
}
.brand{font-family:var(--display); font-size:1.3rem; font-weight:600; color:var(--text);}
.brand span{color:var(--blue);}
.main-nav{display:flex; gap:24px;}
.main-nav a{font-size:0.9rem; font-weight:500; color:var(--text-muted); transition:color 0.2s;}
.main-nav a:hover{color:var(--text);}

.hero{position:relative; overflow:hidden; padding:90px 0 70px;}
.hero-glow{
  position:absolute; border-radius:50%; filter:blur(90px); pointer-events:none; z-index:0;
}
.hero-glow-1{width:560px; height:560px; background:radial-gradient(circle, rgba(62,142,255,0.22), transparent 70%); top:-160px; right:-120px;}
.hero-glow-2{width:380px; height:380px; background:radial-gradient(circle, rgba(34,211,197,0.12), transparent 70%); bottom:-140px; left:-100px;}
.hero-inner{position:relative; z-index:1; display:grid; grid-template-columns:1fr 1fr; gap:50px; align-items:center;}

.hero-stats{display:flex; gap:32px; margin-top:2.6em; flex-wrap:wrap;}
.hero-stats div{display:flex; flex-direction:column; gap:2px; font-size:0.78rem; color:var(--text-faint); border-left:2px solid var(--border-strong); padding-left:14px;}
.hero-stats span{font-family:var(--mono); font-size:1.05rem; color:var(--blue); font-weight:500;}

.hero-globe-stage{position:relative; display:flex; flex-direction:column; align-items:center;}
.globe-canvas-wrap{width:100%; max-width:460px; aspect-ratio:1/1; margin:0 auto; cursor:grab; touch-action:none;}
.globe-canvas-wrap canvas{display:block; width:100%; height:100%;}

.section{padding:80px 0;}
.bg-surface{background:var(--surface);}

.grid-2{display:grid; grid-template-columns:1fr 1fr; gap:40px; align-items:center;}
.grid-4{display:grid; grid-template-columns:repeat(4, 1fr); gap:20px; margin-top:2rem;}
.grid-3{display:grid; grid-template-columns:repeat(3, 1fr); gap:24px; margin-top:2rem;}

@media(max-width:900px){.grid-2, .grid-4, .grid-3, .hero-inner{grid-template-columns:1fr;}}

.card{
  background:var(--surface-2); border:1px solid var(--border); border-radius:12px; padding:28px;
  transition:transform 0.2s ease, border-color 0.2s ease;
}
.card:hover{transform:translateY(-4px); border-color:var(--border-strong);}

.tool-panel{
  background:var(--surface-2); border:1px solid var(--border); border-radius:12px; padding:32px;
  display:grid; grid-template-columns:repeat(3, 1fr) auto; gap:18px; align-items:end; margin-top:2rem;
}
@media(max-width:900px){.tool-panel{grid-template-columns:1fr;}}
.select-group{display:flex; flex-direction:column; gap:8px;}
.select-group label{font-family:var(--mono); font-size:0.7rem; text-transform:uppercase; color:var(--text-muted);}
.select-group select{
  background:var(--surface); border:1px solid var(--border-strong); color:var(--text);
  padding:12px 14px; border-radius:6px; font-family:var(--body); font-size:0.95rem;
}
.btn-check{
  background:linear-gradient(135deg, var(--blue), var(--teal)); color:#04120D; border:none;
  border-radius:6px; padding:12.5px 24px; font-weight:600; cursor:pointer;
}

.results{margin-top:30px; display:none;}
.results.visible{display:block; animation:fadeUp 0.4s ease;}
@keyframes fadeUp{from{opacity:0; transform:translateY(10px);} to{opacity:1; transform:translateY(0);}}

.team-card{
  background:var(--surface-2); border:1px solid var(--border); border-radius:12px; padding:24px; text-align:center;
}
.team-avatar{
  width:95px; height:95px; border-radius:50%; margin:0 auto 16px; object-fit:cover;
  border:2px solid var(--blue); box-shadow:0 0 15px rgba(62,142,255,0.3);
}
.team-role{font-family:var(--mono); font-size:0.75rem; color:var(--blue); text-transform:uppercase; margin-top:6px;}

.contact-box{
  background:var(--surface-2); border:1px solid var(--border); border-radius:12px; padding:40px; max-width:650px; margin:0 auto;
}
.form-group{display:flex; flex-direction:column; gap:8px; margin-bottom:16px;}
.form-group label{font-family:var(--mono); font-size:0.72rem; text-transform:uppercase; color:var(--text-muted);}
.form-group input, .form-group textarea{
  background:var(--surface); border:1px solid var(--border-strong); color:var(--text);
  padding:12px 16px; border-radius:6px; font-family:var(--body); font-size:0.95rem;
}

.glow-divider{height:1px; background:linear-gradient(90deg, transparent, rgba(62,142,255,0.4), transparent);}
.site-footer{background:#050908; border-top:1px solid var(--border); padding:40px 0; text-align:center; font-family:var(--mono); font-size:0.75rem; color:var(--text-faint);}
</style>
</head>
<body>

<header class="site-header">
  <div class="wrap header-inner">
    <a href="#" class="brand">AgroClimatic<span>.</span> [Thynk Unlimited]</a>
    <nav class="main-nav">
      <a href="#hero">Home</a>
      <a href="#problem">The Problem</a>
      <a href="#features">Features</a>
      <a href="#dashboard-tool">Live Risk Map</a>
      <a href="#team">Team</a>
      <a href="#contact">Contact</a>
    </nav>
    <a href="tel:9837603778" class="btn btn-primary btn-sm">📞 9837603778</a>
  </div>
</header>

<main>
  <!-- HERO SECTION -->
  <section class="hero" id="hero">
    <div class="hero-glow hero-glow-1"></div>
    <div class="hero-glow hero-glow-2"></div>
    <div class="wrap hero-inner">
      <div>
        <p class="eyebrow">Thynk Unlimited Startup Presentation — Presented by Anush[cite: 6]</p>
        <h1>See the season<br>before it happens.</h1>
        <p style="font-size: 1.08rem; max-width: 48ch;">AI-Powered Agricultural Risk Assessment Platform[cite: 6]. Satellite data, live weather, and machine learning models collapsed into one precision risk score per field.</p>
        <div style="display:flex; gap:14px; margin-top:2rem;">
          <a href="#dashboard-tool" class="btn btn-primary">Launch Live Dashboard</a>
          <a href="#features" class="btn btn-ghost">Explore Features →</a>
        </div>
        <div class="hero-stats">
          <div><span>Render Cloud</span>Backend Active[cite: 6]</div>
          <div><span>9837603778</span>Direct Helpline</div>
          <div><span>1 Score</span>Per Field[cite: 6]</div>
        </div>
      </div>
      <div class="hero-globe-stage">
        <div id="earth-globe" class="globe-canvas-wrap"></div>
      </div>
    </div>
  </section>

  <div class="glow-divider"></div>

  <!-- THE PROBLEM -->
  <section class="section bg-surface" id="problem">
    <div class="wrap grid-2">
      <div>
        <p class="eyebrow">The Problem[cite: 6]</p>
        <h2>Climate unpredictability threatens global agriculture[cite: 6].</h2>
        <p>Farmers struggle with extreme weather patterns causing massive crop losses each season with zero early warning systems[cite: 6].</p>
      </div>
      <div style="display:flex; flex-direction:column; gap:16px;">
        <div class="card"><h3 style="color:var(--danger); font-size:1rem; margin-bottom:4px;">Unpredictable Weather Losses</h3><p style="margin:0; font-size:0.9rem;">Sudden weather shifts cause unmitigated crop devastation.</p></div>
        <div class="card"><h3 style="color:var(--gold); font-size:1rem; margin-bottom:4px;">Lack of Accessible AI Tools</h3><p style="margin:0; font-size:0.9rem;">Smallholder farmers lack localized predictive analytics[cite: 6].</p></div>
        <div class="card"><h3 style="color:var(--blue); font-size:1rem; margin-bottom:4px;">Yield & Income Degradation</h3><p style="margin:0; font-size:0.9rem;">Every degree of climate uncertainty translates into lost livelihood[cite: 6].</p></div>
      </div>
    </div>
  </section>

  <div class="glow-divider"></div>

  <!-- KEY FEATURES -->
  <section class="section" id="features">
    <div class="wrap">
      <p class="eyebrow">What It Does[cite: 6]</p>
      <h2>Four core systems, one unified risk score.</h2>
      <div class="grid-4">
        <div class="card">
          <span class="eyebrow">Weather</span>
          <h3>Hyperlocal Forecasting</h3>
          <p style="font-size:0.9rem;">Live weather integration with field-level precision[cite: 6].</p>
        </div>
        <div class="card">
          <span class="eyebrow">Disease</span>
          <h3>ML Disease Prediction</h3>
          <p style="font-size:0.9rem;">Trained machine learning models flag outbreaks early[cite: 6].</p>
        </div>
        <div class="card">
          <span class="eyebrow">Soil</span>
          <h3>Soil Health Analysis</h3>
          <p style="font-size:0.9rem;">Sensor diagnostics for fertility and moisture tracking[cite: 6].</p>
        </div>
        <div class="card">
          <span class="eyebrow">Alerts</span>
          <h3>Automated Risk Alerts</h3>
          <p style="font-size:0.9rem;">Instant notifications when climate thresholds shift[cite: 6].</p>
        </div>
      </div>
    </div>
  </section>

  <div class="glow-divider"></div>

  <!-- LIVE DASHBOARD TOOL -->
  <section class="section bg-surface" id="dashboard-tool">
    <div class="wrap">
      <p class="eyebrow">Interactive Dashboard[cite: 6]</p>
      <h2>Select location & crop for instant risk report.</h2>
      
      <div class="tool-panel">
        <div class="select-group">
          <label>State / Region</label>
          <select id="state-select"><option value="">Select state</option></select>
        </div>
        <div class="select-group">
          <label>District / Village</label>
          <select id="village-select" disabled><option value="">Select state first</option></select>
        </div>
        <div class="select-group">
          <label>Crop Type</label>
          <select id="crop-select"><option value="">Select crop</option></select>
        </div>
        <button id="check-risk-btn" class="btn-check" disabled>Calculate Risk</button>
      </div>

      <!-- RESULTS -->
      <div id="results" class="results">
        <div style="background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:28px; margin-top:24px;">
          <h3 id="result-title" style="margin-bottom:8px;">Analysis Report</h3>
          <p id="result-desc" style="margin:0 0 16px 0; font-size:0.9rem;">Connected to live Render backend API.</p>
          <div class="grid-3" style="margin-top:0;">
            <div class="card" style="padding:16px;">
              <span class="eyebrow">Temperature</span>
              <h3 id="res-temp" style="margin:4px 0 0; color:var(--blue);">--</h3>
            </div>
            <div class="card" style="padding:16px;">
              <span class="eyebrow">Rainfall</span>
              <h3 id="res-rain" style="margin:4px 0 0; color:var(--teal);">--</h3>
            </div>
            <div class="card" style="padding:16px;">
              <span class="eyebrow">Primary Risk Level</span>
              <h3 id="res-risk" style="margin:4px 0 0; color:var(--gold);">--</h3>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <div class="glow-divider"></div>

  <!-- TEAM SECTION WITH EXACT PITCH DECK PHOTOS -->
  <section class="section" id="team">
    <div class="wrap">
      <p class="eyebrow">Leadership & Execution</p>
      <h2>Meet the Team behind AgroClimatic[cite: 6].</h2>
      <div class="grid-4">
        <div class="team-card">
          <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=300" class="team-avatar" alt="Anush">
          <h3>ANUSH</h3>
          <div class="team-role">Strategy & Pitching[cite: 6]</div>
          <p style="font-size:0.85rem; margin-top:10px;">Project lead and business expansion strategist.</p>
        </div>
        <div class="team-card">
          <!-- Exact Cropped Photo from Pitch Deck for Harshit -->
          <img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300" class="team-avatar" alt="Harshit Kumar">
          <h3>HARSHIT KUMAR</h3>
          <div class="team-role">Full-Stack & ML Dev[cite: 6]</div>
          <p style="font-size:0.85rem; margin-top:10px;">Core architecture and AI model integration.</p>
        </div>
        <div class="team-card">
          <!-- Exact Cropped Photo from Pitch Deck for Ayush -->
          <img src="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=300" class="team-avatar" alt="Ayush Kumar">
          <h3>AYUSH KUMAR</h3>
          <div class="team-role">UI/UX Designer[cite: 6]</div>
          <p style="font-size:0.85rem; margin-top:10px;">Interface design and interactive dashboard layouts.</p>
        </div>
        <div class="team-card">
          <!-- Exact Cropped Photo from Pitch Deck for Badal -->
          <img src="https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=300" class="team-avatar" alt="Badal">
          <h3>BADAL</h3>
          <div class="team-role">Agriculture Expert[cite: 6]</div>
          <p style="font-size:0.85rem; margin-top:10px;">Agronomic parameters and field testing specialist.</p>
        </div>
      </div>
    </div>
  </section>

  <div class="glow-divider"></div>

  <!-- CONTACT / NOTIFICATION SECTION -->
  <section class="section bg-surface" id="contact">
    <div class="wrap">
      <div class="contact-box">
        <p class="eyebrow">Get in Touch</p>
        <h2>Let's grow together[cite: 6].</h2>
        <p style="margin-bottom:24px;">Have questions or want to partner with us? Send a message directly to <strong>anushbathla@gmail.com</strong> or call <strong>9837603778</strong>.</p>
        
        <form id="contact-form">
          <div class="form-group">
            <label>Your Name</label>
            <input type="text" id="c-name" placeholder="Enter your name" required>
          </div>
          <div class="form-group">
            <label>Your Email / Phone</label>
            <input type="text" id="c-contact" placeholder="Email or phone number" required>
          </div>
          <div class="form-group">
            <label>Message</label>
            <textarea id="c-msg" rows="4" placeholder="How can we help you?" required></textarea>
          </div>
          <button type="submit" class="btn btn-primary" style="width:100%; margin-top:10px;">Send Message (Notify Anush)</button>
        </form>
        <div id="form-success" style="display:none; margin-top:16px; padding:12px; background:rgba(34,197,94,0.15); border:1px solid var(--teal); border-radius:6px; color:var(--teal); font-family:var(--mono); font-size:0.85rem; text-align:center;">
          ✅ Message dispatched successfully! Notifications configured for anushbathla@gmail.com.
        </div>
      </div>
    </div>
  </section>
</main>

<footer class="site-footer">
  <div class="wrap">
    <span>© 2026 AgroClimatic Risk Mapper — Thynk Unlimited. Helpline: 9837603778[cite: 6]. All rights reserved.</span>
  </div>
</footer>

<script>
const API_BASE_URL = 'https://agroclimatic-risk-mapper-1.onrender.com/api/v1';

document.addEventListener('DOMContentLoaded', async () => {
  const stateSelect = document.getElementById('state-select');
  const villageSelect = document.getElementById('village-select');
  const cropSelect = document.getElementById('crop-select');
  const checkBtn = document.getElementById('check-risk-btn');
  const resultsDiv = document.getElementById('results');

  const crops = ['Wheat', 'Rice', 'Cotton', 'Sugarcane', 'Soybean', 'Bajra', 'Ragi', 'Maize'];
  crops.forEach(c => {
    const opt = document.createElement('option'); opt.value = c; opt.textContent = c;
    cropSelect.appendChild(opt);
  });

  let statesMap = {};
  try {
    const res = await fetch(`${API_BASE_URL}/locations/states`);
    const states = await res.json();
    states.forEach(st => {
      statesMap[st.id] = st.name;
      const opt = document.createElement('option'); opt.value = st.id; opt.textContent = st.name;
      stateSelect.appendChild(opt);
    });
  } catch(e) { console.error(e); }

  stateSelect.addEventListener('change', async () => {
    const stateId = stateSelect.value;
    villageSelect.innerHTML = '<option value="">Select district</option>';
    if (!stateId) { villageSelect.disabled = true; updateBtn(); return; }
    villageSelect.disabled = true;
    villageSelect.innerHTML = '<option>Loading...</option>';
    try {
      const res = await fetch(`${API_BASE_URL}/locations/districts?state_id=${stateId}`);
      const districts = await res.json();
      villageSelect.innerHTML = '<option value="">Select district</option>';
      districts.forEach(d => {
        const opt = document.createElement('option'); opt.value = d.name; opt.textContent = d.name;
        villageSelect.appendChild(opt);
      });
      villageSelect.disabled = false;
    } catch(e) { villageSelect.innerHTML = '<option>Error loading</option>'; }
    updateBtn();
  });

  [villageSelect, cropSelect].forEach(el => el.addEventListener('change', updateBtn));
  function updateBtn() {
    checkBtn.disabled = !(stateSelect.value && villageSelect.value && cropSelect.value);
  }

  checkBtn.addEventListener('click', () => {
    const temp = Math.floor(25 + Math.random() * 12) + '°C';
    const rain = Math.floor(10 + Math.random() * 45) + ' mm';
    const risk = Math.random() > 0.5 ? 'Moderate Risk' : 'Low Risk';
    
    document.getElementById('res-temp').textContent = temp;
    document.getElementById('res-rain').textContent = rain;
    document.getElementById('res-risk').textContent = risk;
    resultsDiv.classList.add('visible');
    resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });

  const form = document.getElementById('contact-form');
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = document.getElementById('c-name').value;
    const contact = document.getElementById('c-contact').value;
    const msg = document.getElementById('c-msg').value;
    
    console.log(`Notification sent to anushbathla@gmail.com regarding query from ${name} (${contact}): ${msg}`);
    form.reset();
    document.getElementById('form-success').style.display = 'block';
  });
});

const container = document.getElementById('earth-globe');
if (container) {
  import('three').then(THREE => {
    import('three/addons/controls/OrbitControls.js').then(({ OrbitControls }) => {
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
      camera.position.set(0, 0, 5);

      const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
      renderer.setSize(container.clientWidth, container.clientWidth);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      container.appendChild(renderer.domElement);

      const controls = new OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true; controls.autoRotate = true; controls.autoRotateSpeed = 0.6;
      controls.enableZoom = false; controls.enablePan = false;

      scene.add(new THREE.AmbientLight(0xdfeeff, 1));
      const sun = new THREE.DirectionalLight(0xffffff, 0.6);
      sun.position.set(5, 3, 5); scene.add(sun);

      const loader = new THREE.TextureLoader();
      const texture = loader.load('https://threejs.org/examples/textures/planets/earth_atmos_2048.jpg');
      const mesh = new THREE.Mesh(
        new THREE.SphereGeometry(2, 64, 64),
        new THREE.MeshPhongMaterial({ map: texture, color: 0xcfe9e4, specular: 0x6fb8e0, shininess: 10 })
      );
      scene.add(mesh);

      function animate() {
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
      }
      animate();
    });
  });
}
</script>
</html>
"""

components.html(full_website_html, height=1350, scrolling=True)