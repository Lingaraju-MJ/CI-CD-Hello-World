# ZAP scan notes

I ran OWASP ZAP against the local Hello World site.

ZAP is a security scanner. The baseline scan opens the site, looks at a few extra URLs, and checks the responses for common problems. I used the Docker image so I did not have to install ZAP on Windows.

I did not use Burp Suite. Burp is a desktop tool. For this small app, ZAP was enough.

## How I ran it

The app was already up from `docker compose up -d`.

ZAP has to sit on the same Docker network as the app. From inside that network the site is `http://app:8000`, not localhost.

```powershell
docker run --rm --network ci-cd-hello-world_default -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t http://app:8000
```

The first run downloads the ZAP image. That takes a few minutes. After that the scan itself is shorter.

ZAP also tries `/robots.txt` and `/sitemap.xml`. Those return 404 here. That is normal. We never added those files.

## Result

- 3 URLs checked (home + those two 404s)
- 0 FAIL
- 7 WARN
- 60 PASS

FAIL would be things like XSS or a clearly broken auth check. This app only returns a greeting, so I did not expect those.

The 7 warnings are all about HTTP headers we never set. Flask's default response is a bit open.

## The 7 warnings

**1. Missing Anti-clickjacking Header**  
No `X-Frame-Options` header. Another site could put our page inside an iframe. For a greeting page this is a small risk, but scanners always flag it.

**2. X-Content-Type-Options Header Missing**  
No `nosniff`. The browser might try to guess the content type.

**3. Server Leaks Version Information**  
The `Server` header shows Werkzeug (the library Flask uses) and its version. That tells an attacker what we run. I saw this on `/`, `/robots.txt`, and `/sitemap.xml`.

**4. Content Security Policy (CSP) Header Not Set**  
CSP tells the browser which scripts and styles are allowed. We have no JavaScript here, so this is extra hardening, not a live bug.

**5. Storable and Cacheable Content**  
The page can be stored in a cache. Fine for a public hello world. Not fine later if the page had a user name or a token.

**6. Permissions Policy Header Not Set**  
This header turns off browser features (camera, mic, and so on). We do not use any of those.

**7. Cross-Origin-Embedder-Policy Header Missing**  
Another browser isolation header. Same story: not set, because we never added security headers at all.

## What this means

The scan did not find an injection hole or a leaked secret. It found that a brand new Flask app does not send the headers people expect in production.

I added the first two in `server.py` so every response gets `X-Frame-Options: DENY` and `X-Content-Type-Options: nosniff`. I did not re-run ZAP. The other five warnings are still there on purpose.
