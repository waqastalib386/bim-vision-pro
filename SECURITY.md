# Security Policy - BIM Vision Pro

## 🔒 Critical Security Considerations

### API Key Protection

**NEVER commit API keys to the repository!**

Your OpenAI API key is **highly sensitive** and should be protected at all times.

### Protected Files

The following files contain sensitive information and are **automatically ignored** by `.gitignore`:

- `backend/.env` - Contains your OpenAI API key
- `backend/uploads/` - Contains user-uploaded IFC files
- Any file with `.env` extension
- Credential files (*.pem, *.key, *.cert)

### Setup Instructions

1. **Initial Setup:**
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env and add your actual API key
   ```

2. **Verify Protection:**
   ```bash
   # Run this from project root
   git status

   # .env files should NOT appear in the list
   # If they do, DO NOT commit them!
   ```

3. **Check Before Committing:**
   ```bash
   # Always review what you're about to commit
   git diff --staged

   # Look for any API keys or sensitive data
   # If found, remove them immediately
   ```

## 🚨 What to Do If You Accidentally Commit an API Key

If you accidentally commit your API key to GitHub:

1. **Immediately revoke the API key:**
   - Go to https://platform.openai.com/api-keys
   - Delete the compromised key
   - Create a new API key

2. **Remove from Git History:**
   ```bash
   # WARNING: This rewrites history - coordinate with team members!
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch backend/.env" \
     --prune-empty --tag-name-filter cat -- --all

   # Force push (DANGEROUS - only if necessary)
   git push origin --force --all
   ```

3. **Alternative (Simpler):**
   - If the repository is new and hasn't been shared, delete it and start fresh
   - Create a new repository with proper .gitignore from the beginning

## 🛡️ Best Practices

### Environment Variables

- ✅ **DO:** Use `.env` files for local development
- ✅ **DO:** Use `.env.example` as a template (without real keys)
- ✅ **DO:** Document required environment variables
- ❌ **DON'T:** Commit `.env` files to version control
- ❌ **DON'T:** Share API keys via email, chat, or screenshots
- ❌ **DON'T:** Hardcode API keys in source code

### User Data Protection

- All uploaded IFC files are stored in `backend/uploads/`
- This directory is ignored by Git to protect user data
- Implement proper access controls in production
- Consider encryption for sensitive building data

### Production Deployment

When deploying to production:

1. **Use environment variables** from your hosting platform:
   - Heroku: Use Config Vars
   - Vercel: Use Environment Variables
   - AWS: Use Parameter Store or Secrets Manager
   - Azure: Use Key Vault

2. **Enable HTTPS** for all API communication

3. **Implement rate limiting** to prevent API abuse

4. **Monitor API usage** at https://platform.openai.com/usage

5. **Set API spending limits** to prevent unexpected charges

## 📊 API Usage Monitoring

Regularly check your OpenAI API usage:

- **Dashboard:** https://platform.openai.com/usage
- **Set alerts** for unusual activity
- **Review billing** monthly
- **Monitor rate limits** to avoid service disruptions

## 🔐 Additional Security Measures

### CORS Configuration

Current backend allows all origins (`*`). For production:

```python
# backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific origins only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Input Validation

- Always validate IFC file uploads
- Sanitize user questions before sending to OpenAI
- Implement file size limits
- Check file types before processing

### Error Handling

- Don't expose internal errors to users
- Log errors securely server-side
- Avoid leaking system information in error messages

## 📞 Reporting Security Issues

If you discover a security vulnerability:

1. **DO NOT** create a public GitHub issue
2. Email the maintainer directly with details
3. Wait for confirmation before public disclosure
4. Allow reasonable time for a fix to be developed

## ✅ Pre-Commit Checklist

Before every commit:

- [ ] Run `git status` to check staged files
- [ ] Verify no `.env` files are staged
- [ ] Review `git diff --staged` for sensitive data
- [ ] Check that API keys are not in code
- [ ] Ensure user data files are not included
- [ ] Test that .gitignore is working correctly

## 📚 Resources

- [OpenAI API Best Practices](https://platform.openai.com/docs/guides/safety-best-practices)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

**Remember:** Security is everyone's responsibility. When in doubt, ask before committing!

© 2026 BIM Vision Pro. All rights reserved.
