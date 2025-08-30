"""
UI Components for the enhanced chatbot application.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any
import pandas as pd
from datetime import datetime, timedelta

class UIComponents:
    def __init__(self):
        self.primary_color = "#1f77b4"
        self.secondary_color = "#ff7f0e"
        self.accent_color = "#2ca02c"
        
    def load_custom_css(self):
        """Load custom CSS styles."""
        css_path = "static/css/styles.css"
        try:
            with open(css_path, 'r') as f:
                css = f.read()
            st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
        except FileNotFoundError:
            # Fallback inline CSS
            st.markdown("""
            <style>
            .main-header {
                background: linear-gradient(135deg, #1f77b4, #ff7f0e);
                color: white;
                padding: 2rem;
                border-radius: 10px;
                margin-bottom: 2rem;
                text-align: center;
            }
            .stat-card {
                background: white;
                padding: 1.5rem;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                text-align: center;
                border-left: 4px solid #1f77b4;
            }
            .contact-card {
                background: #f8f9fa;
                padding: 1rem;
                border-radius: 8px;
                margin-bottom: 0.5rem;
                border-left: 3px solid #2ca02c;
            }
            </style>
            """, unsafe_allow_html=True)
    
    def render_header(self, name: str, title: str, avatar: str = "👨‍💻"):
        """Render the application header."""
        st.markdown(f"""
        <div class="main-header">
            <div style="font-size: 3em; margin-bottom: 0.5rem;">{avatar}</div>
            <h1 style="margin: 0; font-size: 2.5em;">{name}</h1>
            <p style="margin: 0; font-size: 1.2em; opacity: 0.9;">{title}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_stats_cards(self, stats: Dict[str, Any]):
        """Render statistics cards."""
        cols = st.columns(len(stats))
        
        for i, (label, value) in enumerate(stats.items()):
            with cols[i]:
                st.markdown(f"""
                <div class="stat-card">
                    <h2 style="color: #1f77b4; margin: 0; font-size: 2.5em;">{value}</h2>
                    <p style="margin: 0.5rem 0 0 0; color: #666; text-transform: uppercase; 
                       letter-spacing: 0.5px; font-size: 0.9em;">{label}</p>
                </div>
                """, unsafe_allow_html=True)
    
    def render_analytics_dashboard(self, analytics_data: Dict):
        """Render analytics dashboard with charts."""
        st.subheader("📊 Analytics Dashboard")
        
        # Create tabs for different analytics views
        tab1, tab2, tab3 = st.tabs(["Overview", "Trends", "Questions"])
        
        with tab1:
            # Overview metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Conversations", 
                         analytics_data.get('total_conversations', 0))
            
            with col2:
                st.metric("Unique Visitors", 
                         analytics_data.get('unique_visitors', 0))
            
            with col3:
                st.metric("New Contacts", 
                         analytics_data.get('new_contacts', 0))
            
            with col4:
                avg_engagement = (analytics_data.get('total_conversations', 0) / 
                                max(analytics_data.get('unique_visitors', 1), 1))
                st.metric("Avg. Engagement", f"{avg_engagement:.1f}")
        
        with tab2:
            # Trends visualization
            self.render_trends_chart(analytics_data)
        
        with tab3:
            # Unknown questions
            self.render_questions_analysis(analytics_data)
    
    def render_trends_chart(self, analytics_data: Dict):
        """Render trends chart."""
        # Sample data - replace with real data
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), 
                             end=datetime.now(), freq='D')
        conversations = [max(0, int(10 + 5 * (i % 7 - 3.5))) for i in range(len(dates))]
        
        df = pd.DataFrame({
            'Date': dates,
            'Conversations': conversations
        })
        
        fig = px.line(df, x='Date', y='Conversations', 
                     title="Daily Conversations Trend",
                     color_discrete_sequence=[self.primary_color])
        
        fig.update_layout(
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_questions_analysis(self, analytics_data: Dict):
        """Render unknown questions analysis."""
        questions = analytics_data.get('common_unknown_questions', [])
        
        if questions:
            st.subheader("Most Common Unknown Questions")
            
            for i, (question, frequency) in enumerate(questions, 1):
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; 
                           margin-bottom: 0.5rem; border-left: 3px solid #ff7f0e;">
                    <strong>#{i}</strong> {question}
                    <span style="float: right; color: #666;">Asked {frequency} times</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No unknown questions recorded yet.")
    
    def render_contact_management(self, contacts: List[Dict]):
        """Render contact management section."""
        st.subheader("👥 Recent Contacts")
        
        if contacts:
            for contact in contacts:
                interest_color = {
                    1: "#dc3545", 2: "#dc3545", 3: "#ffc107", 
                    4: "#ffc107", 5: "#28a745", 6: "#28a745",
                    7: "#28a745", 8: "#28a745", 9: "#28a745", 10: "#28a745"
                }.get(contact.get('interest_level', 5), "#ffc107")
                
                st.markdown(f"""
                <div class="contact-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>{contact.get('name', 'Unknown')}</strong><br>
                            <small style="color: #666;">
                                {contact.get('email', 'No email')} • 
                                {contact.get('company', 'No company')}
                            </small>
                        </div>
                        <div style="text-align: right;">
                            <span style="background: {interest_color}; color: white; 
                                       padding: 2px 8px; border-radius: 12px; font-size: 0.8em;">
                                Interest: {contact.get('interest_level', 5)}/10
                            </span><br>
                            <small style="color: #666;">
                                {contact.get('created_at', 'Unknown date')[:10]}
                            </small>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No contacts recorded yet.")
    
    def render_document_browser(self, documents: Dict[str, Dict]):
        """Render document browser."""
        st.subheader("📄 Document Browser")
        
        if not documents:
            st.info("No documents processed yet.")
            return
        
        # Document search
        search_query = st.text_input("🔍 Search documents...")
        
        # Filter documents
        filtered_docs = documents
        if search_query:
            filtered_docs = {
                k: v for k, v in documents.items() 
                if (search_query.lower() in k.lower() or 
                    search_query.lower() in v.get('summary', '').lower())
            }
        
        # Display documents in columns
        cols = st.columns(3)
        for i, (filename, doc_info) in enumerate(filtered_docs.items()):
            if 'error' in doc_info:
                continue
                
            with cols[i % 3]:
                file_type = doc_info.get('file_type', 'unknown')
                file_icon = {
                    '.pdf': '📄', '.docx': '📝', '.txt': '📋', 
                    '.md': '📖', '.json': '🔧'
                }.get(file_type, '📁')
                
                with st.expander(f"{file_icon} {filename}"):
                    st.write(f"**Type:** {file_type}")
                    st.write(f"**Size:** {doc_info.get('content_length', 0):,} chars")
                    
                    summary = doc_info.get('summary', 'No summary available')
                    st.write(f"**Summary:** {summary}")
                    
                    keywords = doc_info.get('keywords', [])
                    if keywords:
                        keyword_tags = ' '.join([f"`{kw}`" for kw in keywords[:5]])
                        st.write(f"**Keywords:** {keyword_tags}")
    
    def render_chat_interface(self):
        """Render the main chat interface."""
        st.subheader("💬 Chat with Denver")
        
        # Chat container
        chat_container = st.container()
        
        with chat_container:
            # Display chat history
            if 'messages' not in st.session_state:
                st.session_state.messages = []
            
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        return chat_container
    
    def render_sidebar_info(self, stats: Dict):
        """Render sidebar with quick information."""
        with st.sidebar:
            st.markdown("### 📊 Quick Stats")
            
            for key, value in stats.items():
                st.metric(key.replace('_', ' ').title(), value)
            
            st.markdown("### 🔗 Quick Links")
            st.markdown("""
            - [LinkedIn Profile](https://linkedin.com/in/denvermagtibay)
            - [GitHub Portfolio](https://github.com/WarDen-Git)
            - [Email Contact](mailto:engr.denver.magtibay@gmail.com)
            """)
            
            st.markdown("### 💡 Features")
            st.markdown("""
            ✅ Multi-document processing  
            ✅ Visitor analytics  
            ✅ Smart contact management  
            ✅ Real-time insights  
            """)
    
    def render_notification(self, message: str, type: str = "info"):
        """Render a notification."""
        if type == "success":
            st.success(message)
        elif type == "warning":
            st.warning(message)
        elif type == "error":
            st.error(message)
        else:
            st.info(message)
    
    def create_performance_chart(self, data: Dict):
        """Create a performance metrics chart."""
        metrics = list(data.keys())
        values = list(data.values())
        
        fig = go.Figure(data=[
            go.Bar(x=metrics, y=values, 
                   marker_color=self.primary_color,
                   text=values,
                   textposition='auto')
        ])
        
        fig.update_layout(
            title="Performance Metrics",
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        
        return fig
    
    def render_status_indicator(self, status: str):
        """Render a status indicator."""
        status_colors = {
            'online': '🟢',
            'busy': '🟡', 
            'offline': '🔴',
            'away': '⚪'
        }
        
        indicator = status_colors.get(status.lower(), '⚪')
        st.markdown(f"{indicator} **Status:** {status.title()}")
    
    def format_timestamp(self, timestamp: str) -> str:
        """Format timestamp for display."""
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M')
        except:
            return timestamp