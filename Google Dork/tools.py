import argparse
from urllib.parse import urlparse
from googlesearch import search
from fake_useragent import UserAgent
import requests
import time
from tqdm import tqdm


def google_search(query, num_results=5, delay=1):
    search_results = []
    # headers = {}
    # user_agent = UserAgent()
    # headers["User-Agent"] = user_agent.random
    for url in tqdm(search(query, num_results=num_results), desc="Sedang Diproses....", unit="URL"):
        search_results.append(url)
        time.sleep(delay)

    return search_results

def extract_domain(url, include_path=True):
    parsed_url = urlparse(url)
    if include_path:
        return parsed_url.netloc + parsed_url.path
    else:
        return parsed_url.netloc

def domain_only(results):
    
    for url in results:
        domain = extract_domain(url, include_path=False)
        return domain

def save_results_to_txt(results, file_path):
    with open(file_path, "w") as file:
        for url in results:
            file.write(url + "\n")

def main():
    parser = argparse.ArgumentParser(description="Google Search Scraper")
    parser.add_argument("query", help="Kueri pencarian")
    parser.add_argument("--num-results", type=int, default=5, help="Jumlah hasil pencarian (default: 5)")
    parser.add_argument("--output-file", help="Nama file untuk menyimpan hasil")
    parser.add_argument("--domain-only", action="store_true", help="Hanya ambil nama domain tanpa path")
    
    args = parser.parse_args()

    results = google_search(args.query, num_results=args.num_results)

    if args.output_file:
        
        if args.domain_only:
            domain = domain_only(results)
            save_results_to_txt(domain, args.output_file)
            print(f"Hasil pencarian disimpan dalam file {args.output_file}")

        else:
            save_results_to_txt(results, args.output_file)
            print(f"Hasil pencarian disimpan dalam file {args.output_file}")



    else:
        
        if args.domain_only:
            for url in results:
                domain = extract_domain(url, include_path=False)
                print(domain)
        else:
            for url in results:
                print(url)



if __name__ == "__main__":
    main()