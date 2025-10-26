"""Code analysis utilities using radon for complexity analysis"""
from radon.complexity import cc_visit
from radon.metrics import mi_visit
import re

class CodeAnalyzer:
    """Analyzes code for complexity and common issues"""
    
    def __init__(self, code, language='python'):
        self.code = code
        self.language = language
        self.issues = []
    
    def analyze_complexity(self):
        """Calculate cyclomatic complexity using radon"""
        if self.language != 'python':
            return {'average_complexity': 0, 'max_complexity': 0}
        
        try:
            complexity_results = cc_visit(self.code)
            if not complexity_results:
                return {'average_complexity': 0, 'max_complexity': 0}
            
            complexities = [result.complexity for result in complexity_results]
            avg_complexity = sum(complexities) / len(complexities)
            max_complexity = max(complexities)
            
            # Flag high complexity
            for result in complexity_results:
                if result.complexity > 10:
                    self.issues.append({
                        'type': 'high_complexity',
                        'function': result.name,
                        'complexity': result.complexity,
                        'message': f"Function '{result.name}' has high cyclomatic complexity ({result.complexity}). Consider refactoring."
                    })
            
            return {
                'average_complexity': round(avg_complexity, 2),
                'max_complexity': max_complexity
            }
        except Exception as e:
            return {'average_complexity': 0, 'max_complexity': 0, 'error': str(e)}
    
    def check_common_issues(self):
        """Check for common code issues and style violations"""
        lines = self.code.split('\n')
        
        # Check for very long lines
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                self.issues.append({
                    'type': 'style',
                    'line': i,
                    'message': f"Line {i} exceeds 120 characters ({len(line)} chars)"
                })
        
        # Check for TODO comments
        for i, line in enumerate(lines, 1):
            if 'TODO' in line or 'FIXME' in line:
                self.issues.append({
                    'type': 'todo',
                    'line': i,
                    'message': f"Line {i} contains TODO/FIXME comment"
                })
        
        # Check for print statements (Python)
        if self.language == 'python':
            for i, line in enumerate(lines, 1):
                if re.search(r'\bprint\s*\(', line) and not line.strip().startswith('#'):
                    self.issues.append({
                        'type': 'debug',
                        'line': i,
                        'message': f"Line {i} contains print statement - consider using logging"
                    })
        
        # Check for empty except blocks
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
        """Calculate maintainability index"""
        if self.language != 'python':
            return 0
        
        try:
            mi = mi_visit(self.code, multi=True)
            return round(mi, 2) if mi else 0
        except:
            return 0
    
    def get_analysis_summary(self):
        """Get complete analysis summary"""
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