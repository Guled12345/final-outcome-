# EduScan Somalia - Render Deployment Package

A professional learning risk assessment application for Somaliland educational institutions.

## Features

- **Multi-language Support**: English, Somali, and Arabic interfaces
- **Professional Dashboard**: Real-time student performance analytics
- **Risk Assessment**: AI-powered learning difficulty prediction
- **Responsive Design**: Modern gradient UI with authentic cultural elements

## Deployment on Render

### Quick Deploy Button
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Manual Deployment

1. **Upload to GitHub**:
   - Create a new repository on GitHub
   - Upload all files from this package
   - Make sure the repository is public or accessible to Render

2. **Create Render Service**:
   - Go to [render.com](https://render.com)
   - Click "New" → "Web Service"
   - Connect your GitHub repository

3. **Configure Service**:
   - **Name**: `eduscan-somalia`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
   - **Instance Type**: Free tier is sufficient

4. **Environment Variables** (Optional):
   ```
   STREAMLIT_SERVER_HEADLESS=true
   STREAMLIT_SERVER_PORT=$PORT
   ```

5. **Deploy**:
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Your app will be available at: `https://your-app-name.onrender.com`

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## File Structure

```
render_deployment_package/
├── app.py                  # Main application file
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml        # Streamlit configuration
├── data/                  # Application data (auto-created)
├── README.md             # This file
└── render.yaml           # Render deployment config
```

## Technical Details

- **Framework**: Streamlit 1.28.1
- **Python**: 3.11+
- **Dependencies**: pandas, numpy, plotly, scikit-learn
- **Port**: Configured for Render's dynamic port assignment
- **Storage**: Local JSON files (automatically created)

## Support

For deployment issues or technical support, please refer to:
- [Render Documentation](https://render.com/docs)
- [Streamlit Documentation](https://docs.streamlit.io)

## License

Educational use license - Created for Somaliland educational institutions.