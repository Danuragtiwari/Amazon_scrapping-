import csv
import requests
from bs4 import BeautifulSoup

def scrape_amazon_products():
    # Send a GET request to the Amazon page
    url = "https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar"
    response = requests.get(url)

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the product items on the page
    product_items = soup.find_all("div", {"data-component-type": "s-search-result"})

    # Create a CSV file to store the scraped data
    with open("amazon_products.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Product Name", "Price", "Rating", "Seller Name"])

        # Iterate over each product item and extract the details
        for item in product_items:
            # Extract the product name
            product_name = item.find("span", class_="a-text-normal").text.strip()
            # Extract the price
            price_element = item.find("span", class_="a-price-whole")
            price = price_element.text.strip() if price_element else "N/A"

            # Extract the rating
            rating_element = item.find("span", class_="a-icon-alt")
            rating = rating_element.text.strip() if rating_element else "N/A"
            #Extract the seller  details
            seller_element = item.find("a")["href"]
            #Extract the url for the seller
            url_seller='https://www.amazon.in/{}'.format(seller_element)
            #
            response_seller = requests.get(url_seller)

            
            soup_seller = BeautifulSoup(response_seller.content, "html.parser")
            
            product_items_for_seller = soup_seller.find("div",  { "id" :"availability"})
            #
            if product_items_for_seller==None:
                continue
            stock_check =product_items_for_seller.find("span", class_="a-size-medium a-color-success").text.strip()
            if stock_check =='In stock':
                seller_details=soup_seller.find("div",{"id":"merchant-info"})
                
                seller_span_tags=seller_details.find_all('span')
                seller_name=seller_span_tags[1].text.strip()
                
                
                # Write the data to the CSV file
                writer.writerow([product_name, price, rating, seller_name])
                
            


    print("Scraping completed. The data has been saved to 'amazon_products.csv'.")

scrape_amazon_products()
