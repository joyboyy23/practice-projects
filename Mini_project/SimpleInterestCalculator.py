def get_float_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Invalid input! Please enter a valid number.")

def y_or_n(prompt):
    while True:
        answer = input(prompt).lower()
        if answer in ['y', 'n']:
            return answer
        else:
            print("Please enter 'y' for yes or 'n' for no.")

def main():
    print("Welcome to Simple Interest Calculator!")
    
    while True:
        try:
            principal = get_float_input("Enter Principal amount (P): ")
            rate = get_float_input("Enter Rate of interest (R) in %: ")
            time = get_float_input("Enter Time period (T) in years: ")
            
            if principal < 0 or rate < 0 or time < 0:
                print("Principal, Rate, and Time must be non-negative. Please try again.")
                continue
            
            # Calculate Simple Interest
            simple_interest = (principal * rate * time) / 100
            total_amount = principal + simple_interest
            
            print(f"\n📊 Simple Interest (SI): {simple_interest:.2f}")
            print(f"💰 Total Amount (P + SI): {total_amount:.2f}")
            
            answer = y_or_n("\nDo you want to perform another calculation? (y/n): ")
            if answer == 'y':
                print("Starting a new calculation...\n")
            else:
                print("Thank you for using Simple Interest Calculator! Goodbye! 👋")
                break
        
        except Exception as e:
            print(f"An error occurred: {e}. Please try again.")
        
if __name__ == "__main__":
    main()