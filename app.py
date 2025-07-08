import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime, timedelta

# Language translations
TRANSLATIONS = {
    'English': {
        'app_title': 'EduScan Somalia',
        'app_subtitle': 'Professional Learning Risk Assessment System',
        'dashboard': 'Dashboard',
        'settings': 'Settings',
        'system_overview': 'System Overview',
        'total_students': 'Total Students',
        'on_track': 'On Track',
        'at_risk': 'At Risk',
        'intervention': 'Intervention Required',
        'academic_performance_by_subject': 'Academic Performance by Subject',
        'student_risk_distribution': 'Student Risk Distribution',
        'recent_assessment_results': 'Recent Assessment Results',
        'student_name': 'Student Name',
        'grade': 'Grade',
        'math_score': 'Math Score',
        'reading_score': 'Reading Score',
        'science_score': 'Science Score',
        'risk_level': 'Risk Level',
        'assessment_date': 'Assessment Date',
        'language': 'Language',
        'theme': 'Theme',
        'offline_mode': 'Offline Mode',
        'save_settings': 'Save Settings',
        'reset_app': 'Reset Application',
        'subjects': 'Subjects',
        'average_score': 'Average Score',
        'student_risk_overview': 'Student Risk Overview',
        'average_subject_scores': 'Average Subject Scores',
        'analytics': 'Analytics'
    },
    'Somali': {
        'app_title': 'EduScan Somalia',
        'app_subtitle': 'Nidaamka Qiimaynta Khatarta Barashada ee Xirfadda leh',
        'dashboard': 'Shabakada',
        'settings': 'Dejinta',
        'system_overview': 'Guud ahaan Nidaamka',
        'total_students': 'Wadarta Ardayda',
        'on_track': 'Jidka Saxda ah',
        'at_risk': 'Halis ku jira',
        'intervention': 'Waxaa loo baahan yahay faragelin',
        'academic_performance_by_subject': 'Waxqabadka Waxbarasho ee Maaddada',
        'student_risk_distribution': 'Qaybinta Halista Ardayda',
        'recent_assessment_results': 'Natiijooyinka Qiimaynta ee dhawaan',
        'student_name': 'Magaca Ardayga',
        'grade': 'Fasalka',
        'math_score': 'Dhibcaha Xisaabta',
        'reading_score': 'Dhibcaha Akhriska',
        'science_score': 'Dhibcaha Sayniska',
        'risk_level': 'Heerka Halista',
        'assessment_date': 'Taariikhda Qiimaynta',
        'language': 'Luuqada',
        'theme': 'Qaabka',
        'offline_mode': 'Qaabka aan internetka lahayn',
        'save_settings': 'Kaydi Dejinta',
        'reset_app': 'Dib u deji Codsiga',
        'subjects': 'Maaddooyinka',
        'average_score': 'Celceliska Dhibcaha',
        'student_risk_overview': 'Guud ahaan Halista Ardayda',
        'average_subject_scores': 'Celceliska Dhibcaha Maaddada',
        'analytics': 'Falanqaynta'
    },
    'Arabic': {
        'app_title': 'EduScan Somalia',
        'app_subtitle': 'نظام تقييم مخاطر التعلم المهني',
        'dashboard': 'لوحة التحكم',
        'settings': 'الإعدادات',
        'system_overview': 'نظرة عامة على النظام',
        'total_students': 'إجمالي الطلاب',
        'on_track': 'على المسار الصحيح',
        'at_risk': 'في خطر',
        'intervention': 'يتطلب تدخلاً',
        'academic_performance_by_subject': 'الأداء الأكاديمي حسب المادة',
        'student_risk_distribution': 'توزيع مخاطر الطلاب',
        'recent_assessment_results': 'نتائج التقييم الأخيرة',
        'student_name': 'اسم الطالب',
        'grade': 'الصف',
        'math_score': 'درجة الرياضيات',
        'reading_score': 'درجة القراءة',
        'science_score': 'درجة العلوم',
        'risk_level': 'مستوى الخطر',
        'assessment_date': 'تاريخ التقييم',
        'language': 'اللغة',
        'theme': 'المظهر',
        'offline_mode': 'الوضع غير المتصل',
        'save_settings': 'حفظ الإعدادات',
        'reset_app': 'إعادة تعيين التطبيق',
        'subjects': 'المواد',
        'average_score': 'متوسط الدرجة',
        'student_risk_overview': 'نظرة عامة على مخاطر الطلاب',
        'average_subject_scores': 'متوسط درجات المواد',
        'analytics': 'التحليلات'
    }
}

def get_text(key, language=None):
    """Get localized text based on language setting"""
    if language is None:
        language = st.session_state.get('app_language', 'English')
    return TRANSLATIONS.get(language, TRANSLATIONS['English']).get(key, key)

def get_recommendations(risk_level):
    """Get recommendations based on risk level"""
    recommendations = {
        'Low': [
            "Continue current learning approach",
            "Provide enrichment activities",
            "Monitor progress regularly",
            "Encourage independent learning",
            "Maintain engagement"
        ],
        'Medium': [
            "Additional support recommended",
            "Small group instruction",
            "Regular progress monitoring",
            "Parent-teacher collaboration",
            "Targeted skill building",
            "Use visual learning aids"
        ],
        'High': [
            "Immediate intervention required",
            "One-on-one tutoring recommended", 
            "Consult with learning specialist",
            "Implement individualized learning plan",
            "Regular progress monitoring",
            "Family support engagement"
        ]
    }
    return recommendations.get(risk_level, [])

def load_app_settings():
    """Load application settings from file"""
    settings_file = 'data/app_settings.json'
    default_settings = {
        'language': 'English',
        'theme': 'Modern',
        'offline_mode': False
    }
    
    try:
        if os.path.exists(settings_file):
            with open(settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                # Validate theme setting
                valid_themes = ['Modern', 'Classic', 'Dark']
                if settings.get('theme') not in valid_themes:
                    settings['theme'] = 'Modern'
                return settings
    except:
        pass
    
    return default_settings

def save_app_settings(settings):
    """Save application settings to file"""
    settings_file = 'data/app_settings.json'
    os.makedirs('data', exist_ok=True)
    
    try:
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False

def apply_theme(theme):
    """Apply the selected theme to the application"""
    if theme == 'Modern':
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #ff7b00 0%, #ff5722 25%, #ff9800 50%, #ffab00 75%, #ffc107 100%);
            background-attachment: fixed;
            background-size: cover;
            background-repeat: no-repeat;
            font-family: 'Poppins', sans-serif;
            min-height: 100vh;
        }
        
        .main-header {
            background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        
        .main-header h1 {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: #000000;
            text-shadow: 2px 2px 4px rgba(255,255,255,0.3);
        }
        
        .main-header p {
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 0;
        }
        
        .nav-button {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 15px;
            padding: 1rem 2rem;
            margin: 0.5rem;
            color: white;
            text-decoration: none;
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            display: inline-block;
            min-width: 150px;
            text-align: center;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .nav-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.2);
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        }
        
        .nav-button.active {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            color: white;
            transform: translateY(-2px);
        }
        
        /* Force all Streamlit buttons to be blue */
        div[data-testid="stButton"] > button {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        
        div[data-testid="stButton"] > button:hover {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
        }
        
        .metric-card {
            background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            color: white;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.2);
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: #2c3e50;
        }
        
        .metric-title {
            font-size: 1.1rem;
            opacity: 0.9;
            margin-bottom: 0.5rem;
        }
        
        .metric-desc {
            font-size: 0.9rem;
            opacity: 0.7;
        }
        
        .content-card {
            background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.9) 100%);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.3);
            border-radius: 20px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            color: #2c3e50;
        }
        
        .stSelectbox > div > div {
            background-color: rgba(255,255,255,0.9) !important;
            border-radius: 10px !important;
        }
        
        .stTextInput > div > div > input {
            background-color: rgba(255,255,255,0.9) !important;
            border-radius: 10px !important;
        }
        
        .stNumberInput > div > div > input {
            background-color: rgba(255,255,255,0.9) !important;
            border-radius: 10px !important;
        }
        </style>
        """, unsafe_allow_html=True)

def check_offline_mode():
    """Check if application can work offline"""
    settings = load_app_settings()
    return settings.get('offline_mode', False)

def render_app_header():
    """Render professional desktop application header"""
    language = st.session_state.get('app_language', 'English')
    
    st.markdown(f"""
    <div class="main-header">
        <h1>{get_text('app_title', language)}</h1>
        <p>{get_text('app_subtitle', language)}</p>
    </div>
    """, unsafe_allow_html=True)

def get_dashboard_icon():
    """Get dashboard icon"""
    return "🏠"

def get_settings_icon():
    """Get settings icon"""
    return "⚙️"

def render_navigation(language=None):
    """Render desktop-style navigation tabs"""
    if language is None:
        language = st.session_state.get('app_language', 'English')
    
    # Initialize current page in session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'dashboard'
    
    # Simplified navigation - only Dashboard and Settings
    col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 2])
    
    nav_options = [
        ('dashboard', get_dashboard_icon(), get_text('dashboard', language)),
        ('settings', get_settings_icon(), get_text('settings', language))
    ]
    
    # Center the navigation buttons
    with col2:
        if st.button(get_text('dashboard', language), key="nav_dashboard", type="primary"):
            st.session_state.current_page = 'dashboard'
            st.rerun()
    
    with col5:
        if st.button(get_text('settings', language), key="nav_settings", type="primary"):
            st.session_state.current_page = 'settings'
            st.rerun()

def create_metric_card(title, value, description, color="#3b82f6"):
    """Create a professional metric card"""
    return f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value" style="color: {color};">{value}</div>
        <div class="metric-desc">{description}</div>
    </div>
    """

def render_dashboard():
    """Render the main dashboard"""
    # Get language from session state first, then settings
    language = st.session_state.get('app_language')
    if language is None:
        settings = load_app_settings()
        language = settings.get('language', 'English')
        st.session_state['app_language'] = language
    
    st.markdown(f"""
    <div class="content-card">
        <h2 style="margin-top: 0; color: #1e293b; text-align: center;">{get_text('system_overview', language)}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label=get_text('total_students', language),
            value="342",
            delta="12 new this month"
        )
    
    with col2:
        st.metric(
            label=get_text('on_track', language), 
            value="267",
            delta="78% performing well"
        )
    
    with col3:
        st.metric(
            label=get_text('at_risk', language),
            value="52", 
            delta="15% need support"
        )
    
    with col4:
        st.metric(
            label=get_text('intervention', language),
            value="23",
            delta="7% urgent attention"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Performance Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"📊 {get_text('academic_performance_by_subject', language)}")
        # Create subject performance chart
        subjects = ['Mathematics', 'Reading', 'Writing', 'Science', 'Social Studies']
        scores = [78, 82, 75, 80, 77]
        
        fig = px.bar(
            x=subjects, 
            y=scores,
            title=get_text('average_subject_scores', language),
            color=scores,
            color_continuous_scale='Blues'
        )
        fig.update_layout(
            xaxis_title=get_text('subjects', language),
            yaxis_title=get_text('average_score', language),
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader(f"📈 {get_text('student_risk_distribution', language)}")
        # Create risk level pie chart
        risk_labels = [get_text('on_track', language), get_text('at_risk', language), get_text('intervention', language)]
        risk_values = [267, 52, 23]
        risk_colors = ['#10b981', '#f8f9fa', '#ef4444']
        
        fig = go.Figure(data=[go.Pie(
            labels=risk_labels, 
            values=risk_values,
            hole=0.4,
            marker_colors=risk_colors,
            marker_line=dict(color='#000000', width=2)
        )])
        fig.update_layout(
            title=get_text('student_risk_overview', language),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent Assessment Data
    st.subheader(f"📋 {get_text('recent_assessment_results', language)}")
    
    # Create sample assessment data with translated headers
    assessment_data = pd.DataFrame({
        get_text('student_name', language): ['Ahmed Hassan', 'Fatima Ali', 'Omar Mohamed', 'Sahra Abdi', 'Yusuf Ibrahim'],
        get_text('grade', language): ['Grade 6', 'Grade 5', 'Grade 7', 'Grade 6', 'Grade 5'],
        get_text('math_score', language): [85, 92, 78, 88, 75],
        get_text('reading_score', language): [78, 89, 82, 91, 73],
        get_text('science_score', language): [82, 94, 76, 89, 78],
        get_text('risk_level', language): ['Low', 'Low', 'Medium', 'Low', 'Medium'],
        get_text('assessment_date', language): ['2024-06-15', '2024-06-14', '2024-06-13', '2024-06-12', '2024-06-11']
    })
    
    st.dataframe(assessment_data, use_container_width=True)

def render_settings():
    """Render the settings page"""
    # Get language from session state first, then settings
    language = st.session_state.get('app_language')
    if language is None:
        settings = load_app_settings()
        language = settings.get('language', 'English')
        st.session_state['app_language'] = language
    else:
        settings = load_app_settings()
    
    # Add CSS to fix text color for selectboxes
    st.markdown("""
    <style>
    /* Fix selectbox text color */
    .stSelectbox > div > div > div {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Fix selectbox dropdown text */
    .stSelectbox > div > div > div > div {
        color: #000000 !important;
    }
    
    /* Fix selectbox options */
    [data-baseweb="select"] > div {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Fix all text in settings to be black */
    .stMarkdown h3 {
        color: #000000 !important;
    }
    
    /* Fix checkbox text */
    .stCheckbox > label {
        color: #000000 !important;
    }
    
    /* Fix all text labels */
    .stSelectbox label {
        color: #000000 !important;
    }
    
    /* Make sure preview text is visible */
    .stMarkdown p {
        color: #000000 !important;
    }
    
    /* Style navigation buttons to be blue */
    div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="stButton"] > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Style primary buttons specifically */
    button[kind="primary"] {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
    }
    
    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="main-header">
        <h1 class="page-title">{get_text('settings', language)}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Settings form
    with st.form("settings_form"):
        st.markdown(f"### {get_text('language', language)}")
        new_language = st.selectbox(
            get_text('language', language),
            ['English', 'Somali', 'Arabic'],
            index=['English', 'Somali', 'Arabic'].index(language),
            label_visibility="collapsed"
        )
        
        st.markdown(f"### {get_text('theme', language)}")
        new_theme = st.selectbox(
            get_text('theme', language),
            ['Modern', 'Classic', 'Dark'],
            index=['Modern', 'Classic', 'Dark'].index(settings.get('theme', 'Modern')),
            label_visibility="collapsed"
        )
        
        st.markdown(f"### {get_text('offline_mode', language)}")
        offline_mode = st.checkbox(
            get_text('offline_mode', language),
            value=settings.get('offline_mode', False)
        )
        
        # Show current settings preview
        with st.expander("Current Settings Preview", expanded=False):
            st.markdown(f"**Language:** {new_language}")
            st.markdown(f"**Theme:** {new_theme}")
            st.markdown(f"**Offline Mode:** {'Enabled' if settings.get('offline_mode', False) else 'Disabled'}", unsafe_allow_html=True)
            
            # Language preview text
            if new_language == 'Somali':
                st.info("Luqadda: Af-Soomaali - Barnaamijkan wuxuu u shaqeeyaa barashada ardayda")
            elif new_language == 'Arabic':
                st.info("اللغة: العربية - هذا التطبيق يعمل على تقييم تعلم الطلاب")
            else:
                st.info("Language: English - This application works for student learning assessment")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(get_text('save_settings', language), type="primary"):
            new_settings = {
                'language': new_language,
                'theme': new_theme,
                'offline_mode': offline_mode
            }
            
            if save_app_settings(new_settings):
                # Update session state to immediately apply language change
                st.session_state['app_language'] = new_language
                st.success("Settings saved successfully!")
                st.rerun()
            else:
                st.error("Failed to save settings.")
    
    with col2:
        if st.button(get_text('reset_app', language), type="secondary"):
            # Reset session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            
            # Reset to default settings
            default_settings = {
                'language': 'English',
                'theme': 'Modern', 
                'offline_mode': False
            }
            save_app_settings(default_settings)
            
            st.success("Application reset successfully!")
            st.rerun()

def render_bottom_navigation():
    """Render bottom navigation with offline toggle and reset"""
    settings = load_app_settings()
    offline_mode = settings.get('offline_mode', False)
    
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**EduScan Somalia** | Professional Learning Assessment")
    
    with col2:
        status = "🟢 Online" if not offline_mode else "🟡 Offline"
        st.markdown(f"Status: {status}")
    
    with col3:
        if st.button("Toggle Offline Mode", type="primary"):
            new_settings = settings.copy()
            new_settings['offline_mode'] = not offline_mode
            save_app_settings(new_settings)
            st.rerun()

def main():
    """Main application function"""
    # Page configuration
    st.set_page_config(
        page_title="EduScan Somalia",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize language in session state
    if 'app_language' not in st.session_state:
        settings = load_app_settings()
        st.session_state['app_language'] = settings.get('language', 'English')
    
    # Load settings and apply theme
    settings = load_app_settings()
    apply_theme(settings.get('theme', 'Modern'))
    
    # Clean background without image
    st.markdown("""
    <style>
    .stApp {
        background: #f8fafc !important;
        min-height: 100vh !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Render header
    render_app_header()
    
    # Render navigation
    render_navigation()
    
    # Get current language
    language = st.session_state.get('app_language', 'English')
    
    # Render current page content
    current_page = st.session_state.get('current_page', 'dashboard')
    
    if current_page == 'dashboard':
        render_dashboard()
    elif current_page == 'settings':
        render_settings()
    
    # Render bottom navigation
    render_bottom_navigation()

if __name__ == "__main__":
    main()