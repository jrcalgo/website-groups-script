## Simple website URL script for grouping and opening said grouped URLs in one window
<b>Very much so a Quality-of-life improvement over just using favorites or bookmarks in your browser</b>
### <ins>Functionality:</ins>
 - Opens group of URLs in a new window of your OS' default browser
 - Adding/editing/removing groups all takes place in url_groups.json <b>(Do this by hand.... for now)</b>
 - Upon opening a group, recent_url_groups.csv is updated according to current date & time
### <ins>How to use:</ins>
 - CLI: Run <b><i>open</i></b> to open specific URL group(s)
 - CLI: Run <b><i>list</i></b> to list all URL groups currently stored in the .json file
 - CLI: Run <b><i>sort</i></b> to sort the .json file with the following arguments: 
     - <b><i>-az</i></b> for A-Z alphabetical sort,
     - <b><i>-za</i></b> for Z-A alphabetical sort,
     - <b><i>-mr</i></b> for most recently-used sort,
     - <b><i>-lr</i></b> for least recently-used sort. 
     - <b>*** Default sort without args is <i>-az</i> ***</b>
 - CLI: Run <i>fix_file</i> to: <b>A)</b> create a new .json file if file is missing, or <b>B)</b> deprecate current .json and .csv files in favor for default format files

