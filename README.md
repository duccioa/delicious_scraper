# Save your Del.icio.us bookmarks to a 'json'
This is a simple function to collect all of your Del.icio.us bookmarks into a json, including links and tags.
The results are returned in the following structure:
```json
{
  "type": "Delicious bookmark collection",
  "collection_date": "07/08/2017 18:24:29",
  "username": "luposky",
  "features": [
    [
      {
        "title": "delicious-scraper",
        "id": "8ee9c64fa04e91f4fab98e6c4bd0ce5f",
        "link": "https://github.com/duccioa/delicious_scraper",
        "tags": [
          "python",
          "delicious",
          "scraper"
        ]
      }
    ]
  ]
}
```

To use it, simply do:
```python
import delicious_scraper as ds

js = ds.scrape_delicious_user(username="username", 
                              destination="./data_folder/file.json", 
                              start_page=1, 
                              end_page=2,
                              file_format="json")
```
If `file_format="html""` the function returns a Netscape Bookmark html that can be imported directly in Firefox or other browsers.
