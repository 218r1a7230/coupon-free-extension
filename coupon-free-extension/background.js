chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    const supportedSites = ['amazon.com', 'bestbuy.com'];
    const url = new URL(tab.url);
    if (supportedSites.some(site => url.hostname.includes(site))) {
      chrome.tabs.sendMessage(tabId, { action: 'fetchCoupons', site: url.hostname.split('.')[1] });
    }
  }
});