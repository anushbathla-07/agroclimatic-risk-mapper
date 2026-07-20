// AgroClimatic Risk Mapper - dashboard.html logic (API Connected)
document.addEventListener('DOMContentLoaded', async () => {
  const stateSelect = document.getElementById('state-select');
  const villageSelect = document.getElementById('village-select'); // Abhi hum isme districts load kar rahe hain
  const cropSelect = document.getElementById('crop-select');
  const checkBtn = document.getElementById('check-risk-btn');
  const results = document.getElementById('results');

  // FastAPI Backend URL
  const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

  // 1. Backend se States fetch karna
  try {
    const response = await fetch(`${API_BASE_URL}/locations/states`);
    const states = await response.json();
    
    states.forEach((state) => {
      const opt = document.createElement('option');
      opt.value = state.id; // Backend id
      opt.textContent = state.name;
      stateSelect.appendChild(opt);
    });
  } catch (error) {
    console.error('States load hone mein error:', error);
  }

  // Mock Crops (Inko bhi aage chal kar database mein daalenge)
  const MOCK_CROPS = ['Wheat', 'Rice', 'Cotton', 'Sugarcane', 'Soybean', 'Bajra', 'Ragi', 'Maize'];
  MOCK_CROPS.forEach((crop) => {
    const opt = document.createElement('option');
    opt.value = crop;
    opt.textContent = crop;
    cropSelect.appendChild(opt);
  });

  // 2. State select hone par dynamically Districts fetch karna
  stateSelect.addEventListener('change', async () => {
    const stateId = stateSelect.value;
    villageSelect.innerHTML = ''; 

    if (!stateId) {
      villageSelect.disabled = true;
      const opt = document.createElement('option');
      opt.textContent = 'Select state first';
      villageSelect.appendChild(opt);
    } else {
      villageSelect.disabled = true;
      const placeholder = document.createElement('option');
      placeholder.textContent = 'Loading districts...';
      villageSelect.appendChild(placeholder);

      // Backend se specific state ke districts mangwana
      try {
        const response = await fetch(`${API_BASE_URL}/locations/districts?state_id=${stateId}`);
        const districts = await response.json();

        villageSelect.innerHTML = ''; 
        const newPlaceholder = document.createElement('option');
        newPlaceholder.value = '';
        newPlaceholder.textContent = 'Select district';
        villageSelect.appendChild(newPlaceholder);

        districts.forEach((district) => {
          const opt = document.createElement('option');
          opt.value = district.id;
          opt.textContent = district.name;
          villageSelect.appendChild(opt);
        });

        villageSelect.disabled = false;
      } catch (error) {
        console.error('Districts load hone mein error:', error);
        villageSelect.innerHTML = '<option>Error loading data</option>';
      }
    }
    updateButtonState();
  });

  [villageSelect, cropSelect].forEach((el) => el.addEventListener('change', updateButtonState));

  function updateButtonState() {
    checkBtn.disabled = !(stateSelect.value && villageSelect.value && cropSelect.value);
  }

  // Risk Check Button Click
  checkBtn.addEventListener('click', () => {
      // Abhi frontend successfully backend se locations le raha hai. 
      // Agle step mein hum map aur Risk Score calculate karne wala backend API banayenge.
      alert("✅ Success! Aapka Frontend aur Backend connect ho chuka hai! States aur Districts API se aa rahe hain.");
  });
});