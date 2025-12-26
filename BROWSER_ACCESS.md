# Browser Access

## 🌐 Access the Application in Your Browser

The application is now accessible via a web interface!

### URL
**http://localhost:8080/index.html**

### What You Can Do

1. **Enter your store ID** (or use the default: example-store.myshopify.com)
2. **Type a question** about your Shopify store analytics
3. **Click "Ask Question"** to get AI-powered insights
4. **View the results** with:
   - Natural language answer
   - Confidence level
   - Data type analyzed
   - Records processed
   - Intent classification
   - Time period extracted
   - Query used

### Example Questions to Try

- "What were my top 5 selling products last week?"
- "How much inventory should I reorder for next week?"
- "Which customers placed repeat orders in the last 90 days?"
- "What products are likely to go out of stock in 7 days?"
- "How many units of Product X will I need next month?"

### Services Running

- ✅ **Web Interface**: http://localhost:8080
- ✅ **Rails API**: http://localhost:3000
- ✅ **Python AI Service**: http://localhost:8000

### If Browser Doesn't Open Automatically

1. Open your web browser
2. Navigate to: `http://localhost:8080/index.html`
3. Or use: `http://localhost:8080/` and click on `index.html`

### Troubleshooting

**If you see "Cannot connect to API":**
- Make sure Rails API is running on port 3000
- Check: `curl http://localhost:3000/api/v1/health`

**If the page doesn't load:**
- Make sure the web server is running: `ps aux | grep "http.server"`
- Restart: `python3 -m http.server 8080`

**To stop the web server:**
```bash
pkill -f "http.server 8080"
```

### Features

- 🎨 Beautiful, modern UI
- 📱 Responsive design
- ⚡ Real-time API communication
- 💡 Example questions for quick testing
- 📊 Detailed metadata display
- ✅ Status indicators
- 🔄 Loading states

Enjoy using the Shopify AI Analytics application!

