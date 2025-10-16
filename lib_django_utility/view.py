from rest_framework.exceptions import ValidationError
import re
from functools import wraps


def extract_variables_from_condition(condition):
    """
    Extracts variable names from a condition string.

    Args:
        condition (str): The condition string.

    Returns:
        List[str]: List of variable names found in the condition.
    """
    return re.findall(r'\b\w+\b', condition)


def require_query_params(*required_params):
    """
    Decorator to ensure required query parameters are present in the request.

    Args:
        required_params: List of required query parameter names.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(view, request, *args, **kwargs):
            # Check if all required query parameters are present
            missing_params = [
                param for param in required_params if isinstance(param, str) and param not in request.query_params
            ]
            if missing_params:
                raise ValidationError(
                    code="required",
                )
            conditional_params = [param for param in required_params if isinstance(param, tuple)]
            for condition, params_list in conditional_params:
                context = {var: request.query_params.get(var) for var in extract_variables_from_condition(condition)}

                # Evaluate the condition within the context
                if eval(condition, {}, context):
                    missing_params = [
                        param for param in params_list if
                        isinstance(param, str) and param not in request.query_params
                    ]
                    if missing_params:
                        raise ValidationError(
                            code="required",
                        )

            return view_func(view, request, *args, **kwargs)

        return _wrapped_view

    return decorator
