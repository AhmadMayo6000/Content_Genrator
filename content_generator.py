import streamlit as st
import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

st.set_page_config(
    page_title="AI Content Generator",
    page_icon="✍️",
    layout="centered"
)

st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 0rem;}
    .header {
        background: linear-gradient(135deg, #6c3483, #1a5276);
        padding: 28px 24px;
        border-radius: 0 0 24px 24px;
        margin-bottom: 24px;
        text-align: center;
        color: white;
    }
    .header h1 {font-size: 26px; font-weight: 700; margin: 0;}
    .header p {font-size: 13px; margin: 6px 0 0; opacity: 0.8;}
    .content-box {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
        position: relative;
    }
    .platform-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .instagram {background: #fce4ec; color: #c2185b;}
    .facebook {background: #e3f2fd; color: #1565c0;}
    .twitter {background: #e0f7fa; color: #00695c;}
    .linkedin {background: #e8eaf6; color: #283593;}
    .copy-tip {font-size: 11px; color: #aaa; margin-top: 8px;}
</style>

<div class="header">
    <div style="font-size:36px; margin-bottom:8px;">✍️</div>
    <h1>AI Content Generator</h1>
    <p>Generate professional content for all platforms in seconds</p>
</div>
""", unsafe_allow_html=True)

# Content type selector
content_type = st.selectbox(
    "What do you want to create?",
    [
        "📱 Social Media Posts (All Platforms)",
        "📧 Email Campaign",
        "📝 Blog Article",
        "🛍️ Product Description",
        "📢 Advertisement Copy",
        "🎯 WhatsApp Marketing Message",
    ]
)

# Input form
col1, col2 = st.columns(2)
with col1:
    business_name = st.text_input("Business Name", placeholder="e.g. Pizza Palace")
    industry = st.text_input("Industry / Type", placeholder="e.g. Restaurant, Clinic, Clothing")
with col2:
    topic = st.text_input("Topic / Product", placeholder="e.g. New BBQ Pizza, Eid Sale, Free Checkup")
    tone = st.selectbox("Tone", ["Professional", "Friendly & Casual", "Exciting & Energetic", "Luxurious", "Funny"])

target_audience = st.text_input(
    "Target Audience",
    placeholder="e.g. Young families in Lahore, Working professionals, Students"
)

language = st.selectbox("Language", ["English", "Urdu", "Both English and Urdu"])

extra_info = st.text_area(
    "Extra details (optional)",
    placeholder="e.g. 30% discount this weekend, Free delivery above Rs.1500, Limited time offer",
    height=80
)

st.divider()

if st.button("🚀 Generate Content", type="primary", use_container_width=True):
    if not business_name or not topic:
        st.error("Please enter Business Name and Topic!")
    else:
        # Build prompt based on content type
        if "Social Media" in content_type:
            prompt = f"""Create social media content for:
Business: {business_name}
Industry: {industry}
Topic: {topic}
Tone: {tone}
Target Audience: {target_audience}
Language: {language}
Extra Info: {extra_info}

Generate ALL of the following:

1. INSTAGRAM POST:
- Caption (engaging, with emojis)
- 15 relevant hashtags

2. FACEBOOK POST:
- Longer caption with more detail
- Call to action

3. TWITTER/X POST:
- Short punchy tweet under 280 characters

4. LINKEDIN POST:
- Professional version

Make each one unique and platform-appropriate.
"""
        elif "Email" in content_type:
            prompt = f"""Write a professional email campaign for:
Business: {business_name}
Industry: {industry}
Topic: {topic}
Tone: {tone}
Target Audience: {target_audience}
Language: {language}
Extra Info: {extra_info}

Include:
1. Subject line (5 options)
2. Email body (professional, persuasive)
3. Call to action
"""
        elif "Blog" in content_type:
            prompt = f"""Write a complete blog article for:
Business: {business_name}
Industry: {industry}
Topic: {topic}
Tone: {tone}
Target Audience: {target_audience}
Language: {language}
Extra Info: {extra_info}

Include:
1. SEO title
2. Introduction
3. 4-5 main sections with subheadings
4. Conclusion with call to action
5. 10 SEO keywords
"""
        elif "Product" in content_type:
            prompt = f"""Write compelling product descriptions for:
Business: {business_name}
Product: {topic}
Industry: {industry}
Tone: {tone}
Target Audience: {target_audience}
Language: {language}
Extra Info: {extra_info}

Include:
1. Short description (50 words)
2. Long description (150 words)
3. 5 key features/benefits (bullet points)
4. Call to action
"""
        elif "Advertisement" in content_type:
            prompt = f"""Write advertisement copy for:
Business: {business_name}
Industry: {industry}
Topic: {topic}
Tone: {tone}
Target Audience: {target_audience}
Language: {language}
Extra Info: {extra_info}

Include:
1. Google Ad (headline + description)
2. Facebook Ad copy
3. Billboard/Banner text (10 words max)
4. Radio/Audio script (30 seconds)
"""
        else:  # WhatsApp
            prompt = f"""Write WhatsApp marketing messages for:
Business: {business_name}
Industry: {industry}
Topic: {topic}
Tone: {tone}
Target Audience: {target_audience}
Language: {language}
Extra Info: {extra_info}

Write 5 different WhatsApp messages:
1. Promotional message
2. Follow-up message
3. Urgency/Limited time message
4. Friendly reminder
5. Thank you + offer message

Keep each under 200 words. Use emojis appropriately.
"""

        with st.spinner("✍️ Generating your content..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are an expert marketing copywriter and content creator. Create engaging, professional content that converts. Always follow the exact format requested."},
                    {"role": "user", "content": prompt}
                ]
            )
            result = response.choices[0].message.content

        st.success("✅ Content generated!")
        
        # Display result
        st.markdown("### Your Generated Content")
        st.markdown(result)
        
        # Download button
        st.download_button(
            label="⬇️ Download as Text File",
            data=result,
            file_name=f"{business_name}_{topic}_content.txt",
            mime="text/plain",
            use_container_width=True
        )

        # Regenerate
        if st.button("🔄 Generate Different Version", use_container_width=True):
            st.rerun()

# Footer
st.markdown("""
<div style='text-align:center; color:#aaa; font-size:12px; margin-top:30px;'>
    AI Content Generator • Powered by Groq AI • Generate unlimited content
</div>
""", unsafe_allow_html=True)
