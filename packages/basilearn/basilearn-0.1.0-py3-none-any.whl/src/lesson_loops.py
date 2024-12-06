def lesson_loops():
    print("Welcome to Lesson 4: Loops")
    print("-------------------------------------------------")
    print("Loops allow you to execute a block of code multiple times.")
    print("Python has two main types of loops: `for` loops and `while` loops.\n")
    print("Type 'exit' at any time to quit the lesson.\n")

    input("Press Enter to continue...\n")

    # Section 1: `for` Loops
    print("A `for` loop iterates over a sequence, like a list or a range of numbers.")
    print("Example:")
    print("    for i in range(5):")
    print("        print(i)\n")
    print("This will print numbers from 0 to 4.\n")

    input("Press Enter to try it yourself...\n")
    print("Now, let's try writing your own `for` loop!")

    while True:
        print("\nType your `for` loop below. To finish, type 'END' on a new line:")
        user_code = []
        while True:
            line = input(">>> ").rstrip()
            if line.lower() == 'end':
                break
            user_code.append(line)

        if 'exit' in "".join(user_code).lower():
            print("\nRecap of `for` Loops:")
            print("- A `for` loop iterates over sequences like ranges or lists.")
            print("- Syntax: `for item in sequence:`")
            print("- Example: `for i in range(3): print(i)` prints 0, 1, 2.\n")
            break

        try:
            # Join the user code and execute it
            code_to_execute = "\n".join(user_code)
            print("\nYour code:")
            print(code_to_execute)
            print("\nExecuting your code...")
            exec(code_to_execute)
            print("✅ Good job! You successfully wrote a `for` loop.")
        except SyntaxError as e:
            print(f"❌ Syntax error: {e}. Ensure your loop is properly formatted.")
        except Exception as e:
            print(f"❌ Error: {e}. Something went wrong. Check your syntax and try again.")

        continue_experimenting = input("Do you want to try another loop? (yes/no): ").strip().lower()
        if continue_experimenting != 'yes':
            break

    # Section 2: `while` Loops
    input("\nPress Enter to learn about `while` loops...\n")
    print("A `while` loop repeats as long as a condition is true.")
    print("Example:")
    print("    count = 0")
    print("    while count < 5:")
    print("        print(count)")
    print("        count += 1\n")

    input("Press Enter to try it yourself...\n")
    print("Now, let's try writing your own `while` loop!")

    while True:
        print("\nType your `while` loop below. To finish, type 'END' on a new line:")
        user_code = []
        while True:
            line = input(">>> ").rstrip()
            if line.lower() == 'end':
                break
            user_code.append(line)

        if 'exit' in "".join(user_code).lower():
            print("\nRecap of `while` Loops:")
            print("- A `while` loop repeats as long as the condition remains true.")
            print("- Syntax: `while condition:`")
            print("- Example: `while x < 5: print(x); x += 1`.\n")
            break

        try:
            # Join the user code and execute it
            code_to_execute = "\n".join(user_code)
            print("\nYour code:")
            print(code_to_execute)
            print("\nExecuting your code...")
            exec(code_to_execute)
            print("✅ Good job! You successfully wrote a `while` loop.")
        except SyntaxError as e:
            print(f"❌ Syntax error: {e}. Ensure your loop is properly formatted.")
        except Exception as e:
            print(f"❌ Error: {e}. Something went wrong. Check your syntax and try again.")

        continue_experimenting = input("Do you want to try another loop? (yes/no): ").strip().lower()
        if continue_experimenting != 'yes':
            break

    print("\nFinal Recap of Loops:")
    print("- Loops help you repeat blocks of code.")
    print("- `for` loops iterate over sequences like lists or ranges.")
    print("- `while` loops repeat as long as a condition is true.")
    print("Thank you for completing Lesson 4!")
lesson_loops()