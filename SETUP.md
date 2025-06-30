# Setup Guide for Construction Project Database API

## Environment Variable Configuration

### Option 1: Project-level .env file (Recommended)
1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file with your actual API key:
   ```bash
   # OpenAI API Configuration
   OPENAI_API_KEY=sk-proj-your-actual-api-key-here
   ```

### Option 2: System Environment Variable
Set the environment variable in your shell:

**For macOS/Linux:**
```bash
export OPENAI_API_KEY="sk-proj-your-actual-api-key-here"
```

**For Windows:**
```cmd
set OPENAI_API_KEY=sk-proj-your-actual-api-key-here
```

### Option 3: User Home Directory
Create a `.env` file in your home directory:
```bash
echo "OPENAI_API_KEY=sk-proj-your-actual-api-key-here" > ~/.env
```

## Security Best Practices

### ✅ Do:
- Store API keys in environment variables
- Use `.env` files that are gitignored
- Keep API keys out of your source code
- Use different API keys for development/production
- Regularly rotate your API keys

### ❌ Don't:
- Commit API keys to version control
- Share API keys in chat/email
- Hard-code API keys in your source code
- Store API keys in public repositories

## Getting Your OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and store it securely

## Verification

Test your setup:
```bash
python -c "
from API import ConstructionProjectAPI
api = ConstructionProjectAPI()
result = api.query_from_natural_language('How many rooms are there?')
print('Setup successful!' if result['success'] else 'Setup failed: ' + str(result['error']))
"
```

## Troubleshooting

### "OPENAI_API_KEY not found"
- Check if your `.env` file exists and contains the key
- Verify the key format (starts with `sk-proj-`)
- Make sure there are no extra spaces or quotes

### "API quota exceeded"
- Check your OpenAI billing and usage
- Verify your API key is active
- Consider upgrading your OpenAI plan

### Import errors
- Make sure you've installed dependencies:
  ```bash
  pip install openai python-dotenv
  ```
