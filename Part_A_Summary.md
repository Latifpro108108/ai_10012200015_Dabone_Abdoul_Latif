# Part A Summary – Data Preparation
**Student:** Dabone Abdoul Latif  
**Index:** 10012200015  
**Course:** CS4241 - Introduction to Artificial Intelligence  
**Lecturer:** Godwin N. Danso  

---

## What We Did

Part A was about getting the two datasets ready before we could build the chatbot. The two datasets are:
- **Ghana Election Results** (CSV file)
- **Ghana 2025 Budget Statement** (PDF file)

---

## Step 1 – Cleaning the CSV

We loaded the file using pandas and checked for problems.

**Problems we found:**
- The `Votes(%)` column had a `%` sign attached to the numbers (e.g. `55.04%`) which meant Python could not treat it as a number
- The `Votes` column was stored as text, not a number
- Some region names had a hidden character called a non-breaking space (`\xa0`) that looks like a space but is not
- There were no missing values, but we still added `fillna(0)` as a safety measure in case any null values appeared after conversion

**What we fixed:**
- Removed the `%` sign and converted `Votes(%)` to a float
- Converted `Votes` to an integer
- Replaced `\xa0` with a normal space in region names
- Filled any nulls with 0 instead of dropping rows

After cleaning we had **615 rows**, all valid.

---

## Step 2 – Cleaning the PDF

We used PyMuPDF (fitz) to read the PDF page by page.

**Problems we found:**
- Some pages were blank (cover pages, dividers) — these add nothing useful
- Every page had the same header text repeated: *"Resetting the Economy for the Ghana We Want"* and *"2025 Budget"* — this noise would confuse the search later
- Some special characters (like arrows and math symbols) caused encoding errors on Windows

**What we fixed:**
- Skipped pages with less than 50 characters (blank pages)
- Removed the repeated header lines using `.replace()`
- Stripped non-ASCII characters using `.encode('ascii', errors='ignore')`

After cleaning we had about **91,000 words** of usable text.

---

## Step 3 – Chunking

### What is a chunk?
A chunk is a small piece of text. Instead of searching the whole document at once, we break it into smaller pieces and search those. This makes it faster and more accurate.

### What is overlap?
Overlap means we repeat a few words at the start of the next chunk. This way, if an important sentence falls on the boundary between two chunks, it still appears fully in at least one of them.

**Example:**
```
Words:   A B C D E F G H
Chunk 1: A B C D E
Chunk 2:     C D E F G H   ← C D E are repeated (overlap)
```

### Two strategies we tested

| Strategy | Chunk Size | Overlap | PDF Chunks Created |
|---|---|---|---|
| Small | 100 words | 20 words | 1,144 |
| Large | 300 words | 50 words | 366 |

### Which one we chose and why

We chose **large chunks (300 words, 50 overlap)** for the PDF.

The budget document is written in long paragraphs. A 100-word chunk often cuts a paragraph in the middle, which removes the context needed to understand it. With 300 words, the chatbot gets enough surrounding text to give a proper answer.

For the CSV we used **1 row = 1 chunk**. Each row is already one complete fact (candidate, party, votes, region, year) — there is no reason to merge rows together.

---

## Output

At the end of Part A we saved two files:
- `chunks/csv_chunks.json` — 615 chunks from the election data
- `chunks/pdf_chunks.json` — 366 chunks from the budget document

These files are used directly in Part B to create the embeddings and build the search index.
