# Vercel Deployment Guide - VoiceXAI Frontend

## Quick Deploy to Vercel (No Port Configuration)

### Option 1: One-Click Deploy
1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Connect your GitHub account
4. Import your `colleenpridemore/VoicexAI` repository
5. Set build settings:
   - **Framework**: Vite
   - **Root Directory**: `frontend-app`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### Option 2: Vercel CLI Deploy
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from frontend directory
cd /workspaces/VoicexAI/frontend-app
vercel --prod

# Follow prompts - Vercel auto-detects Vite settings
```

### Option 3: GitHub Actions Auto-Deploy
Create `.github/workflows/vercel.yml`:
```yaml
name: Deploy to Vercel
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: cd frontend-app && npm ci
      - name: Build
        run: cd frontend-app && npm run build
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
          working-directory: frontend-app
```

## Environment Variables (Optional)
Set in Vercel dashboard:
- `VITE_API_BASE_URL` → Your API endpoint
- `VITE_AGENT_BASE_URL` → Your agent network endpoint

## BGI25 Hackathon Ready! 🚀
- ✅ No port conflicts
- ✅ Auto-scaling
- ✅ Global CDN
- ✅ HTTPS included
- ✅ Custom domain support

Your Wagwan Swarm frontend will be live at: `https://your-project.vercel.app`