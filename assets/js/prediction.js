// AgroClimatic Risk Mapper — prediction.html logic
document.addEventListener('DOMContentLoaded', () => {
  const cropSelect = document.getElementById('crop-select');
  const stateSelect = document.getElementById('state-select');
  const stageSelect = document.getElementById('stage-select');
  const predictBtn = document.getElementById('predict-btn');
  const results = document.getElementById('results');
  const list = document.getElementById('prediction-list');

  AGRO_DATA.crops.forEach((crop) => {
    const opt = document.createElement('option');
    opt.value = crop; opt.textContent = crop;
    cropSelect.appendChild(opt);
  });
  Object.keys(AGRO_DATA.states).forEach((state) => {
    const opt = document.createElement('option');
    opt.value = state; opt.textContent = state;
    stateSelect.appendChild(opt);
  });
  AGRO_DATA.stages.forEach((stage) => {
    const opt = document.createElement('option');
    opt.value = stage; opt.textContent = stage;
    stageSelect.appendChild(opt);
  });

  [cropSelect, stateSelect, stageSelect].forEach((el) =>
    el.addEventListener('change', () => {
      predictBtn.disabled = !(cropSelect.value && stateSelect.value && stageSelect.value);
    })
  );

  predictBtn.addEventListener('click', () => {
    const predictions = predictDiseases(cropSelect.value, stateSelect.value, stageSelect.value);
    list.innerHTML = '';
    predictions.forEach((p) => {
      const level = levelFromScore(p.prob);
      const card = document.createElement('div');
      card.className = 'prediction-card';
      card.innerHTML = `
        <div>
          <h4>${p.name}</h4>
          <p>${cropSelect.value} · ${stateSelect.value} · ${stageSelect.value} stage</p>
        </div>
        <span class="prediction-prob" style="color:${LEVEL_COLOR[level]}">${p.prob}%</span>
      `;
      list.appendChild(card);
    });
    results.classList.add('visible');
    results.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
});