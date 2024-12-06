# print-wp-sources

This program just prints the sources of the given Wikipedia article to standard output.

## Installation

``` shell
pipx install print-wp-sources --include-deps
```

## Usage

Use the Wikipedia article's name as the argument to `print-wp-sources`. For example, if the article's URL is `https://en.wikipedia.org/wiki/Automatic_negative_thoughts`, then the argument for `print-wp-sources` would be `"Automatic_negative_thoughts"`.

``` shell
print-wp-sources "Automatic_negative_thoughts"

Output:
https://pubmed.ncbi.nlm.nih.gov/26431418
https://www.theguardian.com/lifeandstyle/2014/aug/11/how-to-silence-negative-thinking
https://www.inc.com/chris-winfield/is-stomping-ants-the-key-to-living-a-happier-life.html
https://doi.org/10.1007%2Fbf01178214
https://api.semanticscholar.org/CorpusID:22915336
https://www.huffingtonpost.com/entry/how-to-stop-automatic-negative-thoughts_us_58330f18e4b0eaa5f14d4833
https://doi.org/10.1037%2F0022-006x.51.5.721
https://pubmed.ncbi.nlm.nih.gov/6630686
https://wikimediafoundation.org/
```

> Note: make sure to use quotes around the article name in the argument to `print-wp-sources`.

One can also easily pipe the output to a file.

``` shell
print-wp-sources "Automatic_negative_thoughts" > sources.txt
print-wp-sources "Python_(programming_language)" | tee sources.txt
```
