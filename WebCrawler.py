
import sys
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin
from queue import Queue
import multiprocessing
import validators
import hashlib

class WebCrawler:
    def __init__(self, root_url, max_depth = 3):
        self.max_depth = max_depth
        self.visited = set()
        self.to_visit = Queue()
        self.to_visit.put((root_url, 0))
        self.broken_links = set()
        self.links_info = {}
        self.image_hashes = {}
        self.duplicate_images = set()
        
    @staticmethod
    def fetch_url(url):
        try:
            response = requests.get(url, timeout=25)  
            response.raise_for_status()  
            
            return response.text, None  
        except requests.RequestException as e:
            return None, str(e) 
        except ValueError as valueError: 
            return None, str(valueError)

    @staticmethod
    def fetch_and_hash_image(url):
        try:
            response = requests.get(url, timeout=25)
            response.raise_for_status()
            image_data = response.content
            hash_obj = hashlib.md5() 
            hash_obj.update(image_data) 
            return hash_obj.hexdigest()
        except requests.RequestException:
            return None
        
    @staticmethod
    def parse_links(html, root_url):
        soup = BeautifulSoup(html, 'html.parser')  
        links = {urljoin(root_url, tag.get('href')) for tag in soup.find_all('a', href=True)}  
        images = {urljoin(root_url, img.get('src')) for img in soup.find_all('img', src=True)}
        return links, images
    
    
    def check_for_duplicate_images(self, image_url):
        hash_val = WebCrawler.fetch_and_hash_image(image_url) 
        if hash_val:
            if hash_val in self.image_hashes:
                self.duplicate_images.add(image_url)
            else:
                self.image_hashes[hash_val] = image_url


    def fetch_and_process_url(self, url, depth):
        html, error = WebCrawler.fetch_url(url)
        if error:
            self.broken_links.add(url)
        else:
            self.links_info[url] = depth
            if depth < self.max_depth:
                new_links, image_urls = WebCrawler.parse_links(html, url)
                for img_url in image_urls:
                    self.check_for_duplicate_images(img_url)
                for link in new_links:
                    if link not in self.visited:
                        self.to_visit.put((link, depth + 1))


    def crawl(self):
        with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
            futures_set = set()
            while not self.to_visit.empty() or futures_set:
                if not self.to_visit.empty(): 
                    url, depth = self.to_visit.get()
                    if url not in self.visited:
                        self.visited.add(url)
                        future = executor.submit(self.fetch_and_process_url, url, depth) 
                        futures_set.add(future)
                        future.add_done_callback(futures_set.discard) 

           
        return self.links_info, self.broken_links, self.duplicate_images


def write_result_to_file(links_info, broken_links, duplicate_images, file_name="output.txt", file_dup="duplicate_images.txt"):
    with open(file_name, "w") as file:
        file.write("============= Links and Depths =============\n")
        for link, depth in links_info.items(): 
            file.write(f"URL: {link} --- Depth [{depth}]\n")
            
        file.write("\n\n============= Broken Links =================\n")
        for link in broken_links: 
            file.write(f"{link}\n")
    with open(file_dup, "w") as file:
        file.write("\n============= Duplicate Images =================\n")
        for image in duplicate_images:
            file.write(f"{image}\n")

    print("Done check your file")


def validate_and_get_input():
    if (len(sys.argv) < 2 or not validators.url(sys.argv[1])):
        print("Invalid URL input")
        sys.exit(0)

    max_depth = 3

    if (len(sys.argv) > 2) and (sys.argv[2].isdigit()):
        max_depth = int(sys.argv[2])
    else:
        print("No depth was chosen, default depth = 3")

    return sys.argv[1], max_depth


if __name__ == "__main__":
    root_url, max_depth = validate_and_get_input()
    crawler = WebCrawler(root_url, max_depth)
    links_info, broken_links, duplicate_images = crawler.crawl()
    write_result_to_file(links_info, broken_links, duplicate_images)