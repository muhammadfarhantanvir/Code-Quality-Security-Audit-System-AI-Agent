"""
Streamlit dashboard for the audit system
"""

import os
import pandas as pd
import streamlit as st
import plotly.express as px
from dataclasses import asdict

from ..core.auditor import CodeAuditor


def create_streamlit_dashboard():
    """Create Streamlit dashboard for the audit system"""
    st.set_page_config(
        page_title="Code Quality & Security Audit System",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 Code Quality & Security Audit System")
    st.markdown("### Automated Code Analysis with Local AI Models")
    
    # Initialize auditor
    auditor = CodeAuditor()
    
    # Sidebar
    st.sidebar.header("Audit Configuration")
    
    # Check Ollama status
    ollama_status = auditor.ollama.is_available()
    status_color = "🟢" if ollama_status else "🔴"
    st.sidebar.markdown(f"**Ollama Status:** {status_color} {'Connected' if ollama_status else 'Disconnected'}")
    
    if not ollama_status:
        st.sidebar.warning("Ollama is not running. Only pattern-based analysis will be available.")
    
    # Directory input
    directory_path = st.sidebar.text_input(
        "Project Directory Path",
        value="./sample_project",
        help="Enter the path to your project directory"
    )
    
    # Advanced options
    with st.sidebar.expander("Advanced Options"):
        use_ai = st.checkbox("Enable AI Analysis", value=not st.sidebar.checkbox("Disable AI", value=False))
        severity_filter = st.selectbox("Minimum Severity", ["ALL", "LOW", "MEDIUM", "HIGH"], index=0)
        max_file_size = st.number_input("Max File Size (chars)", value=2000, min_value=100, max_value=10000)
    
    # Scan button
    if st.sidebar.button("🚀 Start Audit", type="primary"):
        if not os.path.exists(directory_path):
            st.error(f"Directory '{directory_path}' does not exist!")
        else:
            with st.spinner("Scanning project... This may take a few minutes."):
                try:
                    config = {
                        'scanning': {
                            'max_file_size': max_file_size
                        }
                    }
                    auditor = CodeAuditor(config)
                    report = auditor.scan_directory(directory_path, use_ai=use_ai)
                    st.session_state['current_report'] = report
                    st.success("Audit completed successfully!")
                except Exception as e:
                    st.error(f"Error during audit: {str(e)}")
    
    # Display results
    if 'current_report' in st.session_state:
        report = st.session_state['current_report']
        
        # Filter by severity if needed
        if severity_filter != "ALL":
            report.security_issues = [i for i in report.security_issues if i.severity == severity_filter]
            report.quality_issues = [i for i in report.quality_issues if i.severity == severity_filter]
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Risk Score", f"{report.risk_score}/100")
        
        with col2:
            st.metric("Security Issues", len(report.security_issues))
        
        with col3:
            st.metric("Quality Issues", len(report.quality_issues))
        
        with col4:
            st.metric("Files Scanned", report.total_files)
        
        # Risk assessment
        risk_level = "HIGH" if report.risk_score > 70 else "MEDIUM" if report.risk_score > 30 else "LOW"
        risk_color = "red" if risk_level == "HIGH" else "orange" if risk_level == "MEDIUM" else "green"
        
        st.markdown(f"### Risk Assessment: <span style='color:{risk_color}'>{risk_level}</span>", unsafe_allow_html=True)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Security issues by type
            if report.security_issues:
                sec_df = pd.DataFrame([asdict(issue) for issue in report.security_issues])
                fig = px.bar(
                    sec_df.groupby(['issue_type', 'severity']).size().reset_index(name='count'),
                    x='issue_type',
                    y='count',
                    color='severity',
                    title="Security Issues by Type",
                    color_discrete_map={'HIGH': '#d32f2f', 'MEDIUM': '#f57c00', 'LOW': '#388e3c'}
                )
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.success("✅ No security issues found!")
        
        with col2:
            # Quality issues by type
            if report.quality_issues:
                qual_df = pd.DataFrame([asdict(issue) for issue in report.quality_issues])
                fig = px.pie(
                    qual_df.groupby('issue_type').size().reset_index(name='count'),
                    values='count',
                    names='issue_type',
                    title="Quality Issues Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.success("✅ No quality issues found!")
        
        # File type distribution
        if report.files_by_type:
            st.subheader("📁 Files by Type")
            files_df = pd.DataFrame(list(report.files_by_type.items()), columns=['Extension', 'Count'])
            fig = px.bar(files_df, x='Extension', y='Count', title="Files Scanned by Type")
            st.plotly_chart(fig, use_container_width=True)
        
        # Detailed issues
        tab1, tab2, tab3, tab4 = st.tabs(["🔐 Security Issues", "📊 Quality Issues", "💡 Recommendations", "📈 Metrics"])
        
        with tab1:
            if report.security_issues:
                st.subheader(f"Found {len(report.security_issues)} Security Issues")
                
                # Severity filter for display
                severity_counts = {}
                for issue in report.security_issues:
                    severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1
                
                if severity_counts:
                    st.write("**Issues by Severity:**")
                    for severity, count in sorted(severity_counts.items(), key=lambda x: ['LOW', 'MEDIUM', 'HIGH'].index(x[0])):
                        color = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🟢'}[severity]
                        st.write(f"{color} {severity}: {count}")
                
                st.write("---")
                
                for i, issue in enumerate(report.security_issues, 1):
                    severity_color = "🔴" if issue.severity == "HIGH" else "🟡" if issue.severity == "MEDIUM" else "🟢"
                    
                    with st.expander(f"{severity_color} {issue.issue_type} - {issue.file_path}:{issue.line_number}"):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown(f"**Severity:** {issue.severity}")
                            st.markdown(f"**Description:** {issue.description}")
                            if hasattr(issue, 'cwe_id') and issue.cwe_id:
                                st.markdown(f"**CWE ID:** {issue.cwe_id}")
                            st.code(issue.code_snippet, language="python")
                            st.markdown(f"**Recommendation:** {issue.recommendation}")
                        
                        with col2:
                            st.markdown("**Quick Actions:**")
                            st.button(f"📋 Copy Code", key=f"copy_sec_{i}")
                            st.button(f"🔗 View File", key=f"view_sec_{i}")
            else:
                st.success("🎉 No security issues detected!")
        
        with tab2:
            if report.quality_issues:
                st.subheader(f"Found {len(report.quality_issues)} Quality Issues")
                
                # Group by type
                issue_types = {}
                for issue in report.quality_issues:
                    issue_types[issue.issue_type] = issue_types.get(issue.issue_type, 0) + 1
                
                if issue_types:
                    st.write("**Issues by Type:**")
                    for issue_type, count in sorted(issue_types.items(), key=lambda x: x[1], reverse=True):
                        st.write(f"• {issue_type}: {count}")
                
                st.write("---")
                
                for i, issue in enumerate(report.quality_issues, 1):
                    severity_color = "🟡" if issue.severity == "MEDIUM" else "🟢"
                    
                    with st.expander(f"{severity_color} {issue.issue_type} - {issue.file_path}:{issue.line_number}"):
                        st.markdown(f"**Severity:** {issue.severity}")
                        st.markdown(f"**Description:** {issue.description}")
                        st.code(issue.code_snippet[:200] + "..." if len(issue.code_snippet) > 200 else issue.code_snippet, language="python")
                        st.markdown(f"**Recommendation:** {issue.recommendation}")
            else:
                st.success("🎉 No quality issues detected!")
        
        with tab3:
            st.subheader("💡 Strategic Recommendations")
            
            if report.recommendations:
                for i, rec in enumerate(report.recommendations, 1):
                    priority = "🔴 HIGH" if "URGENT" in rec else "🟡 MEDIUM" if any(word in rec for word in ["Implement", "Add"]) else "🟢 LOW"
                    st.markdown(f"{i}. {priority} - {rec}")
            
            # Business impact analysis
            st.subheader("💰 Business Impact Analysis")
            
            high_issues = len([i for i in report.security_issues if i.severity == "HIGH"])
            medium_issues = len([i for i in report.security_issues + report.quality_issues if i.severity == "MEDIUM"])
            
            # Estimated costs (placeholder calculations)
            potential_breach_cost = high_issues * 500000  # $500K per high-severity issue
            maintenance_savings = medium_issues * 5000    # $5K per medium issue
            technical_debt_hours = getattr(report.code_metrics, 'technical_debt_minutes', 0) // 60
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Potential Breach Cost Avoided", f"${potential_breach_cost:,}")
            with col2:
                st.metric("Annual Maintenance Savings", f"${maintenance_savings:,}")
            with col3:
                st.metric("Technical Debt (Hours)", f"{technical_debt_hours:,}")
            
            # Action plan
            st.subheader("📋 Action Plan")
            
            if high_issues > 0:
                st.error(f"🚨 **IMMEDIATE ACTION REQUIRED**: {high_issues} high-severity security issues need immediate attention")
            
            if medium_issues > 0:
                st.warning(f"⚠️ **SCHEDULE FIXES**: {medium_issues} medium-severity issues should be addressed within 2 weeks")
            
            if not high_issues and not medium_issues:
                st.success("✅ **MAINTAIN STANDARDS**: Code quality is good, continue current practices")
        
        with tab4:
            st.subheader("📊 Code Metrics")
            
            # Display code metrics
            metrics = report.code_metrics
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Lines of Code", f"{metrics.lines_of_code:,}")
                st.metric("Total Files", report.total_files)
                st.metric("Scan Duration", f"{report.scan_duration:.2f}s")
            
            with col2:
                st.metric("Technical Debt", f"{metrics.technical_debt_minutes} min")
                st.metric("Function Count", metrics.function_count)
                st.metric("Class Count", metrics.class_count)
            
            # Progress bars for ratios
            st.subheader("Quality Ratios")
            
            comment_ratio = min(metrics.comment_ratio, 1.0)
            st.progress(comment_ratio)
            st.caption(f"Comment Ratio: {comment_ratio:.1%}")
            
            # File type breakdown
            if report.files_by_type:
                st.subheader("File Distribution")
                for ext, count in sorted(report.files_by_type.items(), key=lambda x: x[1], reverse=True):
                    percentage = (count / report.total_files) * 100
                    st.write(f"{ext}: {count} files ({percentage:.1f}%)")
    
    # Historical reports section
    st.markdown("---")
    st.subheader("📈 Historical Reports")
    
    historical_reports = auditor.get_historical_reports()
    
    if historical_reports:
        df = pd.DataFrame(historical_reports)
        df['scan_date'] = pd.to_datetime(df['scan_date'])
        
        # Trend chart
        if len(df) > 1:
            fig = px.line(
                df.head(10),  # Show last 10 reports
                x='scan_date',
                y='risk_score',
                title="Risk Score Trend Over Time",
                markers=True
            )
            fig.update_layout(xaxis_title="Date", yaxis_title="Risk Score")
            st.plotly_chart(fig, use_container_width=True)
        
        # Table of recent reports
        st.subheader("Recent Audits")
        display_df = df[['project_path', 'scan_date', 'total_files', 'risk_score']].head(10)
        display_df['scan_date'] = display_df['scan_date'].dt.strftime('%Y-%m-%d %H:%M')
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("No historical reports found. Run your first audit to see trends over time.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>🔍 Code Quality & Security Audit System v1.0.0</p>
            <p>Powered by AI • Built with ❤️ for developers</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def main():
    """Main entry point for the dashboard"""
    create_streamlit_dashboard()


if __name__ == "__main__":
    main()