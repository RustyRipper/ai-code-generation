import os
import ast
import re
from collections import defaultdict


def analyze_code(code, filename):
    results = {"Filename": filename}

    # Keyword Distribution
    keywords = ['if', 'else', 'for', 'while', 'def', 'class', 'try', 'except']
    keyword_distribution = {kw: len(re.findall(r'\b' + kw + r'\b', code)) for kw in keywords}
    results["Keyword Distribution"] = keyword_distribution

    # Naming Conventions
    pascal_case = len(re.findall(r'\b[A-Z][a-z]*[A-Z][a-z]*\b', code))
    snake_case = len(re.findall(r'\b[a-z]+(_[a-z]+)+\b', code))
    results["Naming Conventions"] = {"PascalCase": pascal_case, "snake_case": snake_case}

    # Comment Analysis
    comments = re.findall(r'#.*', code)
    average_comment_length = sum(len(comment) for comment in comments) / len(comments) if comments else 0
    overly_detailed_comments = sum(1 for comment in comments if len(comment) > 40)
    results["Comments"] = {
        "Total Comments": len(comments),
        "Average Length": average_comment_length,
        "Overly Detailed Comments": overly_detailed_comments
    }

    # Cyclomatic Complexity
    tree = ast.parse(code)
    complexity = 1
    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.FunctionDef)):
            complexity += 1
    results["Cyclomatic Complexity"] = complexity

    # Code Duplication Detection
    def find_duplicate_functions(tree):
        function_names = defaultdict(list)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                function_names[node.name].append(ast.get_source_segment(code, node))

        duplicates = {name: func_code for name, func_code in function_names.items() if len(func_code) > 1}
        return duplicates

    duplicates = find_duplicate_functions(tree)
    results["Duplicate Functions"] = {name: len(funcs) for name, funcs in duplicates.items()}

    # Repetitive Patterns Check
    repetitive_patterns = re.findall(r'\b\w+\b', code)
    repetitive_count = len([word for word in repetitive_patterns if repetitive_patterns.count(word) > 3])
    results["Repetitive Patterns"] = repetitive_count

    # Variable & Function Naming Analysis
    overly_descriptive_names = sum(
        1 for name in re.findall(r'\b[a-zA-Z_]{10,}\b', code) if '_' in name
    )
    results["Overly Descriptive Names"] = overly_descriptive_names

    # Simple Logic and Default Values
    default_values = len(re.findall(r'\b=\s*[\'\"\d\[\]\{\}\(\)]', code))
    results["Default Values"] = default_values

    # Exception Handling
    exception_handlers = len(re.findall(r'\btry\b.*?\bexcept\b', code, re.DOTALL))
    results["Exception Handling"] = exception_handlers

    # AI Generated Probability
    ai_score = 0
    total_weight = 9

    ai_score += (complexity < 10) * (1 / total_weight)
    ai_score += (average_comment_length > 15) * (2 / total_weight)
    ai_score += (pascal_case == 0) * (1 / total_weight)
    ai_score += (snake_case > 0) * (1 / total_weight)
    ai_score += (len(duplicates) > 0) * (0.5 / total_weight)
    ai_score += (repetitive_count > 5) * (1 / total_weight)
    ai_score += (overly_descriptive_names > 2) * (1 / total_weight)
    ai_score += (default_values > 2) * (0.5 / total_weight)
    ai_score += (exception_handlers <= 2) * (1 / total_weight)

    ai_probability = ai_score * 100
    results["AI Generated Probability (%)"] = round(ai_probability, 2)

    return results


def analyze_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                code = file.read()
                results = analyze_code(code, filename)

                print(f"=== Analysis for {directory}/{filename} ===")
                # for key, value in results.items():
                #     print(f"{key}: {value}")
                print(f"'AI Generated Probability (%): {results['AI Generated Probability (%)']}")
                print("\n")


analyze_directory('code_samples/ai')
analyze_directory('code_samples/human')
