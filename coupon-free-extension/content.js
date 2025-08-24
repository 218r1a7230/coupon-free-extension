chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'fetchCoupons') {
    fetchCoupons(request.site);
  }
});

async function fetchCoupons(site) {
  try {
    const response = await fetch(`http://localhost:8000/coupons?site=${site}`); // Replace with deployed backend URL
    const coupons = await response.json();
    injectUI(coupons, site);
  } catch (error) {
    console.error('Error fetching coupons:', error);
  }
}

function injectUI(coupons, site) {
  if (document.getElementById('coupon-guard-panel')) return; // Avoid duplicates

  const panel = document.createElement('div');
  panel.id = 'coupon-guard-panel';
  panel.style.position = 'fixed';
  panel.style.top = '10px';
  panel.style.right = '10px';
  panel.style.background = 'white';
  panel.style.border = '1px solid #ccc';
  panel.style.padding = '10px';
  panel.style.zIndex = '9999';
  panel.style.maxWidth = '300px';
  panel.style.boxShadow = '0 2px 10px rgba(0,0,0,0.2)';

  const title = document.createElement('h3');
  title.textContent = `Valid Coupons for ${site.charAt(0).toUpperCase() + site.slice(1)}`;
  panel.appendChild(title);

  coupons.forEach(coupon => {
    const item = document.createElement('div');
    item.style.marginBottom = '10px';

    const codeSpan = document.createElement('span');
    codeSpan.textContent = `${coupon.code} - ${coupon.discount} (Success: ${(coupon.success_rate * 100).toFixed(0)}%)`;
    item.appendChild(codeSpan);

    const workedBtn = document.createElement('button');
    workedBtn.textContent = 'Worked';
    workedBtn.style.marginLeft = '5px';
    workedBtn.onclick = () => sendFeedback(coupon.code, true);
    item.appendChild(workedBtn);

    const failedBtn = document.createElement('button');
    failedBtn.textContent = "Didn't Work";
    failedBtn.style.marginLeft = '5px';
    failedBtn.onclick = () => sendFeedback(coupon.code, false);
    item.appendChild(failedBtn);

    panel.appendChild(item);
  });

  document.body.appendChild(panel);
}

async function sendFeedback(code, success) {
  try {
    await fetch('http://localhost:8000/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code, success })
    });
    alert('Feedback submitted!');
  } catch (error) {
    console.error('Error sending feedback:', error);
  }
}