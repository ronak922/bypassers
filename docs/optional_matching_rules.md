By default, the script will not run on the following sites:
- Youtube `*://*.youtube.com/shorts/*`_(@match)_ (which is used for redirecting shorts)
- Google:
    - Drive/Docs `/^(https?:\/\/)(drive|docs)\.google\.com(\/.*)/`_(@include)_ (which is used for Auto-DL from Drive/Docs)
    - redirects `/^https?:\/\/(?:www\.)?google\.com\/url.*[?&]q=/`_(@include)_ (used for bypassing these redirects) 
    - Recaptcha `*://*/recaptcha/api2/*`_(@match)_ or `/^(?:https?:\/\/)?(?:www\.)?(?:google\.com|recaptcha\.net)\/recaptcha\/api2\/.*$/`_(@include)_ (used for Auto-Open of captchas in many sites).
- Twitter `*://*.twitter.com/*`_(@match)_ Bypass redirects
- TikTok `*://*.tiktok.com/*`_(@match)_ Bypass redirects
- Facebook `*://*.facebook.com/*`_(@match)_ Bypass redirects
- VK `*://*.vk.com/*`_(@match)_ Bypass redirects

These can be re-enabled manually in your userscript manager by adding the mentioned matching rules in the script settings.