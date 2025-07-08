# 2GIS Dynamic Search Scraper - Private Tool Overview

---

## About

This project contains a proprietary Python tool designed for advanced scraping of business listings and contact details from the 2GIS website, focusing on dynamic, JavaScript-rendered search results.

The tool leverages automated browser control through Selenium WebDriver to navigate listings, paginate through all search results, and extract detailed contact information — including phone numbers and WhatsApp contacts — with high accuracy and reliability.

---

## Key Functionalities

- **Region & Query Based Search:** Provides flexibility to perform targeted searches by region (city/area) and keyword (e.g., "restaurants", "shops").

- **Full Pagination Handling:** Automatically detects and traverses all result pages, ensuring comprehensive collection of firm identifiers.

- **Contact Information Scraping:** For each collected firm, the tool navigates to their detailed profile, scrolling relevant content dynamically to load phone numbers and WhatsApp contact links.

- **WhatsApp Number Decoding:** Includes logic to decode Base64-encoded WhatsApp links embedded in the site’s URLs, enabling retrieval of direct WhatsApp phone numbers even if obscured.

- **Result Compilation:** Aggregates all collected phone and WhatsApp contacts in a clean, readable text file organized by firm ID.

---

## Intended Use & Benefits

This tool is intended **strictly for internal security research and analysis purposes**, aimed at:

- **Assessing 2GIS’s Parsing Security:** By simulating automated scraping activities, the tool helps identify vulnerabilities or potential weaknesses in how 2GIS exposes and protects contact data.

- **Improving Website Robustness:** Insights gained can inform 2GIS developers to enhance anti-scraping techniques, dynamic content protection, or API security measures.

- **Competitive Intelligence & Market Analysis:** Allows authorized users to quickly gather business contact data relevant to specific regions and sectors, facilitating market research or outreach campaigns.

- **Demonstrating Automation Technical Capabilities:** Showcases advanced automated interaction with JavaScript-heavy web pages, useful for broader data extraction challenges.

---

## Ethical Notice & Usage Restrictions

- This tool contains sensitive automation techniques designed to mimic human browsing behavior.

- The source code is **proprietary and confidential**, and is **not distributed publicly** to prevent misuse or unauthorized duplication.

- Usage is restricted to authorized personnel for **security improvement purposes only**.

- Users must comply with all applicable laws, website terms of service, and ethical guidelines when deploying scraping technologies.

- Please contact the appropriate security teams before attempting any data extraction on live platforms you do not own.

---

## How the Tool Works (Conceptual Overview)

1. **User Inputs:** Region code and search term entered interactively.

2. **Automated Browser Launch:** Opens a visible Chrome browser instance with customized options for seamless scraping.

3. **Page Navigation & Firm ID Collection:** Visits search results, waits for page elements to load completely, and iteratively collects unique firm IDs from all paginated search results.

4. **Contact Extraction:** For each firm, visits the profile page, scrolls contact panels to force dynamic loading, and extracts phone numbers and decoded WhatsApp links.

5. **Data Output:** Compiles all collected information into a timestamped text file with a structured summary.

---

## Technical Environment

- Written in **Python 3**.

- Uses **Selenium WebDriver** with ChromeDriver managed via `webdriver-manager`.

- Handles dynamic, JS-rendered content using explicit waits and JavaScript execution.

- Decodes obfuscated contact links (Base64 encoded WhatsApp URLs).

---

## Conclusion

This scraper tool is a sophisticated internal asset designed to support security testing and enhance data protection on the 2GIS platform.

By carefully benchmarking and demonstrating scraping methods, it helps ensure that contact information exposure aligns with privacy and security best practices — ultimately improving user trust and platform integrity.

---

*For further information or access, please contact the author internally. Unauthorized copying or distribution is prohibited.*
