"""
Web Push Notification & Service Worker System for CineStories.
Provides:
1. PWA Service Worker (dist/sw.js) with push notification listeners, offline caching, and click handlers.
2. Web App Manifest (dist/manifest.json) for mobile and desktop browser installation.
3. Visual, tactile Web Push Opt-In Bell Button and Modal Component with bilingual support (EN/HI).
4. Client-side Notification API registration, permission request, and instant test notification trigger.
"""

from pathlib import Path
from typing import Dict, Any

SW_JS_CONTENT = """// CineStories PWA & Web Push Service Worker
const CACHE_NAME = 'cinestories-v2';
const CORE_ASSETS = [
  '/',
  '/assets/logo.png',
  '/manifest.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(CORE_ASSETS).catch(() => {});
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    }).then(() => self.clients.claim())
  );
});

// Real-Time Web Push Notification Event Listener
self.addEventListener('push', (event) => {
  let data = {};
  if (event.data) {
    try {
      data = event.data.json();
    } catch (e) {
      data = { title: event.data.text() };
    }
  }

  const title = data.title || '🎬 CineStories Breaking Alert';
  const options = {
    body: data.body || 'Trending now: New box office record and climax clues revealed! Tap to explore.',
    icon: data.icon || '/assets/logo.png',
    badge: data.badge || '/assets/logo.png',
    image: data.image || null,
    vibrate: [200, 100, 200],
    data: {
      url: data.url || '/'
    },
    actions: [
      { action: 'explore', title: '🔍 Read Climax' },
      { action: 'close', title: 'Dismiss' }
    ]
  };

  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});

// Notification Click Handler
self.addEventListener('notificationclick', (event) => {
  event.notification.close();

  if (event.action === 'close') {
    return;
  }

  const targetUrl = (event.notification.data && event.notification.data.url) ? event.notification.data.url : '/';

  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then((windowClients) => {
      for (let client of windowClients) {
        if (client.url === targetUrl && 'focus' in client) {
          return client.focus();
        }
      }
      if (clients.openWindow) {
        return clients.openWindow(targetUrl);
      }
    })
  );
});
"""

MANIFEST_JSON_CONTENT = """{
  "name": "CineStories - Breaking Cinema & Climax Stories",
  "short_name": "CineStories",
  "description": "Real-time Google Trends cinema stories, climax decoders, ending breakdowns, and OTT releases.",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#0b0e14",
  "theme_color": "#e50914",
  "icons": [
    {
      "src": "/assets/logo.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ]
}
"""

PUSH_NOTIFICATION_CSS = """
/* Web Push Notification Floating Bell & Modal Styling */
.push-bell-widget {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 9998;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.push-bell-btn {
  background: linear-gradient(135deg, #e50914 0%, #b80710 100%);
  color: #ffffff;
  border: none;
  border-radius: 50px;
  padding: 12px 18px;
  font-size: 14px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  box-shadow: 0 8px 24px rgba(229, 9, 20, 0.45), 0 0 0 1px rgba(255, 255, 255, 0.15);
  transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.25s ease;
  outline: none;
}

.push-bell-btn:hover {
  transform: translateY(-3px) scale(1.04);
  box-shadow: 0 12px 30px rgba(229, 9, 20, 0.6), 0 0 0 2px rgba(255, 255, 255, 0.3);
}

.push-bell-btn:active {
  transform: translateY(1px) scale(0.98);
}

.push-bell-btn .bell-icon {
  font-size: 18px;
  display: inline-block;
  animation: bellShake 3.5s ease-in-out infinite;
}

.push-bell-btn.is-subscribed {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  box-shadow: 0 8px 20px rgba(16, 185, 129, 0.4);
}

.push-bell-btn.is-subscribed .bell-icon {
  animation: none;
}

.pulse-dot {
  width: 9px;
  height: 9px;
  background-color: #facc15;
  border-radius: 50%;
  display: inline-block;
  box-shadow: 0 0 0 0 rgba(250, 204, 21, 0.7);
  animation: pulseDot 1.8s infinite;
}

@keyframes pulseDot {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(250, 204, 21, 0.7); }
  70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(250, 204, 21, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(250, 204, 21, 0); }
}

@keyframes bellShake {
  0%, 100% { transform: rotate(0); }
  2%, 6% { transform: rotate(14deg); }
  4%, 8% { transform: rotate(-14deg); }
  10% { transform: rotate(0); }
}

/* Modal Overlay */
.push-modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(5, 7, 12, 0.75);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s ease, visibility 0.3s ease;
}

.push-modal-backdrop.is-open {
  opacity: 1;
  visibility: visible;
}

.push-modal-card {
  background: linear-gradient(180deg, #161922 0%, #0c0e14 100%);
  border: 1px solid rgba(229, 9, 20, 0.35);
  border-radius: 20px;
  width: 100%;
  max-width: 440px;
  padding: 28px;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.7), 0 0 40px rgba(229, 9, 20, 0.2);
  position: relative;
  transform: translateY(20px) scale(0.96);
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  color: #ffffff;
  text-align: left;
}

.push-modal-backdrop.is-open .push-modal-card {
  transform: translateY(0) scale(1);
}

.push-modal-close {
  position: absolute;
  top: 16px;
  right: 16px;
  background: rgba(255, 255, 255, 0.08);
  border: none;
  color: #94a3b8;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}

.push-modal-close:hover {
  background: rgba(255, 255, 255, 0.2);
  color: #ffffff;
}

.push-modal-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 16px;
}

.push-modal-icon {
  width: 50px;
  height: 50px;
  border-radius: 14px;
  background: linear-gradient(135deg, rgba(229, 9, 20, 0.2) 0%, rgba(229, 9, 20, 0.05) 100%);
  border: 1px solid rgba(229, 9, 20, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  flex-shrink: 0;
}

.push-modal-title {
  font-size: 19px;
  font-weight: 800;
  line-height: 1.25;
  color: #ffffff;
  margin: 0;
}

.push-modal-body {
  font-size: 14px;
  line-height: 1.55;
  color: #cbd5e1;
  margin-bottom: 20px;
}

.push-features-list {
  list-style: none;
  padding: 0;
  margin: 0 0 24px 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.push-features-list li {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: #94a3b8;
}

.push-features-list li span.tick {
  color: #10b981;
  font-weight: 800;
}

.push-modal-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.push-btn-primary {
  background: linear-gradient(135deg, #e50914 0%, #b80710 100%);
  color: #ffffff;
  border: none;
  border-radius: 12px;
  padding: 14px 20px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 4px 16px rgba(229, 9, 20, 0.4);
}

.push-btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 22px rgba(229, 9, 20, 0.6);
}

.push-btn-secondary {
  background: rgba(255, 255, 255, 0.06);
  color: #94a3b8;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 12px 20px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}

.push-btn-secondary:hover {
  background: rgba(255, 255, 255, 0.12);
  color: #ffffff;
}

@media (max-width: 600px) {
  .push-bell-widget {
    bottom: 20px;
    right: 16px;
  }
  .push-bell-btn span.btn-label {
    display: none;
  }
  .push-bell-btn {
    padding: 12px;
    border-radius: 50%;
  }
}
"""

def get_push_notification_html(lang: str = "en") -> str:
    """Returns the visual Bell Button and Modal HTML localized for EN or HI."""
    is_hi = (lang == "hi")
    
    btn_label = "ब्रेकिंग अलर्ट्स 🔔" if is_hi else "Cinema Alerts 🔔"
    modal_title = "🎬 ब्रेकिंग सिनेमा और क्लाइमेक्स अलर्ट्स मिस न करें" if is_hi else "🎬 Never Miss a Breaking Cinema Climax"
    modal_body = (
        "Google Trends पर आते ही ट्रेंडिंग फ़िल्मों के क्लाइमेक्स ट्विस्ट, ट्रेलर सीक्रेट्स और ओटीटी रिलीज़ की तुरंत सूचना सीधे अपने स्क्रीन पर पाएं।"
        if is_hi else
        "Get instant alerts the second trending trailer easter eggs, box office milestones, and climax twists drop on Google Trends."
    )
    feature_1 = "⚡ रियल-टाइम ब्रेकिंग ट्रेलर और क्लाइमेक्स अलर्ट्स" if is_hi else "⚡ Real-time trailer & climax decoders"
    feature_2 = "🍿 जीरो स्पैम — सिर्फ उच्च-गुणवत्ता सिनेमा ट्रेंड्स" if is_hi else "🍿 Zero spam — strictly trending cinema updates"
    feature_3 = "🔕 जब चाहें एक क्लिक में बंद करें" if is_hi else "🔕 1-click easy opt-out anytime"
    
    btn_primary = "🔔 तुरंत अलर्ट्स चालू करें" if is_hi else "🔔 Enable Instant Alerts"
    btn_secondary = "बाद में" if is_hi else "Maybe Later"
    btn_test = "⚡ टेस्ट नोटिफिकेशन भेजें" if is_hi else "⚡ Send Test Push Notification"
    subscribed_msg = "✓ आप पहले से CineStories अलर्ट्स से जुड़े हैं!" if is_hi else "✓ You are subscribed to CineStories Alerts!"

    return f"""
<!-- Web Push Notification Widget & Modal -->
<div class="push-bell-widget" id="pushBellWidget">
  <button type="button" class="push-bell-btn" id="pushBellBtn" aria-label="{btn_label}">
    <span class="bell-icon">🔔</span>
    <span class="btn-label">{btn_label}</span>
    <span class="pulse-dot" id="pushPulseDot"></span>
  </button>
</div>

<div class="push-modal-backdrop" id="pushModalBackdrop" role="dialog" aria-modal="true" aria-labelledby="pushModalTitle">
  <div class="push-modal-card">
    <button type="button" class="push-modal-close" id="pushModalClose" aria-label="Close modal">&times;</button>
    <div class="push-modal-header">
      <div class="push-modal-icon">🎬</div>
      <h3 class="push-modal-title" id="pushModalTitle">{modal_title}</h3>
    </div>
    <p class="push-modal-body" id="pushModalBody">{modal_body}</p>
    <ul class="push-features-list" id="pushFeaturesList">
      <li><span class="tick">✓</span> {feature_1}</li>
      <li><span class="tick">✓</span> {feature_2}</li>
      <li><span class="tick">✓</span> {feature_3}</li>
    </ul>
    <div class="push-modal-actions" id="pushModalActions">
      <button type="button" class="push-btn-primary" id="pushEnableBtn">{btn_primary}</button>
      <button type="button" class="push-btn-secondary" id="pushDismissBtn">{btn_secondary}</button>
    </div>
  </div>
</div>
"""

def get_push_notification_script(lang: str = "en") -> str:
    """Returns the client JavaScript registering /sw.js, requesting permission, and triggering alerts."""
    is_hi = (lang == "hi")
    welcome_title = "🎬 CineStories ब्रेकिंग अलर्ट सक्रिय!" if is_hi else "🎬 CineStories Alerts Activated!"
    welcome_body = "बधाई! अब आप ट्रेंडिंग फ़िल्मों के क्लाइमेक्स और ब्रेकिंग अपडेट्स सबसे पहले पाएंगे।" if is_hi else "Awesome! You will now receive instant alerts for breaking movie scoops and climax twists."
    test_title = "🔥 आज का ट्रेंडिंग क्लाइमेक्स अलर्ट" if is_hi else "🔥 Trending Climax Scoop Decoded"
    test_body = "Google Trends पर इस फ़िल्म के क्लाइमेक्स ने मचाया तहलका! टैप करके देखें।" if is_hi else "Trending right now on Google Trends: The shocking climax twist decoded! Tap to explore."

    return f"""
    // ==========================================
    // Web Push Notification System Client Logic
    // ==========================================
    (function() {{
      const bellBtn = document.getElementById('pushBellBtn');
      const pulseDot = document.getElementById('pushPulseDot');
      const backdrop = document.getElementById('pushModalBackdrop');
      const closeBtn = document.getElementById('pushModalClose');
      const dismissBtn = document.getElementById('pushDismissBtn');
      const enableBtn = document.getElementById('pushEnableBtn');
      const actionsContainer = document.getElementById('pushModalActions');
      const modalBody = document.getElementById('pushModalBody');

      // Register PWA Service Worker
      if ('serviceWorker' in navigator) {{
        window.addEventListener('load', () => {{
          navigator.serviceWorker.register('/sw.js').then((reg) => {{
            console.log('[Push] ServiceWorker registered with scope:', reg.scope);
          }}).catch((err) => {{
            console.warn('[Push] ServiceWorker registration notice:', err);
          }});
        }});
      }}

      // Check current notification permission state
      function updateUIState() {{
        if (!('Notification' in window)) {{
          if (bellBtn) bellBtn.style.display = 'none';
          return;
        }}

        if (Notification.permission === 'granted' || localStorage.getItem('cinestories_push_enabled') === 'true') {{
          if (bellBtn) {{
            bellBtn.classList.add('is-subscribed');
            const label = bellBtn.querySelector('.btn-label');
            if (label) label.textContent = '{"अलर्ट्स चालू हैं ✓" if is_hi else "Alerts Active ✓"}';
          }}
          if (pulseDot) pulseDot.style.display = 'none';

          if (actionsContainer) {{
            actionsContainer.innerHTML = `
              <button type="button" class="push-btn-primary" id="pushTestAlertBtn">{"⚡ टेस्ट अलर्ट चलाकर देखें" if is_hi else "⚡ Send Test Push Notification"}</button>
              <button type="button" class="push-btn-secondary" id="pushCloseModalBtn">{"बंद करें" if is_hi else "Close"}</button>
            `;
            const testBtn = document.getElementById('pushTestAlertBtn');
            const closeMBtn = document.getElementById('pushCloseModalBtn');
            if (testBtn) testBtn.addEventListener('click', triggerTestNotification);
            if (closeMBtn) closeMBtn.addEventListener('click', closeModal);
          }}
          if (modalBody) {{
            modalBody.textContent = '{"✓ आप पहले से ही CineStories के रियल-टाइम ब्रेकिंग अलर्ट्स से जुड़े हुए हैं। नीचे दिए गए बटन से आप अभी एक टेस्ट नोटिफिकेशन देख सकते हैं।" if is_hi else "✓ You are actively subscribed to CineStories Breaking Cinema Alerts. Tap below to send a live test notification to your screen."}';
          }}
        }}
      }}

      function openModal() {{
        if (backdrop) backdrop.classList.add('is-open');
      }}

      function closeModal() {{
        if (backdrop) backdrop.classList.remove('is-open');
      }}

      function triggerTestNotification() {{
        closeModal();
        if ('Notification' in window && Notification.permission === 'granted') {{
          if ('serviceWorker' in navigator && navigator.serviceWorker.controller) {{
            navigator.serviceWorker.ready.then((reg) => {{
              reg.showNotification('{test_title}', {{
                body: '{test_body}',
                icon: '/assets/logo.png',
                badge: '/assets/logo.png',
                vibrate: [200, 100, 200],
                data: {{ url: window.location.pathname }}
              }});
            }});
          }} else {{
            new Notification('{test_title}', {{
              body: '{test_body}',
              icon: '/assets/logo.png'
            }});
          }}
          if (typeof showToast === 'function') {{
            showToast('{"अलर्ट भेजा गया!" if is_hi else "Test Alert Sent!"}', '{"आपके स्क्रीन पर नोटिफिकेशन पॉपअप हो गया होगा।" if is_hi else "Check your screen for the push notification!"}');
          }}
        }}
      }}

      function requestPushPermission() {{
        if (!('Notification' in window)) {{
          alert('{"आपके ब्राउज़र में नोटिफिकेशन समर्थित नहीं है।" if is_hi else "Web Notifications are not supported in this browser."}');
          return;
        }}

        Notification.requestPermission().then((permission) => {{
          if (permission === 'granted') {{
            localStorage.setItem('cinestories_push_enabled', 'true');
            updateUIState();
            closeModal();

            if (typeof celebrateSparkles === 'function') {{
              celebrateSparkles(window.innerWidth / 2, window.innerHeight / 2);
            }}
            if (typeof showToast === 'function') {{
              showToast('{"अलर्ट्स सक्रिय!" if is_hi else "Alerts Activated!"}', '{"अब आप सिनेमा के हर बड़े ट्रेंड की सूचना पाएंगे।" if is_hi else "You are now subscribed to breaking cinema scoops!"}');
            }}

            // Send immediate welcome notification
            if ('serviceWorker' in navigator && navigator.serviceWorker.controller) {{
              navigator.serviceWorker.ready.then((reg) => {{
                reg.showNotification('{welcome_title}', {{
                  body: '{welcome_body}',
                  icon: '/assets/logo.png',
                  badge: '/assets/logo.png',
                  data: {{ url: window.location.pathname }}
                }});
              }});
            }} else {{
              new Notification('{welcome_title}', {{
                body: '{welcome_body}',
                icon: '/assets/logo.png'
              }});
            }}
          }} else {{
            closeModal();
          }}
        }});
      }}

      // Event Listeners
      if (bellBtn) bellBtn.addEventListener('click', openModal);
      if (closeBtn) closeBtn.addEventListener('click', closeModal);
      if (dismissBtn) dismissBtn.addEventListener('click', closeModal);
      if (enableBtn) enableBtn.addEventListener('click', requestPushPermission);
      if (backdrop) {{
        backdrop.addEventListener('click', (e) => {{
          if (e.target === backdrop) closeModal();
        }});
      }}

      // Initialize state on page load
      updateUIState();
    }})();
"""

def write_push_assets(dist_dir: Path):
    """Writes sw.js and manifest.json into the target dist directory."""
    dist_dir.mkdir(parents=True, exist_ok=True)
    
    sw_path = dist_dir / "sw.js"
    with open(sw_path, "w", encoding="utf-8") as f:
        f.write(SW_JS_CONTENT)
    print(f"[Push] Wrote service worker to: {sw_path}")

    manifest_path = dist_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(MANIFEST_JSON_CONTENT)
    print(f"[Push] Wrote web manifest to: {manifest_path}")

    # Also sync into root directory for local serving
    with open(Path("sw.js"), "w", encoding="utf-8") as f:
        f.write(SW_JS_CONTENT)
    with open(Path("manifest.json"), "w", encoding="utf-8") as f:
        f.write(MANIFEST_JSON_CONTENT)
