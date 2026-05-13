/*
  Portable consent-aware analytics loader.
  Replace ANALYTICS_LOADER with a function that loads the approved analytics tool.
  Do not load non-essential analytics or marketing scripts before consent where
  consent is legally required.
*/
(function () {
  const STORAGE_KEY = "site_consent_v1";

  function getConsent() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
    } catch (_) {
      return {};
    }
  }

  function setConsent(value) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      analytics: Boolean(value.analytics),
      marketing: Boolean(value.marketing),
      updatedAt: new Date().toISOString()
    }));
    window.dispatchEvent(new CustomEvent("site-consent-change", { detail: getConsent() }));
  }

  function loadAnalyticsWhenAllowed() {
    const consent = getConsent();
    if (!consent.analytics || window.__siteAnalyticsLoaded) return;
    window.__siteAnalyticsLoaded = true;
    if (typeof window.ANALYTICS_LOADER === "function") {
      window.ANALYTICS_LOADER();
    }
  }

  window.SiteConsent = { get: getConsent, set: setConsent, loadAnalyticsWhenAllowed };
  window.addEventListener("site-consent-change", loadAnalyticsWhenAllowed);
  loadAnalyticsWhenAllowed();
}());
