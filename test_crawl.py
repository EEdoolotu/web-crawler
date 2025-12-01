import unittest

# Assuming your functions are correctly imported from 'crawl'
from crawl import normalize_url, get_h1_from_html, get_first_paragraph_from_html, get_urls_from_html, get_images_from_html, extract_page_data


class TestCrawl(unittest.TestCase):

    ## 🔗 normalize_url Tests
    
    def test_normalize_url_basic(self):
        input_url = "https://blog.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_trailing_slash(self):
        """Should remove trailing slash."""
        input_url = "https://blog.boot.dev/path/"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_query_and_fragment(self):
        """Should strip query parameters and fragment."""
        input_url = "https://blog.boot.dev/path/?q=test#fragment"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)
        
    def test_normalize_url_case_insensitivity(self):
        """Should handle different netloc casing (if normalize_url lowercases netloc)."""
        input_url = "hTTps://BlOg.Boot.Dev/Path"
        # Assuming the normalize_url function lowercases the netloc
        actual = normalize_url(input_url) 
        expected = "blog.boot.dev/Path" 
        self.assertEqual(actual, expected)

    # ---

    ## 📄 get_h1_from_html Tests
    
    def test_get_h1_from_html_basic(self):
        input_body = '<html><body><h1>Test Title</h1></body></html>'
        actual = get_h1_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_h1_from_html_missing(self):
        """Should return empty string if no h1 tag is present."""
        input_body = '<html><body><h2>Title</h2></body></html>'
        actual = get_h1_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    # ---

    ## 📄 get_first_paragraph_from_html Tests

    def test_get_first_paragraph_from_html_main_priority(self):
        """Should prioritize <p> inside <main> over one outside."""
        input_body = '''<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_main_fallback(self):
        """Should fall back to the first <p> if <main> is missing."""
        input_body = '<html><body><p>First paragraph.</p><div><p>Second paragraph.</p></div></body></html>'
        actual = get_first_paragraph_from_html(input_body)
        expected = "First paragraph."
        self.assertEqual(actual, expected)
        
    def test_get_first_paragraph_from_html_missing(self):
        """Should return empty string if no <p> tags are present."""
        input_body = '<html><body><h1>Header only</h1></body></html>'
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)
        
    # ---

    ## 🌐 get_urls_from_html Tests (Expanded)

    # Note: Renamed your redundant absolute tests for clarity and proper structure
    
    def test_get_urls_from_html_multiple_types(self):
        """Should extract relative, absolute, and full path links and join them."""
        input_url = "https://boot.dev/course/"
        input_body = '''<html><body>
            <a href="/about">Relative Root</a>
            <a href="lessons/1">Relative Path</a>
            <a href="https://other.com/page">Absolute URL</a>
            <a name="anchor">Ignore this</a>
        </body></html>'''
        actual = get_urls_from_html(input_body, input_url)
        expected = [
            "https://boot.dev/about",
            "https://boot.dev/course/lessons/1",
            "https://other.com/page"
        ]
        self.assertCountEqual(actual, expected) # Use assertCountEqual for order independence

    def test_get_urls_from_html_relative_root(self):
        """Test a link starting with a single slash (relative to root)."""
        input_url = "https://example.com/section/page"
        input_body = '<html><body><a href="/assets/file.js">JS File</a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://example.com/assets/file.js"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_empty_body(self):
        """Should return an empty list when no <a> tags are present."""
        input_url = "https://example.com"
        input_body = '<html><body><p>No links here.</p></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    # ---

    ## 🖼️ get_images_from_html Tests (Expanded)
    
    def test_get_images_from_html_multiple_types(self):
        """Should correctly join relative paths and keep absolute paths."""
        input_url = "https://higherleague.com/page"
        input_body = '''<html><body>
            <img src="/logo.png" alt="Logo">
            <img src="assets/icon.svg">
            <img src="https://cdn.external.com/pic.jpg">
            <img alt="No src">
        </body></html>'''
        actual = get_images_from_html(input_body, input_url)
        expected = [
            "https://higherleague.com/logo.png",
            "https://higherleague.com/assets/icon.svg",
            "https://cdn.external.com/pic.jpg"
        ]
        self.assertCountEqual(actual, expected)
    
    def test_get_images_from_html_no_src(self):
        """Should ignore <img> tags that are missing the 'src' attribute."""
        input_url = "https://google.com"
        input_body = '<html><body><img data-src="/lazy.png" alt="Lazy"><img alt="No Src"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)
        
    def test_get_images_from_html_empty_body(self):
        """Should return an empty list when no <img> tags are present."""
        input_url = "https://beats.com"
        input_body = '<html><body><a href="/">Link</a></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_extract_page_data_basic(self):
        input_url = "https://blog.boot.dev"
        input_body = '''<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://blog.boot.dev/link1"],
            "image_urls": ["https://blog.boot.dev/image1.jpg"]
        }
        self.assertEqual(actual, expected)

    
    def test_extract_page_data_missing_elements(self):
        """Should handle missing <h1>, <p>, <a>, and <img> tags gracefully."""
        input_url = "https://no-content.net"
        input_body = '''<html><body>
            <h2>Subtitle</h2>
            <div>Some text only</div>
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://no-content.net",
            "h1": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": []
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_absolute_external_links(self):
        """Should correctly handle external absolute links and images."""
        input_url = "http://internal-site.org"
        input_body = '''<html><body>
            <h1>Absolute Links</h1>
            <a href="https://google.com/search?q=test">External Link</a>
            <a href="/internal-page">Internal Link</a>
            <img src="http://cdn.images.com/logo.gif" alt="External Image">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "http://internal-site.org",
            "h1": "Absolute Links",
            "first_paragraph": "", # Assumes no <p> is found
            "outgoing_links": [
                "https://google.com/search?q=test",
                "http://internal-site.org/internal-page"
            ],
            "image_urls": ["http://cdn.images.com/logo.gif"]
        }
        self.assertCountEqual(actual['outgoing_links'], expected['outgoing_links'])
        self.assertEqual(actual, expected)

    def test_extract_page_data_multiple_assets(self):
        """Should collect multiple outgoing links and images."""
        input_url = "https://example.com"
        input_body = '''<html><body>
            <main><p>Multiple elements test.</p></main>
            <a href="product/1">Prod 1</a>
            <a href="/about">About</a>
            <img src="img/icon.png">
            <img src="https://static.com/photo.jpg">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://example.com",
            "h1": "",
            "first_paragraph": "Multiple elements test.",
            "outgoing_links": [
                "https://example.com/product/1",
                "https://example.com/about"
            ],
            "image_urls": [
                "https://example.com/img/icon.png",
                "https://static.com/photo.jpg"
            ]
        }
        # Use assertCountEqual on lists for order independence, then assert overall dict equality
        self.assertCountEqual(actual['outgoing_links'], expected['outgoing_links'])
        self.assertCountEqual(actual['image_urls'], expected['image_urls'])
        
        # Remove lists for final dict comparison
        del actual['outgoing_links'], actual['image_urls']
        del expected['outgoing_links'], expected['image_urls']
        self.assertEqual(actual, expected)

    def test_extract_page_data_nested_paragraph(self):
        """Should find the paragraph even when nested (if get_first_paragraph_from_html handles nesting)."""
        input_url = "https://nested.dev"
        input_body = '''<html><body>
            <p>Outer P</p>
            <main>
                <div>
                    <p>The target P</p>
                </div>
            </main>
            <a href="home">Home</a>
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://nested.dev",
            "h1": "",
            # Assuming get_first_paragraph_from_html prioritizes <main> and finds nested <p>
            "first_paragraph": "The target P", 
            "outgoing_links": ["https://nested.dev/home"],
            "image_urls": []
        }
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()