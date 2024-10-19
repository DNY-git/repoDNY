import requests
import sys
import time
import threading

API_KEY = "13e20394bb9a408fa70a1e37a4732b92"

# Global variable to control the spinner thread
spinner_running = True

def fetch_news(category):
    url = f"https://newsapi.org/v2/top-headlines?category={category}&country=us&apiKey={API_KEY}"

    global spinner_running
    spinner_running = True  # Start the spinner

    # Start the spinner in a separate thread
    spinner_thread = threading.Thread(target=spinner)
    spinner_thread.start()

    response = requests.get(url)
    
    # Stop the spinner after receiving the response
    stop_spinner()

    if response.status_code == 200:
        articles = response.json().get("articles")
        if articles:
            return articles
        else:
            print("No news found for the selected category.")
            return []
    elif response.status_code == 401:
        print("Unauthorized: Invalid API key.")
        return []
    elif response.status_code == 404:
        print("Not Found: The requested resource was not found.")
        return []
    else:
        print(f"Error fetching news. HTTP Status Code: {response.status_code}")
        return []

def spinner():
    while spinner_running:
        for cursor in '|/-\\':
            sys.stdout.write(f'\r\033[31mFetching news... {cursor}\033[0m')  # Fetching message in red with spinner
            sys.stdout.flush()
            time.sleep(0.1)

def stop_spinner():
    global spinner_running
    spinner_running = False  # Stop the spinner
    sys.stdout.write('\r\033[0m                          \033[0m')  # Clear the fetching line
    sys.stdout.flush()

def display_articles(articles):
    if not articles:
        print("No articles to display.")
        return

    for i, article in enumerate(articles, start=1):
        title = article.get("title")
        description = article.get("description")

        # Display article title with a delay
        print(f"\033[34m{i}. {title}\033[0m")  # Article titles in blue
        if description:
            print(f"   Description: {description}")

        # Wait for 3 seconds before displaying the next article
        if i < len(articles):  # Avoid waiting after the last article
            print("\033[31mFetching next article...\033[0m")  # Message in red
            time.sleep(3)  # Wait for 3 seconds before showing the next article
        print()  # Add a newline for better readability

    # After all articles are displayed, ensure no spinner or fetching message is shown
    stop_spinner()  # Stop spinner if still running
    print("\033[0mFinished displaying all articles.\033[0m")  # Indicate that all articles have been shown

def print_banner():
    banner = r"""
\033[33m  _____    _       _           
 |  ___|__| |_ ___| |__  _ __  
 | |_ / _ \ __/ __| '_ \| '__| 
 |  _|  __/ || (__| | | | |    
 |_|  \___|\__\___|_| |_|_|    
                               
  \033[31m__
                               _.-~  )
                    _..--~~~~,'   ,-/     _
                 .-'. . . .'   ,-','    ,' )
               ,'. . . _   ,--~,-'__..-'  ,'
             ,'. . .  (@)' ---~~~~      ,'
            /. . . . '~~             ,-'
           /. . . . .             ,-'
          ; . . . .  - .        ,'
         : . . . .       _     /
        . . . . .          `-.:
       . . . ./  - .          )
      .  . . |  _____..---.._/ ____ Seal _
~---~~~~----~~~~             ~~\033[0m
    """
    print(banner)

def print_categories():
    categories = [
        "business",
        "entertainment",
        "general",
        "health",
        "science",
        "sports",
        "technology"
    ]
    print("\033[33mSelect news category (choose a number or enter 0 to exit):\033[0m")  # Prompt in yellow
    for i, category in enumerate(categories, start=1):
        print(f"\033[35m{i}.\033[0m \033[32m{category}\033[0m")  # Numbers in purple and category names in green
    print("\033[35m0. Exit\033[0m")  # Exit option in purple

def main():
    print_banner()
    
    while True:
        print_categories()
        
        # Get user input for category selection
        try:
            choice = int(input("\033[33mEnter your choice: \033[0m"))  # Prompt in yellow
            if choice == 0:
                print("\033[34mExiting the bot. Goodbye!\033[0m")
                break
            elif 1 <= choice <= 7:
                category = ["business", "entertainment", "general", "health", "science", "sports", "technology"][choice - 1]
                articles = fetch_news(category)
                display_articles(articles)
            else:
                print("\033[31mInvalid choice. Please select a number between 0 and 7.\033[0m")
        except ValueError:
            print("\033[31mPlease enter a valid number.\033[0m")

if __name__ == "__main__":
    main()
