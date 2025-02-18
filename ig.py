import os
import sys
import requests
import json
from datetime import datetime

def banner():
    print("""\033[1;36m
    ██╗ ██████╗        ██████╗ ███████╗██╗███╗   ██╗████████╗
    ██║██╔════╝       ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝
    ██║██║  ███╗█████╗██║   ██║███████╗██║██╔██╗ ██║   ██║   
    ██║██║   ██║╚════╝██║   ██║╚════██║██║██║╚██╗██║   ██║   
    ██║╚██████╔╝      ╚██████╔╝███████║██║██║ ╚████║   ██║   
    ╚═╝ ╚═════╝        ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   
                                                         
    \033[0m""")
    print("\033[1;32m[+] Instagram OSINT Tool [+]\033[0m")
    print("\033[1;32m[+] Version: 1.0 [+]\033[0m")
    print("\033[1;32m[+] Author: Claw4u [+]\033[0m")
    print()

def download_stories(username):
    print(f"\n\033[1;32m[+] Downloading stories for {username}...\033[0m")
    
    # Create directory for stories if it doesn't exist
    if not os.path.exists(f"downloads/{username}/stories"):
        os.makedirs(f"downloads/{username}/stories")
    
    # Note: In a real implementation, you would need to use Instagram API or a third-party library
    # This is a placeholder for the actual implementation
    try:
        # Simulating story API call
        # In a real implementation, you would use instaloader or another library
        print("\033[1;33m[!] Fetching user stories...\033[0m")
        
        # Simulate download process
        print("\033[1;32m[+] Found 5 stories\033[0m")
        for i in range(1, 6):
            print(f"\033[1;32m[+] Downloading story {i}/5...\033[0m")
            # Simulate download delay
            time.sleep(1)
            
        print(f"\n\033[1;32m[+] Successfully downloaded stories to downloads/{username}/stories\033[0m")
    except Exception as e:
        print(f"\033[1;31m[-] Error downloading stories: {str(e)}\033[0m")
    
    input("\n\033[36mPress Enter to go back to the menu...\033[0m")

def download_highlights(username):
    print(f"\n\033[1;32m[+] Downloading highlights for {username}...\033[0m")
    
    # Create directory for highlights if it doesn't exist
    if not os.path.exists(f"downloads/{username}/highlights"):
        os.makedirs(f"downloads/{username}/highlights")
    
    # Note: In a real implementation, you would need to use Instagram API or a third-party library
    # This is a placeholder for the actual implementation
    try:
        # Simulating highlights API call
        print("\033[1;33m[!] Fetching user highlights...\033[0m")
        
        # Simulate fetching highlight IDs
        print("\033[1;32m[+] Found 3 highlight collections\033[0m")
        highlight_names = ["Travel", "Food", "Friends"]
        
        for i, name in enumerate(highlight_names):
            print(f"\033[1;32m[+] Downloading highlight collection: {name}\033[0m")
            # Create directory for each highlight collection
            if not os.path.exists(f"downloads/{username}/highlights/{name}"):
                os.makedirs(f"downloads/{username}/highlights/{name}")
            
            # Simulate downloading highlight items
            num_items = 3  # Simulated number of items per highlight
            for j in range(1, num_items + 1):
                print(f"\033[1;32m[+] Downloading item {j}/{num_items} from {name}...\033[0m")
                # Simulate download delay
                time.sleep(0.5)
            
        print(f"\n\033[1;32m[+] Successfully downloaded highlights to downloads/{username}/highlights\033[0m")
    except Exception as e:
        print(f"\033[1;31m[-] Error downloading highlights: {str(e)}\033[0m")
    
    input("\n\033[36mPress Enter to go back to the menu...\033[0m")

def options_menu(username):
    print(f"\n\033[1;32m[+] Target: @{username}\033[0m\n")
    print("\033[1;33m[1] Get User Information\033[0m")
    print("\033[1;33m[2] Download Profile Picture\033[0m")
    print("\033[1;33m[3] Download Stories\033[0m")  # New option
    print("\033[1;33m[4] Download Highlights\033[0m")  # New option
    print("\033[1;33m[5] Change Username\033[0m")
    print("\033[1;33m[6] Help\033[0m")
    print("\033[1;33m[7] Exit\033[0m")
    
    choice = input("\n\033[36mEnter your choice: \033[0m")
    
    if choice == "1":
        # Placeholder for get_user_info function
        print("\033[1;32m[+] Getting user information...\033[0m")
        input("\n\033[36mPress Enter to go back to the menu...\033[0m")
        os.system('cls' if os.name == 'nt' else 'clear')
        banner()
        options_menu(username)
    elif choice == "2":
        # Placeholder for download_profile_pic function
        print("\033[1;32m[+] Downloading profile picture...\033[0m")
        input("\n\033[36mPress Enter to go back to the menu...\033[0m")
        os.system('cls' if os.name == 'nt' else 'clear')
        banner()
        options_menu(username)
    elif choice == "3":
        os.system('cls' if os.name == 'nt' else 'clear')
        banner()
        download_stories(username)
        os.system('cls' if os.name == 'nt' else 'clear')
        banner()
        options_menu(username)
    elif choice == "4":
        os.system('cls' if os.name == 'nt' else 'clear')
        banner()
        download_highlights(username)
        os.system('cls' if os.name == 'nt' else 'clear')
        banner()
        options_menu(username)
    elif choice == "5":
        username = input("\n\033[36mEnter new Instagram username: \033[0m")
        input("\n\033[36mUsername changed successfully. Press Enter to go back to the menu...\033[0m")
        os.system('cls' if os.name == 'nt' else 'clear')
        banner()
        options_menu(username)
    elif choice == "6":
        os.system('cls' if os.name == 'nt' else 'clear')
        banner()
        # Placeholder for open_help function
        print("\033[1;32m[+] Help Menu\033[0m")
        print("\033[1;33m[1] Get User Information - Retrieves basic profile data\033[0m")
        print("\033[1;33m[2] Download Profile Picture - Saves profile image to local directory\033[0m")
        print("\033[1;33m[3] Download Stories - Downloads active stories\033[0m")
        print("\033[1;33m[4] Download Highlights - Downloads highlight collections\033[0m")
        print("\033[1;33m[5] Change Username - Switch target account\033[0m")
        print("\033[1;33m[6] Help - Shows this menu\033[0m")
        print("\033[1;33m[7] Exit - Quits the program\033[0m")
        input("\n\033[36mPress Enter to go back to the menu...\033[0m")
        os.system('cls' if os.name == 'nt' else 'clear')
        banner()
        options_menu(username)
    elif choice == "7":
        print("\033[1;31mExiting...\033[0m")
        sys.exit()
    else:
        print("\033[1;31mInvalid choice. Please try again.\033[0m")
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        banner()
        options_menu(username)

def main():
    # Import here to avoid circular imports
    import time
    
    os.system('cls' if os.name == 'nt' else 'clear')
    banner()
    username = input("\n\033[36mEnter Instagram username: \033[0m")
    
    # Create downloads directory structure
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    if not os.path.exists(f"downloads/{username}"):
        os.makedirs(f"downloads/{username}")
    
    os.system('cls' if os.name == 'nt' else 'clear')
    banner()
    options_menu(username)

if __name__ == "__main__":
    main()