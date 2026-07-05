import requests
from bs4 import BeautifulSoup
import csv

def scrape_quotes(url, output_file):
    print(f"Connecting to {url}...")

    try:
        # Timeout add kiya - 10 sec me response nahi aaya to error
        response = requests.get(url, timeout=10)

        # 200 ke alawa koi bhi status = problem
        if response.status_code != 200:
            print(f"Error: Website ne response diya {response.status_code}")
            print("Website down ho sakti hai ya URL galat hai.")
            return

    except requests.exceptions.ConnectionError:
        print("Error: Internet connection nahi hai ya website accessible nahi hai.")
        return
    except requests.exceptions.Timeout:
        print("Error: Website ne 10 seconds me response nahi diya. Try karo baad me.")
        return
    except Exception as e:
        print(f"Unexpected error while connecting: {e}")
        return

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.find_all('div', class_='quote')

        if not quotes:
            print("Warning: Koi quotes nahi mile. Website ka structure change ho gaya hoga.")
            return

        with open(output_file, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(['Quote', 'Author', 'Tags'])

            saved = 0
            for quote in quotes:
                try:
                    text = quote.find('span', class_='text').get_text()
                    author = quote.find('small', class_='author').get_text()
                    tag_list = quote.find_all('a', class_='tag')
                    tags = ', '.join([tag.get_text() for tag in tag_list])

                    writer.writerow([text, author, tags])
                    print(f"Saved: {author}")
                    saved += 1

                except AttributeError:
                    print("Warning: Ek quote ka structure different tha, skip kiya.")
                    continue

        print("------------------------------")
        print(f"Total {saved} quotes saved in '{output_file}'")

    except PermissionError:
        print(f"Error: '{output_file}' already open hai Excel me. Band karo pehle.")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Run karo
scrape_quotes("http://quotes.toscrape.com", "quotes.csv")