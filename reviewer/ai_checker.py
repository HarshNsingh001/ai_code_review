"""
This class provides AI-powered code review using OpenAI's GPT API.
It integrates with Django settings to get the API key.
"""

from openai import OpenAI
from django.conf import settings

class AICodeChecker:
    """
    AICodeChecker connects to OpenAI's GPT API and provides:
    - Detailed code review
    - Best practices analysis
    - Suggestions for improvements
    """

    def __init__(self):
        """
        Initialize the OpenAI client using the API key from Django settings.
        """
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def review_code(self, code, language='python', analysis_summary=None):
        """
        Review the given code and return an AI-powered evaluation.

        Parameters:
        - code (str): The source code to review.
        - language (str): Programming language (default: python).
        - analysis_summary (dict, optional): Results from static analysis like complexity.

        Returns:
        - str: Detailed feedback from the AI.
        """
        try:
            # Include static analysis results if provided
            context = ""
            if analysis_summary:
                avg_complexity = analysis_summary['complexity'].get('average_complexity', 0)
                max_complexity = analysis_summary['complexity'].get('max_complexity', 0)
                maintainability = analysis_summary.get('maintainability_index', 0)
                total_issues = analysis_summary.get('total_issues', 0)

                context = (
                    "Static Analysis Summary:\n"
                    f"- Cyclomatic Complexity: Avg {avg_complexity}, Max {max_complexity}\n"
                    f"- Maintainability Index: {maintainability}\n"
                    f"- Issues Found: {total_issues}\n"
                )

            # Prepare the prompt for GPT
            prompt = (
                f"You are an expert code reviewer. Review the following {language} code and provide:\n"
                "1. Overall code quality assessment\n"
                "2. Best practices violations\n"
                "3. Potential bugs or edge cases\n"
                "4. Security concerns\n"
                "5. Performance improvements\n"
                "6. Refactoring suggestions\n\n"
                f"{context}\n"
                f"Code to review:\n```{language}\n{code}\n```\n"
                "Provide structured and actionable feedback."
            )

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert code reviewer who provides constructive, detailed feedback."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )

            # Return AI's response
            return response.choices[0].message.content

        except Exception as e:
            # If something goes wrong, return an error message
            return f"AI Review unavailable: {str(e)}"

    def suggest_improvements(self, code, issues):
        """
        Suggest practical improvements based on detected issues.

        Parameters:
        - code (str): Source code (optional for context)
        - issues (list): List of issues found in the code

        Returns:
        - str: Recommendations from AI
        """
        if not issues:
            return "No critical issues found. Code looks good!"

        try:
            # Summarize issues into text for the AI
            issues_text = "\n".join([f"- {issue.get('message', issue.get('type', 'Unknown'))}" for issue in issues[:5]])

            prompt = (
                f"Given these code issues:\n{issues_text}\n\n"
                "Provide 3-5 specific, actionable improvements for this code. Be concise and practical."
            )

            # Call OpenAI API
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
