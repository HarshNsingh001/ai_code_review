"""AI-powered code review using OpenAI API"""
from openai import OpenAI
from django.conf import settings

class AICodeChecker:
    """Uses OpenAI to provide intelligent code review feedback"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def review_code(self, code, language='python', analysis_summary=None):
        """
        Send code to OpenAI for review
        
        Args:
            code: Source code to review
            language: Programming language
            analysis_summary: Static analysis results
            
        Returns:
            AI-generated feedback
        """
        try:
            # Prepare context with analysis summary
            context = ""
            if analysis_summary:
                context = f"""
Static Analysis Results:
- Cyclomatic Complexity: Avg {analysis_summary['complexity'].get('average_complexity', 0)}, Max {analysis_summary['complexity'].get('max_complexity', 0)}
- Maintainability Index: {analysis_summary.get('maintainability_index', 0)}
- Issues Found: {analysis_summary.get('total_issues', 0)}
"""
            
            prompt = f"""You are an expert code reviewer. Review the following {language} code and provide:
1. Overall code quality assessment
2. Best practices violations
3. Potential bugs or edge cases
4. Security concerns
5. Performance improvements
6. Refactoring suggestions

{context}

Code to review:
```{language}
{code}
```

Provide a structured review with specific, actionable feedback."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert code reviewer who provides constructive, detailed feedback."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"AI Review unavailable: {str(e)}"
    
    def suggest_improvements(self, code, issues):
        """Generate specific improvement suggestions based on found issues"""
        if not issues:
            return "No critical issues found. Code looks good!"
        
        try:
            issues_text = "\n".join([f"- {issue.get('message', issue.get('type', 'Unknown'))}" for issue in issues[:5]])
            
            prompt = f"""Given these code issues:
{issues_text}

Provide 3-5 specific, actionable improvements for this code. Be concise and practical."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful code mentor."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Unable to generate suggestions: {str(e)}"