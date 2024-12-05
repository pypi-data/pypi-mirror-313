# **secfi Library**
**secfi** is a free Python library made to simplify access to SEC (U.S. Securities and Exchange Commission) filings and perform basic web scraping of the retrieved documents

- [Installation](#installation)
- [Features](#features)
  - [1. `getCiks`](#1-getciks)
  - [2. `getFils`](#2-getfils)
  - [3. `scrapLatest`](#3-scraplatest)
  - [4. `scrap`](#4-scrap)
  - [5. `secForms`](#5-secforms)
- [Notes](#notes)
- [License](#license)

<br>

___

<br>
Ypu can try this in free colab:

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1D5luJcWHL_Y7hGw781csspIfZdOhPHZ7?usp=sharing)


<br>
<br>
## Installation

```bash
pip install secfi
```
<br>


## Features

### <a name="1-getciks"></a>1. `getCiks()`
Fetches a DataFrame of all company tickers and their corresponding Central Index Keys (CIKs).

```python
import secfi

ciks = secfi.getCiks()
print(ciks.head())
```

**Returns:**
A DataFrame with columns:
- `cik_str` – The raw CIK string.
- `title` – The company name.
- `cik` – The CIK padded to 10 digits (for SEC queries).

```
| ticker | cik_str  | title                       | cik        |
|--------|----------|-----------------------------|------------|
| NVDA   | 1045810  | NVIDIA CORP                 | 0001045810 |
| AAPL   | 320193   | Apple Inc.                  | 0000320193 |
| MSFT   | 789019   | MICROSOFT CORP              | 0000789019 |
| AMZN   | 1018724  | AMAZON COM INC              | 0001018724 |
| GOOGL  | 1652044  | Alphabet Inc.               | 0001652044 |
| ...    | ...      | ...                         | ...        |
```
<br>



### <a name="2-getfils"></a>2. `getFils(ticker: str)`
Fetches recent filings for a specific company by its ticker.

```python
import secfi

filings = secfi.getFils("AAPL")
print(filings.head())
```

**Parameters:**
- `ticker` (str): The company's ticker symbol.

**Returns:**
A DataFrame like:

```
| filingDate | reportDate | form    | filmNumber | size    | isXBRL | url          |
|------------|------------|---------|------------|---------|--------|--------------|
| 2024-11-01 | 2024-09-30 | 10-Q    | 241416538  | 9185722 | 1      | sec.gov/...  |
| 2024-08-02 | 2024-06-30 | 10-Q    | 241168331  | 8114974 | 1      | sec.gov/...  |
| 2024-05-01 | 2024-03-31 | 10-Q    | 24899170   | 7428154 | 1      | sec.gov/...  |
| 2024-04-11 | 2024-05-22 | DEF 14A | 24836785   | 8289378 | 1      | sec.gov/...  |
| 2024-02-02 | 2023-12-31 | 10-K    | 24588330   | 12110804| 1      | sec.gov/...  |
| 2023-10-27 | 2023-09-30 | 10-Q    | 231351529  | 7894342 | 1      | sec.gov/...  |
| ...        | ...        | ...     | ...        | ...     | ...    | ...          |
```
<br>



### <a name="3-scraplatest"></a>3. `scrapLatest(ticker: str, form: str)`
Retrieves the textual content of the latest SEC filing of a specific form type for a given ticker.

<!-- 
The SEC provides 165 different types of forms that can be referenced for regulatory purposes. 
You can find a complete list of these forms in the following CSV file on GitHub:
-->

The SEC provides **165 different types of forms**. You can find the complete list in the following CSV file:

[SEC Forms CSV](https://github.com/gauss314/secfi/blob/main/info/sec_forms.csv)

#### 10 Most Common Forms for Public Companies:
1. **10-K**: Annual report that provides a comprehensive overview of the company's business and financial condition.
2. **10-Q**: Quarterly report that includes unaudited financial statements and provides a continuing view of the company's financial position.
3. **8-K**: Report used to announce major events that shareholders should know about (e.g., acquisitions, leadership changes).
4. **S-1**: Registration statement for companies planning to go public with an initial public offering (IPO).
5. **S-3**: Registration statement for secondary offerings or resales of securities.
6. **DEF 14A**: Proxy statement used for shareholder meetings, including executive compensation and voting matters.
7. **4**: Statement of changes in beneficial ownership (insider trading disclosures).
8. **3**: Initial statement of beneficial ownership of securities (insider ownership).
9. **6-K**: Report submitted by foreign private issuers to disclose information provided to their home country's regulators.
10. **13D**: Filing by anyone acquiring more than 5% of a company's shares, detailing their intentions.

#### 10 Most Common Forms for Foreign Companies:
1. **6-K**: Quarterly or event-specific report submitted by foreign private issuers, serving a similar role to the 10-Q for U.S. companies.
2. **20-F**: Annual report for foreign private issuers, equivalent to the 10-K for U.S. companies.
3. **40-F**: Annual report filed by certain Canadian companies under the U.S.-Canada Multijurisdictional Disclosure System.
4. **F-1**: Registration statement for foreign companies planning an initial public offering (IPO) in the U.S.
5. **F-3**: Registration statement for foreign companies conducting secondary offerings in the U.S.
6. **F-4**: Registration statement for mergers, acquisitions, or business combinations involving foreign companies.
7. **CB**: Filing required for tender offers, rights offerings, or business combinations involving foreign private issuers.
8. **13F**: Quarterly report by institutional investment managers disclosing equity holdings, applicable to some foreign firms.
9. **11-K**: Annual report for employee stock purchase, savings, and similar plans for foreign issuers.
10. **SD**: Specialized disclosure report, often related to conflict minerals, applicable to foreign private issuers with U.S. reporting obligations.

#### Example

```python
import secfi

secfi.scrapLatest("NVDA", "10-Q")
```

#### Example Output

When calling the `scrapLatest("NVDA", "10-Q")` function, the returned dictionary might look like this:

<pre>
{
    'filingDate': '2024-11-27',
    'reportDate': '2024-11-25',
    'form': '4',
    'filmNumber': '',
    'size': 4872,
    'isXBRL': 0,
    'url': 'https://www.sec.gov/Archives/edgar/data/0001045810/000104581024000318/xslF345X05/wk-form4_1732744744.xml',
    'acceptanceDateTime': '2024-11-27T16:59:12.000Z',
    'text': 'STATESSECURITIES AND EXCHANGE COMMISSIONWashington, D.C.\nFor the quarterly period ended October, 2024 OR TRANSITION REPORT PURSUANT TO SECTION 13 OR 15(d) OF THE SECURITIES EXCHANGE ACT OF 1934Commission File Number: 0-23985 NVIDIA CORPORATION(Exact name of registrant as specified in its charter) Delaware94-3177549(State or other jurisdiction of(I.R.S. Employerincorporation or organization)Identification No.)2788 San Tomas Expressway, Santa Clara, California95051(Address\xa0of principal executive offices)(Zip Code)(408) 486-2000 ....'
}
</pre>

**Parameters:**
- `ticker` (str): The company's ticker symbol.
- `form` (str): The form type to retrieve (e.g., "10-K", "8-K").

**Returns:**

dict: A dictionary containing details of the filing, including:
- `filingDate` (str): The date the filing was submitted
- `reportDate` (str): The reporting period date
- `form` (str): The type of SEC form (e.g., '10-K', '10-Q')
- `filmNumber` (str): The film number associated with the filing
- `size` (int): The size of the filing in bytes
- `isXBRL` (int): Whether the filing is in XBRL format (1 for yes, 0 for no)
- `url` (str): The URL of the filing
- `text` (str): The text content of the filing if found and successfully scraped
                Otherwise, an empty string

If the specified form is not found for the given ticker, returns an empty dictionary

<br>



### <a name="4-scrap"></a>4. `scrap(url: str, timeout: int = 15)`
Scrapes the textual content of a given URL.

```python
content = secfi.scrap("https://example.com")
print(content[:500])  # Preview the first 500 characters
```

**Parameters:**
- `url` (str): The URL to scrape.
- `timeout` (int): Timeout for the HTTP request (default is 15 seconds).

**Returns:**
The cleaned text content of the URL or an error message if the request fails.

<br>



### <a name="5-secforms"></a>1. `secForms()`
Fetches a DataFrame of SEC forms and their details from the `sec_forms.csv` file located in the `info` directory.

```python
import secfi

sec_forms = secfi.secForms()
print(sec_forms.head())
```

**Returns:**
A DataFrame with columns:
- `Number` – The unique identifier for the form.
- `Description` – A brief description of the form.
- `Last Updated` – The last updated date of the form.
- `SEC Number` – The SEC-assigned identifier for the form.
- `Topic(s)` – Relevant topics associated with the form.
- `link` – A direct URL to the PDF version of the form.


| Number | Description                                        | Last Updated | SEC Number | Topic(s)                                         | link                                      |
|--------|----------------------------------------------------|--------------|------------|------------------------------------------------|------------------------------------------|
| 1      | Application for registration or exemption from... | Feb. 1999    | SEC1935    | Self-Regulatory Organizations                  | [PDF](https://www.sec.gov//files/form1.pdf) |
| 1-A    | Regulation A Offering Statement (PDF)             | Sept. 2021   | SEC486     | Securities Act of 1933, Small Businesses       | [PDF](https://www.sec.gov//files/form1a.pdf) |
| 1-E    | Notification under Regulation E (PDF)             | Aug. 2001    | SEC1807    | Investment Company Act of 1940, Small Busin... | [PDF](https://www.sec.gov//files/form1-e.pdf) |
| ...    | ...                                                | ...          | ...        | ...                                            | ...                                       |


<br>


## Notes
- The library uses a custom `User-Agent` to comply with SEC API requirements.
- Ensure that requests to the SEC website respect their usage policies and rate limits.

## License
This project is open source and available under the MIT License.




