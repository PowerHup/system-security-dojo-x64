#!/opt/pwn.college/python
import hashlib
import binascii

file_path = "/challenge/elf-crackme-level2.2"


def read_flag():
    with open("/flag", "r") as file:
        file_contents = file.read()
        print(file_contents)


def calculate_md5(data):
    md5_hash = hashlib.md5(data).hexdigest()
    return md5_hash


def md5_check(hex_string):
    hex_string = hex_string.replace(" ", "")
    binary_data = binascii.unhexlify(hex_string)
    md5_result = calculate_md5(binary_data)
    return md5_result


def patch():
    try:
        with open(file_path, "r+b") as file:
            position = int(
                input(
                    "[+] Please enter the position to modify (in hexadecimal, e.g., 0x1000): "
                ),
                16,
            )
            new_data = input(
                "[+] Please enter the new data in seperate bytes (in hexadecimal, e.g., 01 be ef): "
            )

            file.seek(position)
            file.write(bytes.fromhex(new_data))

        print("[+] Modification completed!")
    except FileNotFoundError:
        print("[-] Unable to open the file")
    except Exception as e:
        print("[-] An error occurred:", e)


def check():
    try:
        with open(file_path, "rb") as file:
            position = 0x1060
            length = 405
            file.seek(position)
            data_read = file.read(length)
            md5_2 = calculate_md5(data_read)
            print("The current hash is", md5_2)
            if md5_2 == "ba4f77d33e8961855bda04916d50f802":
                print("[+] Modification completed!")
                read_flag()
            else:
                print(
                    "[-] Hash verification for the .text segment failed. Please modify it again."
                )

    except Exception as e:
        print("[-] An error occurred:", e)


if __name__ == "__main__":
    print("###")
    print("### Welcome to ./elf-crackme-level2.2!")
    print("###")
    print("")
    print("Original .text hash is ba4f77d33e8961855bda04916d50f802")
    print("We changed two bytes in the .text segment to 0x9090. Please try to find")
    print(
        "and crack the original result. After completing the repair, execute the check function to get the flag."
    )
    while True:
        print("Select the action you want to perform:")
        print("1. Modify the ELF file")
        print("2. Check the repaired content")
        print("3. Exit")

        choice = input("Enter the option number: ")

        if choice == "1":
            patch()
        elif choice == "2":
            check()
        elif choice == "3":
            print("The program has exited.")
            break
        else:
            print("Invalid option, please enter again.")
