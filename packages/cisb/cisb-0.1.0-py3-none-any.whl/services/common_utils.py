import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline_checks.log"),  # Log to a file
        logging.StreamHandler()  # Print to the console
    ]
)

def run_checks(checks, context_name="General Compliance"):
    """
    Runs the given checks and calculates the total score based on automated checks.
    Args:
        checks (list): A list of tuples where each tuple contains:
                       - the check function
                       - the arguments for the check function
                       - a boolean indicating whether the check is manual (True for manual, False for automated)
        context_name (str): The context name for these checks (e.g., 'Artifacts', 'Dependencies').
                            This will be included in the summary to reflect the specific area being checked.
    Returns:
        dict: A dictionary of the results of each check with their scores and messages.
    """
    total_score = 0
    total_possible_score = 0
    results = {}
    manual_checks = []
    manual_check_count = 0

    for check, args, is_manual in checks:
        logging.info(f"Running {check.__name__} in {context_name}...")

        try:
            result = check(*args)
            
            # Handle automated checks and manual checks that return scores
            if isinstance(result, tuple):
                score, message = result
                if score is None:
                    # For manual checks, just record None, but don't increment totals
                    if is_manual:
                        results[check.__name__] = {
                            "compliance_score": None,
                            "message": message,
                        }
                    else:
                        total_possible_score += 5
                else:
                    if not is_manual:
                        total_score += score
                        total_possible_score += 5

                if is_manual:
                    manual_check_count += 1
                    manual_checks.append(check.__name__)

                results[check.__name__] = {
                    "compliance_score": score,
                    "message": message,
                }
                logging.info(f"Score: {score}, Message: {message}")

            # Handle manual checks that return None
            elif result is None and is_manual:
                results[check.__name__] = {
                    "compliance_score": None,
                    "message": "Manual check required",
                }
                manual_check_count += 1
                manual_checks.append(check.__name__)
                logging.info(f"{check.__name__}: Manual check required")

        except Exception as e:
            # Ensure that errors in manual checks are still counted as manual
            if is_manual:
                manual_check_count += 1
                manual_checks.append(check.__name__)

            results[check.__name__] = {
                "compliance_score": None,
                "message": f"Error running check: {str(e)}",
            }
            logging.error(f"Error running {check.__name__}: {str(e)}")

        print("\n")  # Space after each check's output

    print("\n===========================")
    print(
        f"Total {context_name} compliance score: {total_score}/{total_possible_score}"
    )
    print(f"Number of manual checks: {manual_check_count}")
    if manual_checks:
        print(f"Manual checks performed: {', '.join(manual_checks)}")
    print("===========================")

    # Return both score and detailed results for manual checks
    return results

