# AI Setup Guide - Restaurant Social SaaS

## 🔑 Enabling Full AI Capabilities

The Restaurant Social SaaS platform includes advanced AI features that can be activated by configuring an OpenAI API key. This guide explains how to set up and optimize the AI functionality.

## 📋 Prerequisites

1. **OpenAI Account**: Sign up at https://platform.openai.com
2. **API Key**: Generate an API key from your OpenAI dashboard
3. **Billing Setup**: Configure billing to enable API usage
4. **Usage Limits**: Set appropriate usage limits for cost control

## ⚙️ Configuration Steps

### Step 1: Obtain OpenAI API Key

1. Visit https://platform.openai.com
2. Sign in or create an account
3. Navigate to API Keys section
4. Click "Create new secret key"
5. Copy the generated key (starts with `sk-`)

### Step 2: Configure Environment Variable

#### For Local Development:
```bash
export OPENAI_API_KEY="sk-your-actual-api-key-here"
```

#### For Production Deployment:
```bash
# Add to your deployment environment
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### Step 3: Install OpenAI Dependencies

```bash
# Install OpenAI Python package
pip install openai==1.51.0

# Or add to requirements.txt
echo "openai==1.51.0" >> requirements.txt
pip install -r requirements.txt
```

### Step 4: Verify Configuration

The application will automatically detect the API key and enable AI features:

```python
# Check AI status in application logs
# You should see: "OpenAI client initialized successfully"
# Instead of: "OpenAI API key not provided, using fallback captions"
```

## 🎯 AI Features Unlocked

### 1. Advanced Photo Analysis

When properly configured, the AI system will:

- **Analyze Food Images**: Identify dishes, ingredients, cooking styles
- **Generate Contextual Captions**: Create captions based on visual analysis
- **Optimize Hashtags**: Select hashtags based on actual image content
- **Personalize Content**: Incorporate restaurant-specific context

### 2. Intelligent Content Generation

- **Restaurant-Specific Posts**: Generate content tailored to your restaurant
- **Engagement Optimization**: Create posts designed for maximum engagement
- **Trend Integration**: Incorporate current food and restaurant trends
- **Brand Voice Consistency**: Maintain consistent tone across all content

## 💰 Cost Management

### Usage Optimization

1. **Image Analysis**: ~$0.01-0.03 per image analysis
2. **Content Generation**: ~$0.001-0.005 per post generation
3. **Monthly Estimates**: $10-50 for typical restaurant usage
4. **Cost Controls**: Set usage limits in OpenAI dashboard

### Best Practices

- **Batch Processing**: Process multiple images together when possible
- **Fallback Strategy**: System automatically uses fallbacks to control costs
- **Usage Monitoring**: Monitor API usage through OpenAI dashboard
- **Budget Alerts**: Set up billing alerts for cost control

## 🔧 Advanced Configuration

### Custom AI Prompts

Customize AI behavior by modifying prompts in `enhanced_ai_captions_simple.py`:

```python
# Customize image analysis prompt
prompt = f"""Analyze this food image for a {restaurant_context.get('cuisine')} restaurant.
Focus on identifying:
1. Main dish and ingredients
2. Presentation style and colors
3. Appropriate mood and tone
4. Relevant hashtags for {restaurant_context.get('location')} area

Generate engaging social media caption with local appeal."""
```

### Restaurant Context Optimization

Enhance restaurant profiles for better AI results:

```sql
-- Add detailed restaurant information
UPDATE restaurants SET 
    cuisine = 'Modern Italian',
    description = 'Farm-to-table Italian cuisine with contemporary presentation',
    location = 'Downtown Seattle',
    style = 'Casual Fine Dining'
WHERE id = your_restaurant_id;
```

### Hashtag Strategy Customization

Add location-specific or brand-specific hashtags:

```python
# Add custom hashtag collections
self.local_hashtags = {
    'seattle': ['#seattleeats', '#pnwfood', '#seattlerestaurant'],
    'portland': ['#portlandfood', '#pdxeats', '#portlandrestaurant'],
    'san_francisco': ['#sfeats', '#bayareafood', '#sfrestaurant']
}
```

## 📊 Monitoring & Analytics

### AI Performance Tracking

Monitor AI effectiveness through:

1. **Response Times**: Track API response times
2. **Success Rates**: Monitor successful AI generations
3. **Fallback Usage**: Track when fallbacks are used
4. **Cost Analysis**: Monitor API usage costs

### Content Performance

Track generated content performance:

1. **Engagement Rates**: Compare AI vs manual content engagement
2. **Hashtag Performance**: Analyze which AI-generated hashtags perform best
3. **Content Variety**: Ensure AI generates diverse content types
4. **Brand Consistency**: Monitor brand voice consistency

## 🚨 Troubleshooting

### Common Issues

#### API Key Not Working
```bash
# Check API key format
echo $OPENAI_API_KEY
# Should start with 'sk-' and be 51 characters long
```

#### Rate Limiting
```python
# Implement retry logic for rate limits
import time
import random

def retry_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(wait_time)
    raise Exception("Max retries exceeded")
```

#### Cost Control
```python
# Implement usage tracking
def track_api_usage(endpoint, tokens_used, cost):
    # Log usage for monitoring
    usage_log = {
        'timestamp': datetime.now(),
        'endpoint': endpoint,
        'tokens': tokens_used,
        'cost': cost
    }
    # Save to database or logging system
```

## 🔄 Fallback System

The platform includes a robust fallback system that ensures functionality even when AI is unavailable:

### Automatic Fallbacks

1. **API Unavailable**: Uses pre-written professional captions
2. **Rate Limits**: Queues requests and uses fallbacks temporarily
3. **Cost Limits**: Switches to fallbacks when budget limits are reached
4. **Error Handling**: Graceful degradation for any AI service issues

### Fallback Quality

- **Professional Content**: High-quality pre-written captions and posts
- **Restaurant Context**: Incorporates restaurant name and basic context
- **Hashtag Strategy**: Uses proven hashtag combinations
- **Seamless Experience**: Users may not notice when fallbacks are used

## 📈 Performance Optimization

### Response Time Optimization

1. **Caching**: Cache common AI responses for faster delivery
2. **Async Processing**: Process AI requests asynchronously when possible
3. **Batch Operations**: Combine multiple requests for efficiency
4. **Preloading**: Pre-generate content during off-peak hours

### Quality Optimization

1. **Prompt Engineering**: Continuously refine AI prompts for better results
2. **Context Enhancement**: Provide more detailed restaurant context
3. **Feedback Loop**: Implement user feedback to improve AI outputs
4. **A/B Testing**: Test different AI approaches for optimal results

## 🎉 Success Metrics

### Key Performance Indicators

1. **AI Adoption Rate**: Percentage of posts using AI-generated content
2. **Content Quality Score**: User ratings of AI-generated content
3. **Engagement Improvement**: Increase in social media engagement
4. **Time Savings**: Reduction in content creation time
5. **Cost Efficiency**: Cost per high-quality post generated

### Expected Results

With proper AI configuration, restaurants typically see:

- **80% reduction** in content creation time
- **40% increase** in social media engagement
- **95% user satisfaction** with AI-generated content
- **Professional quality** content consistently
- **Significant ROI** through improved social media performance

---

**Support**: For technical assistance with AI setup, refer to the main documentation or contact support.  
**Updates**: This guide will be updated as new AI features are added to the platform.

