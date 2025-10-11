def cel2far(temp):
    far = float(temp * 9/5) + 32
    return far

def far2cel(temp):
    cel = (float(temp - 32) * 5/9)
    return cel

def menu():
    multiline_string = """
    ("Temperature Converter")
=================================
("1. Celsius to Fahrenheit")
("2. Fahrenheit to Celsius")
("3. Exit")
=================================
"""
    print(multiline_string)

def get_temperature():
        while True:
            try:
                temp = float(input("Enter temperature: "))
                return temp
            except ValueError:
                print("Invalid input! Please enter a valid number.")

def main():
    while True:
        menu()
        choice = int(input("Enter your choice (1-3): "))

        if choice == 3:
            print("Exiting the program. Goodbye!")
            break
        elif choice in [1, 2]:
            temp = get_temperature()
            if choice == 1:
                result = cel2far(temp)
                print(f"{temp}°C is {result}°F")
            elif choice == 2:
                result = far2cel(temp)
                print(f"{temp}°F is {result}°C")
        else:
            print("Invalid choice! Please select 1-3.")
            
if __name__ == "__main__":
    main()
    
