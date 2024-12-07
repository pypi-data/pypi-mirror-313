# CleanSort Library

A simple and powerful library that helps you clean and organize metadata from websites.

## What is this library for?

This library helps you:
1. Take messy website metadata (like information about books, articles, or journals)
2. Clean it up by keeping only the important parts (like titles, authors, ISBN numbers)
3. Organize it neatly by category
4. Store it in a database for later use

## Step-by-Step Installation Guide

### For Users (Using the Library)

1. Make sure you have Python installed (version 3.7 or higher):
   - Go to https://www.python.org/downloads/
   - Download and install Python for your operating system
   - Make sure to check "Add Python to PATH" during installation

2. Install the CleanSort library using pip:
   ```bash
   pip install cleansort
   ```

### For Developers (Contributing to the Library)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cleansort
   cd cleansort
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Use the Library

### Simple Python Example
```python
# Import the library
from cleansort import CleanSort

# Create a new CleanSort object
cleaner = CleanSort()

# Example metadata (this could be from a website)
metadata = """
<meta name="title" content="Harry Potter">
<meta name="author" content="J.K. Rowling">
<meta name="isbn" content="978-0-7475-3269-9">
<meta name="source_site" content="books.com">
"""

# Process the metadata
result = cleaner.process_metadata(metadata)

# See the organized results
print(result)

# Get everything from the database
stored_data = cleaner.get_stored_metadata()
```

### Using the API from Any Programming Language

1. First, start the API server:
   - Open a terminal/command prompt
   - Navigate to your project directory
   - Run:
     ```bash
     python run_server.py
     ```
   - You'll see a message saying the server is running

2. Now you can use the library from any programming language!

#### JavaScript Example
```javascript
// Using fetch in browser or Node.js
async function processMetadata(metadata) {
    const response = await fetch('http://localhost:5000/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ metadata })
    });
    return await response.json();
}
```

#### Java Example
```java
// Using Java's HttpClient
String url = "http://localhost:5000/process";
String metadata = "<meta name=\"title\" content=\"My Book\">";
HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create(url))
    .POST(HttpRequest.BodyPublishers.ofString(
        "{\"metadata\": \"" + metadata + "\"}"))
    .header("Content-Type", "application/json")
    .build();
```

## What Kind of Data Can It Process?

The library can handle metadata about:
- Books
- Articles
- Journals
- Book chapters

It looks for these specific pieces of information:
- Names/titles
- Author names
- ISBN numbers
- Website sources

## Common Problems and Solutions

1. "Import error when using the library"
   - Make sure you installed the library using pip
   - Check that Python is in your system PATH

2. "Can't connect to the API"
   - Make sure the server is running (python run_server.py)
   - Check that you're using the correct URL (http://localhost:5000)

3. "Getting empty results"
   - Check that your metadata follows the expected format
   - Make sure it contains at least one of the supported fields

## Need Help?

If you run into any problems:
1. Check the Common Problems section above
2. Look at the example files in the 'examples' directory
3. Create an issue on GitHub

## License

MIT License - Feel free to use this library in your projects!