from datetime import datetime

from django.core.exceptions import ValidationError


class ValidatesProperties:
    validation_rules = {}

    def validate(self, data):
        """
        Validate the component's properties.
        """
        validation_rules = getattr(self, "validation_rules", None)
        if not validation_rules:
            return

        errors = {}

        for field, rules in validation_rules.items():
            value = data.get(field)
            for rule in rules:
                rule_parts = rule.split(":")
                rule_name = rule_parts[0]
                rule_args = rule_parts[1:] if len(rule_parts) > 1 else []

                method_name = f"validate_{rule_name}"
                method = getattr(self, method_name, None)

                if method:
                    error = method(value, *rule_args)
                    if error:
                        errors.setdefault(field, []).append(error)

        if errors:
            raise ValidationError(errors)

        return errors

    # Validators
    def validate_required(self, value):
        if value is None or (isinstance(value, str) and not value.strip()):
            return "This field is required."

    def validate_email(self, value):
        pattern = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(pattern, value):
            return "Invalid email format."

    def validate_min_length(self, value, length):
        if len(value) < length:
            return f"This field must be at least {length} characters."

    def validate_max_length(self, value, length):
        if len(value) > length:
            return f"This field must not exceed {length} characters."

    def validate_date_equals(self, value, compare_date):
        try:
            date_value = datetime.strptime(value, "%Y-%m-%d")
            if date_value.date() != compare_date.date():
                return "The date does not match the given date."
            return None
        except ValueError:
            return "The value is not a valid date."

    def validate_exists(self, value, data_list):
        # Simplified exists check against a list. In Laravel, it checks against a DB.
        if value not in data_list:
            return "The selected value is invalid."
        return None

    def validate_file(self, file_obj):
        if not hasattr(file_obj, "read"):
            return "The value is not a valid file."
        return None

    def validate_integer(self, value):
        if not isinstance(value, int):
            return "The value is not an integer."
        return None

    def validate_nullable(self, value):
        # If value is None or an empty string, validation passes. Else, it fails.
        if value in [None, ""]:
            return None
        return "The value is not nullable."

    def validate_alpha_dash(self, value):
        if not re.match("^[a-zA-Z0-9_-]*$", value):
            return (
                "The value may only contain letters, numbers, dashes, and underscores."
            )
        return None

    def validate_alpha_num(self, value):
        if not value.isalnum():
            return "The value may only contain letters and numbers."
        return None

    def validate_array(self, value):
        if not isinstance(value, list):
            return "The value must be an array."
        return None

    def validate_url(self, value):
        # Placeholder: This is a complex one in Laravel, requiring DNS checks. Here's a simplified version:
        import validators

        if not validators.url(value):
            return "The URL is not valid."
        return None

    def validate_max(self, value, max_val):
        if len(value) > max_val:
            return f"The value must not be greater than {max_val} characters."
        return None

    def validate_min(self, value, min_val):
        if len(value) < min_val:
            return f"The value must be at least {min_val} characters."
        return None

    def validate_not_in(self, value, *args):
        if value in args:
            return "The selected value is invalid."
        return None

    def validate_regex(self, value, pattern):
        if not re.match(pattern, value):
            return "The value format is invalid."
        return None

    def validate_starts_with(self, value, *args):
        if not value.startswith(args):
            return "The value must start with one of the following: " + ", ".join(args)
        return None

    def validate_numeric(self, value):
        if not isinstance(value, (int, float)):
            return "The value must be numeric."
        return None

    def validate_boolean(self, value):
        if not isinstance(value, bool):
            return "The value must be boolean."
        return None

    def validate_confirmed(self, value, confirmation_field):
        if value != self.data.get(confirmation_field):
            return "The confirmation does not match."
        return None

    def validate_date(self, value, format="%Y-%m-%d"):
        try:
            datetime.strptime(value, format)
            return None
        except ValueError:
            return "The value is not a valid date."

    def validate_before(self, value, date_string):
        input_date = datetime.strptime(value, "%Y-%m-%d")
        comparison_date = datetime.strptime(date_string, "%Y-%m-%d")
        if input_date >= comparison_date:
            return f"The date must be before {date_string}."
        return None

    def validate_after(self, value, date_string):
        input_date = datetime.strptime(value, "%Y-%m-%d")
        comparison_date = datetime.strptime(date_string, "%Y-%m-%d")
        if input_date <= comparison_date:
            return f"The date must be after {date_string}."
        return None

    def validate_between(self, value, min_val, max_val):
        if not min_val <= len(value) <= max_val:
            return f"The value length must be between {min_val} and {max_val}."
        return None

    def validate_different(self, value, other_field):
        if value == self.data.get(other_field):
            return f"The value must be different from {other_field}."
        return None

    def validate_alpha(self, value):
        if not value.isalpha():
            return "The value must be alphabetic."
        return None
