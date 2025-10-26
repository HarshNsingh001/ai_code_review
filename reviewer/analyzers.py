from radon.complexity import cc_visit
from radon.metrics import mi_visit
import re

class CodeAnalyzer:
    """
    Analyzes code for:
    - Cyclomatic complexity
    - Maintainability
    - Common issues like long lines, TODOs, print statements, bare except clauses
    """

    def __init__(self, code, language='python'):
        """
        Initialize the analyzer with code and language.

        Parameters:
        - code (str): The source code to analyze
        - language (str): Programming language (default: python)
        """
        self.code = code
        self.language = language
        self.issues = []  # Stores detected issues

    def analyze_complexity(self):
        """
        Calculate cyclomatic complexity using Radon.

        Returns:
        - dict: average_complexity and max_complexity
        """
        if self.language != 'python':
            return {'average_complexity': 0, 'max_complexity': 0}

        try:
            results = cc_visit(self.code)
            if not results:
                return {'average_complexity': 0, 'max_complexity': 0}

            complexities = [r.complexity for r in results]
            avg_complexity = sum(complexities) / len(complexities)
            max_complexity = max(complexities)

            # Flag functions with high complexity
            for r in results:
                if r.complexity > 10:
                    self.issues.append({
                        'type': 'high_complexity',
                        'function': r.name,
                        'complexity': r.complexity,
                        'message': f"Function '{r.name}' has high cyclomatic complexity ({r.complexity}). Consider refactoring."
                    })

            return {
                'average_complexity': round(avg_complexity, 2),
                'max_complexity': max_complexity
            }

        except Exception as e:
            return {'average_complexity': 0, 'max_complexity': 0, 'error': str(e)}

    def check_common_issues(self):
        """
        Detect common issues in the code, including:
        - Long lines (>120 characters)
        - TODO/FIXME comments
        - Print statements (should use logging)
        - Bare except clauses
        """
        lines = self.code.split('\n')

        # Long lines
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                self.issues.append({
                    'type': 'style',
                    'line': i,
                    'message': f"Line {i} exceeds 120 characters ({len(line)} chars)"
                })

        # TODO/FIXME comments
        for i, line in enumerate(lines, 1):
            if 'TODO' in line or 'FIXME' in line:
                self.issues.append({
                    'type': 'todo',
                    'line': i,
                    'message': f"Line {i} contains TODO/FIXME comment"
                })

        # Print statements
        if self.language == 'python':
            for i, line in enumerate(lines, 1):
                if re.search(r'\bprint\s*\(', line) and not line.strip().startswith('#'):
                    self.issues.append({
                        'type': 'debug',
                        'line': i,
                        'message': f"Line {i} contains print statement - consider using logging"
                    })

        # Bare except clauses
        if self.language == 'python':
            for i, line in enumerate(lines, 1):
                if 'except:' in line or 'except :' in line:
                    self.issues.append({
                        'type': 'error_handling',
                        'line': i,
                        'message': f"Line {i} has bare except clause - specify exception type"
                    })

        return self.issues

    def calculate_maintainability_index(self):
        """
        Calculate the maintainability index of the code using Radon.

        Returns:
        - float: Maintainability index score
        """
        if self.language != 'python':
            return 0

        try:
            mi = mi_visit(self.code, multi=True)
            return round(mi, 2) if mi else 0
        except Exception:
            return 0

    def get_analysis_summary(self):
        """
        Get a complete analysis summary combining:
        - Cyclomatic complexity
        - Maintainability index
        - Detected issues
        - Total issues and lines of code

        Returns:
        - dict: Analysis summary
        """
        complexity = self.analyze_complexity()
        self.check_common_issues()
        maintainability = self.calculate_maintainability_index()

        return {
            'complexity': complexity,
            'maintainability_index': maintainability,
            'issues': self.issues,
            'total_issues': len(self.issues),
            'lines_of_code': len(self.code.split('\n'))
        }
