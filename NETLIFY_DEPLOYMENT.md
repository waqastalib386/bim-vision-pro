# Netlify Deployment Guide
## BIM Vision Pro - Frontend Deployment

Complete guide for deploying your BIM Vision Pro React frontend to Netlify.

---

## ✅ What's Been Configured

Your frontend is now ready for Netlify deployment with the following setup:

### 1. **Environment Variable Configuration**

**File:** [frontend/.env.production](frontend/.env.production)
```env
VITE_API_URL=https://bim-vision-pro.onrender.com
```

**Note:** This file is NOT committed to Git (ignored by .gitignore). You'll set this in Netlify dashboard instead.

### 2. **Netlify Configuration**

**File:** [frontend/netlify.toml](frontend/netlify.toml)
- Build command: `npm run build`
- Publish directory: `dist`
- Client-side routing support (redirects)
- Security headers
- Static asset caching

### 3. **API Integration**

**File:** [frontend/src/App.jsx](frontend/src/App.jsx)
```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

All API calls now use the environment variable, which automatically switches between:
- **Development:** http://localhost:8000
- **Production:** https://bim-vision-pro.onrender.com

### 4. **Build Verification**

✅ Production build tested successfully:
```
dist/index.html                   0.79 kB │ gzip:  0.42 kB
dist/assets/index-CaqY-9kk.css   20.79 kB │ gzip:  4.26 kB
dist/assets/index-sJ5AV9og.js   213.96 kB │ gzip: 67.90 kB
✓ built in 4.96s
```

### 5. **Git Repository**

✅ Changes committed and pushed to GitHub:
```
Repository: https://github.com/waqastalib386/bim-vision-pro
Branch: main
Commit: "Configure frontend for Netlify deployment"
```

---

## 🚀 Deploy to Netlify

### Step 1: Connect to Netlify

1. **Go to Netlify:** https://app.netlify.com

2. **Click "Add new site"** → "Import an existing project"

3. **Connect to GitHub:**
   - Authorize Netlify to access your GitHub
   - Select repository: `waqastalib386/bim-vision-pro`

4. **Configure build settings:**

   Netlify should auto-detect settings from `netlify.toml`, but verify:

   ```
   Base directory: frontend
   Build command: npm run build
   Publish directory: frontend/dist
   ```

5. **Click "Deploy site"**

### Step 2: Set Environment Variables

**IMPORTANT:** Set the backend URL in Netlify dashboard.

1. Go to **Site settings** → **Environment variables**

2. Click **Add a variable**

3. Add:
   ```
   Key: VITE_API_URL
   Value: https://bim-vision-pro.onrender.com
   ```

4. Click **Save**

5. **Redeploy** the site:
   - Go to **Deploys** tab
   - Click **Trigger deploy** → **Deploy site**

### Step 3: Configure Custom Domain (Optional)

1. Go to **Site settings** → **Domain management**

2. Click **Add custom domain**

3. Enter your domain (e.g., `bim-vision-pro.yourdomain.com`)

4. Follow DNS configuration instructions

5. Enable HTTPS (automatic with Netlify)

---

## 📋 Deployment Checklist

- [x] Frontend configured with environment variables
- [x] `netlify.toml` created with build settings
- [x] API calls updated to use `VITE_API_URL`
- [x] Production build tested successfully
- [x] Changes committed to Git
- [x] Changes pushed to GitHub
- [ ] Connected GitHub repo to Netlify
- [ ] Set `VITE_API_URL` in Netlify dashboard
- [ ] Deployed to Netlify
- [ ] Verified production site works
- [ ] (Optional) Custom domain configured

---

## 🔍 Verify Deployment

After deploying, verify your site:

### 1. Check Site URL

Netlify provides a URL like: `https://your-site-name.netlify.app`

### 2. Test Functionality

1. **Open your Netlify URL**
2. **Upload an IFC file** - should connect to Render backend
3. **View AI analysis** - should show Hinglish results
4. **Ask questions** - chat should work
5. **Check cost estimation** - should calculate correctly
6. **View validation** - should show errors/warnings

### 3. Check Console for Errors

Press F12 to open DevTools and check:
- No CORS errors
- API calls going to correct backend URL
- All assets loading correctly

### 4. Test on Mobile

Netlify preview on mobile devices to ensure responsive design works.

---

## 🛠️ Troubleshooting

### Issue: "Failed to fetch" or CORS errors

**Solution:**
- Verify `VITE_API_URL` is set in Netlify dashboard
- Check backend CORS settings allow requests from Netlify domain
- Ensure backend is running on Render

### Issue: 404 on page refresh

**Solution:**
- Verify `netlify.toml` redirects are configured
- The redirect rule `/* -> /index.html` should handle client-side routing

### Issue: Environment variable not working

**Solution:**
- Ensure variable name is exactly `VITE_API_URL` (Vite requires `VITE_` prefix)
- Redeploy after setting environment variables
- Check build logs for the value being used

### Issue: Build fails on Netlify

**Solution:**
- Check Netlify build logs for specific error
- Verify `package.json` has all dependencies
- Ensure Node version is compatible (18+)
- Check base directory is set to `frontend`

---

## 📊 Expected URLs

After deployment:

- **Frontend (Netlify):** `https://your-site-name.netlify.app`
- **Backend (Render):** `https://bim-vision-pro.onrender.com`
- **API Endpoint:** `https://bim-vision-pro.onrender.com/api/upload-ifc`

---

## 🔄 Continuous Deployment

Netlify automatically deploys when you push to GitHub:

1. Make changes locally
2. Commit: `git commit -m "your message"`
3. Push: `git push origin main`
4. Netlify auto-deploys in ~2-3 minutes

**View deployment status:**
- Netlify dashboard → Deploys tab
- GitHub commit shows Netlify status badge

---

## 📈 Production Optimizations

Your build already includes:

✅ **Code splitting** - Vite automatic chunking
✅ **Tree shaking** - Unused code removed
✅ **Minification** - CSS and JS minified
✅ **Gzip compression** - Assets compressed
✅ **Asset hashing** - Cache busting
✅ **Security headers** - XSS, frame protection

**Build size:**
- HTML: 0.79 kB (gzipped: 0.42 kB)
- CSS: 20.79 kB (gzipped: 4.26 kB)
- JS: 213.96 kB (gzipped: 67.90 kB)

---

## 🔐 Security Considerations

1. **HTTPS Enabled:** Netlify provides free SSL
2. **Security Headers:** Configured in `netlify.toml`
3. **No API Keys in Frontend:** All keys stay in backend
4. **CORS Configured:** Backend allows Netlify domain
5. **Input Validation:** All user inputs validated

---

## 📚 Additional Resources

- [Netlify Docs](https://docs.netlify.com/)
- [Vite Environment Variables](https://vitejs.dev/guide/env-and-mode.html)
- [Custom Domains on Netlify](https://docs.netlify.com/domains-https/custom-domains/)

---

## 🎉 Next Steps

1. **Deploy to Netlify** using steps above
2. **Share your live URL** with users
3. **Monitor analytics** in Netlify dashboard
4. **Set up custom domain** (optional)
5. **Enable form notifications** (optional)

---

**Last Updated:** 2026-01-20
**Repository:** https://github.com/waqastalib386/bim-vision-pro
**Backend:** https://bim-vision-pro.onrender.com

---

© 2026 BIM Vision Pro. All rights reserved.
