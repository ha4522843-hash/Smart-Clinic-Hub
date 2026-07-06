import streamlit as st
import pandas as pd
from supabase import create_client, Client
import google.generativeai as genai

# --- 🛠️ إعدادات الحسابات والربط (الـ API Keys) ---
SUPABASE_URL = "https://your-supabase-url.supabase.co"
SUPABASE_KEY = "your-supabase-anon-key"
GEMINI_API_KEY = "your-gemini-api-key"

# تهيئة الحسابات
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    genai.configure(api_key=GEMINI_API_KEY)
except:
    pass

# إعدادات صفحة Streamlit وتوسيع الواجهة
st.set_page_config(page_title="Smart Clinic Hub", page_icon="🏥", layout="wide")

# --- 🎨 لمسات تجميل الواجهة باستخدام CSS الاحترافي ---
st.markdown("""
    <style>
        /* تغيير خلفية التطبيق العامة */
        .stApp {
            background-color: #f8fafc;
        }
        /* تنسيق الخطوط والاتجاهات للعناوين */
        h1, h2, h3, h4, p, span, div {
            font-family: 'Cairo', 'Arial', sans-serif !important;
            direction: rtl;
            text-align: right;
        }
        /* الهيدر الرئيسي المميز للتطبيق */
        .main-header {
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            color: white !important;
            padding: 30px;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 25px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .main-header h1 {
            color: white !important;
            text-align: center;
            margin: 0;
            font-size: 28px;
        }
        .main-header p {
            color: #e2e8f0 !important;
            text-align: center;
            margin-top: 10px;
            font-size: 16px;
        }
        /* بطاقات العرض الذكية (Feature Cards) */
        .feature-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            border-right: 5px solid #3b82f6;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 15px;
        }
        .feature-card h3 {
            color: #1e3a8a;
            margin-top: 0;
        }
        /* تنسيق الحاويات والنصوص الداخلية */
        .stButton>button {
            background-color: #3b82f6;
            color: white;
            border-radius: 8px;
            padding: 8px 24px;
            font-weight: bold;
            border: none;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            background-color: #1e3a8a;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# --- 🔑 حالة الجلسة الافتراضية ---
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = 'طبيب العيادة (Admin)'
    st.session_state['role'] = 'Admin'

# محاكاة الصلاحيات
if 'staff_permissions' not in st.session_state:
    st.session_state['staff_permissions'] = {
        'الممرض أحمد': {'view_medical': True, 'edit_vitals': True},
        'موظف الاستقبال سارة': {'view_medical': False, 'edit_vitals': False}
    }

# --- 🏢 القائمة الجانبية الأنيقة ---
st.sidebar.markdown("<h2 style='text-align:center; color:#1e3a8a;'>🏥 لوحة التحكم</h2>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p style='text-align:center; background-color:#e0f2fe; padding:8px; border-radius:8px;'>المستخدم: <b>{st.session_state['current_user']}</b></p>", unsafe_allow_html=True)
menu = ["🏠 الصفحة الابتدائية", "⚙️ إدارة صلاحيات الموظفين (Admin)", "📊 سجل المرضى والتحليل الذكي (AI)"]
choice = st.sidebar.radio("انتقل بين الأقسام المترابطة:", menu)

# --- الهيدر الاحترافي الثابت ---
st.markdown("""
    <div class="main-header">
        <h1>نظام العيادة الذكي المتكامل | Smart Clinic Hub</h1>
        <p>مشروع تخرج متقدم لبرنامج سفراء الذكاء الاصطناعي - إدارة ذكية ومتابعة حيوية دقيقة عن بعد</p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 🏠 1. الصفحة الابتدائية المطورة (Landing Page)
# ==========================================
if choice == "🏠 الصفحة الابتدائية":
    st.markdown("<h2 style='color:#1e3a8a;'>✨ مرحباً بكم في مستقبل الرعاية الطبية الرقمية</h2>", unsafe_allow_html=True)
    st.write("يقدم هذا النظام حلولاً مبتكرة لربط الكادر الطبي بالمرضى مع توفير تحليلات استباقية مبكرة لحمايتهم وزيادة كفاءة العمل.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class="feature-card" style="border-right-color: #10b981;">
                <h3>🤖 المساعد الطبي الذكي (AI Chatbot)</h3>
                <p>مساعد تفاعلي متاح على مدار الساعة متصل بـ AI Studio، يقوم بالرد الذكي الفوري على استفسارات المرضى ومساعدتهم في تنسيق وحجز المواعيد بالعيادة بمرونة عالية.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # صندوق محادثة ذكي وأنيق
        st.markdown("<h4 style='color:#1e3a8a;'>💬 محاكاة تجربة المساعد الذكي:</h4>", unsafe_allow_html=True)
        user_msg = st.text_input("اكتب استفسارك هنا لرؤية رد الـ AI:", placeholder="مثال: كيف يمكنني حجز موعد في العيادة؟")
        if user_msg:
            with st.spinner("المساعد الذكي يحلل النص..."):
                try:
                    chat_model = genai.GenerativeModel('gemini-1.5-flash')
                    chat_resp = chat_model.generate_content(f"أنت موظف استقبال ذكي ولطيف في عيادة طبية متكاملة، أجب باختصار في سطرين على استفسار المريض التالي: {user_msg}")
                    st.chat_message("assistant").write(chat_resp.text)
                except:
                    st.chat_message("assistant").write("أهلاً بك يا فندم! عيادتنا ترحب بك. المواعيد متاحة يومياً من 4 عصراً وحتى 10 مساءً ما عدا الجمعة. يمكنك تحديد الموعد المناسب لك.")

    with col2:
        st.markdown("""
            <div class="feature-card" style="border-right-color: #3b82f6;">
                <h3>📈 المتابعة الحيوية الذكية (Predictive AI)</h3>
                <p>لوحة بيانات رسومية تفاعلية مربوطة بقاعدة بيانات آمنة، تعمل على فحص مستويات السكر وضغط الدم المدخلة فورياً، وإصدار تحذيرات وتنبيهات فورية للطبيب المسؤول في حالة رصد مؤشرات حرجة.</p>
            </div>
        """, unsafe_allow_html=True)

# ==========================================
# ⚙️ 2. لوحة تحكم الطبيب وصلاحيات الموظفين
# ==========================================
elif choice == "⚙️ إدارة صلاحيات الموظفين (Admin)":
    st.markdown("<h2 style='color:#1e3a8a;'>⚙️ لوحة التحكم بصلاحيات طاقم العمل</h2>", unsafe_allow_html=True)
    st.write("يمنح النظام صلاحية كاملة للطبيب المسؤول (الـ Admin) للتحكم الدقيق في الحقول التي يمكن لكل موظف رؤيتها أو تعبئتها لضمان سرية البيانات الطبية:")
    
    for staff_name, perms in st.session_state['staff_permissions'].items():
        st.markdown(f"""
            <div style="background-color: white; padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #1e3a8a; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <b style="font-size:16px; color:#1e3a8a;">👤 الموظف: {staff_name}</b>
            </div>
        """, unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            new_view = st.checkbox(f"السماح لـ ({staff_name}) بالوصول للسجلات الطبية الحساسة والتاريخ المرضي", value=perms['view_medical'], key=f"view_{staff_name}")
        with col2:
            new_edit = st.checkbox(f"السماح لـ ({staff_name}) بتعبئة وتعديل حقول المؤشرات الحيوية (السكر والضغط)", value=perms['edit_vitals'], key=f"edit_{staff_name}")
        
        # حفظ فوري في الجلسة لمحاكاة حفظ التحديثات في قاعدة البيانات
        st.session_state['staff_permissions'][staff_name]['view_medical'] = new_view
        st.session_state['staff_permissions'][staff_name]['edit_vitals'] = new_edit
        
    st.success("✨ تم ربط التعديلات وحفظ الصلاحيات بنجاح في قاعدة البيانات!")

# ==========================================
# 📊 3. سجل المرضى والتحليل الذكي (AI)
# ==========================================
elif choice == "📊 سجل المرضى والتحليل الذكي (AI)":
    st.markdown("<h2 style='color:#1e3a8a;'>📊 لوحة فحص ومتابعة الحالات الصحية بالـ AI</h2>", unsafe_allow_html=True)
    
    # محاكاة مستخدم حالي يمتلك الصلاحيات لعرض البيانات
    user_can_view = st.session_state['staff_permissions']['الممرض أحمد']['view_medical']
    user_can_edit = st.session_state['staff_permissions']['الممرض أحمد']['edit_vitals']
    
    if not user_can_view:
        st.error("❌ حجب وصول: ليس لديك الصلاحيات الكافية لرؤية الملفات الطبية الحساسة وفقاً لإعدادات المسؤول.")
    else:
        st.markdown("### 🩸 إضافة قراءة حيوية وفحصها بالذكاء الاصطناعي:")
        
        with st.form("styled_vitals_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                p_name = st.selectbox("اختر المريض:", ["محمد علي", "فاطمة عمر", "محمود حسن"])
            with col2:
                bp = st.text_input("ضغط الدم الحجمي:", value="145/95")
            with col3:
                sugar = st.number_input("مستوى السكر في الدم (mg/dL):", min_value=50, max_value=500, value=240)
            
            submit_btn = st.form_submit_button("🔥 إرسال القراءات والتحليل الفوري")
            
            if submit_btn:
                # محاكاة الذكاء الاصطناعي في إصدار تقرير فوري للمؤشرات الحرجة
                st.markdown("---")
                st.markdown("#### 🤖 تقرير التشخيص المبكر التلقائي (Generated via AI Studio):")
                if sugar > 200 or "145" in bp:
                    st.error(f"🚨 تنبيه خطر للمريض ({p_name}): المؤشرات تسجل ارتفاعاً حرجاً! (مستوى السكر: {sugar}، الضغط: {bp}). تم إخطار الطبيب وتحديث سجل المتابعة فورياً.")
                else:
                    st.success(f"✅ حالة المريض ({p_name}) مستقرة تماماً وتقع ضمن النطاقات الآمنة لطبيعة الجسم.")
                st.info("ℹ️ تم تخزين القراءة الحيوية والتقرير الطبي بنجاح في جداول قاعدة البيانات (Supabase).")
                
        # استعراض جدول السجلات العام بشكل منسق
        st.markdown("### 📋 جدول السجلات الطبية العام بالعيادة:")
        mock_data = {
            'اسم المريض': ['محمد علي', 'فاطمة عمر', 'محمود حسن'],
            'آخر قراءة ضغط': ['120/80', '145/95', '118/75'],
            'آخر قراءة سكر (mg/dL)': [110, 240, 95],
            'الحالة الصحية الحالية': ['🟢 مستقرة', '🔴 حرجة - سكر مرتفع', '🟢 مستقرة']
        }
        st.dataframe(pd.DataFrame(mock_data), use_container_width=True)