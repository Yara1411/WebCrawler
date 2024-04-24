# Python Web Crawler

## Description

This Python Web Crawler is designed to efficiently navigate websites starting from a given root URL and depth(the number of “clicks” away from the home page).
It uses concurrent programming to fetch URLs and parse their HTML content to identify links and images.
The crawler checks for broken links and duplicate images by hashing image data.
It aims to help users audit websites for link validity and image redundancy up to a specified depth of navigation.

## Features

- Concurrent URL fetching using ThreadPoolExecutor.
- Parsing of HTML content to extract links and images.
- Detection of broken links and duplicate images.
- Outputs results to text files, including link depths and issues found.

## Before Installation

Ensure you have Python and Git installed on your computer:

- **Python**: [Install Python](https://www.python.org/downloads/)
- **Git**: [Install Git](https://git-scm.com/downloads)

## Setup

1. Clone the repository:
   git clone https://github.com/Yara1411/WebCrawler
2. Navigate to the project directory:
   cd path/to/WebCrawler

## Installation

Install virtualenv and create a virtual environment:

1. pip install virtualenv
2. virtualenv myenv
3. source myenv/bin/activate

Install the required dependencies: pip install -r requirements.txt

## Running the program

To run the Web Crawler, use the following command:
python3 WebCrawler.py https://website.com depth

## Requirements

- Python 3.6 or higher
- Compatible with MacOS, Linux, and Windows operating systems.
