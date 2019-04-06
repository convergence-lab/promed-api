import argparse
from time import sleep
from datetime import datetime, timedelta
import urllib.request
from bs4 import BeautifulSoup
import json

def parse_result(data, day, verbose):
    parsed_data = []
    html = data["return"]
    soup = BeautifulSoup(html, 'lxml')
    elems = soup.select(".slink")
    for i, elem in enumerate(elems):
        print(elem)
        elem_dict = {}
        id_ = elem.attrs["id"].replace("id", "")
        req = urllib.request.Request(f"https://www.promedmail.org/ajax/getPost.php?alert_id={id_}")
        req.add_header("Referer", "http://www.promedmail.org")
        r = urllib.request.urlopen(req)
        data = r.read().decode("utf-8")
        data = json.loads(data)
        print(data)
        post_html = data["post"]
        soup2 = BeautifulSoup(post_html, "lxml")
        post_text = soup2.get_text()
        elem_dict["id"] = id_
        elem_dict["date"] = day.strftime("%m/%d/%Y")
        elem_dict["title"] = elem.text
        elem_dict["html"] = post_html
        elem_dict["text"] = post_text
        if verbose:
            print(f"{i}/{len(elems)} ID: {elem_dict['id']} Title: {elem_dict['title']}")
        r.close()
        parsed_data += [elem_dict]
        break
    return parsed_data

def search(search_from, search_to, verbose):
    search_from = datetime.strptime(search_from, "%m/%d/%Y")
    search_to = datetime.strptime(search_to, "%m/%d/%Y")
    aday = timedelta(days=1)

    day = search_from
    data_list = []
    while day < search_to:
        f = day.strftime("%m/%d/%Y")
        t = day + aday
        t = t.strftime("%m/%d/%Y")
        if verbose:
            print(f, t)
        with urllib.request.urlopen(f"https://www.promedmail.org/ajax/runSearch.php?kwby1=summary&search=&date1={f}&date2={t}&feed_id=1") as res:
            data = res.read().decode("utf-8")

        data = json.loads(data)
        data = parse_result(data, day, verbose)
        data_list += data
        day += aday
    return data_list

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='ProMed mail Searcher.')
    parser.add_argument("from_day", metavar="FROM", type=str, help="The first day you want to searchd search. The format is \"MM/DD/YYYY\"")
    parser.add_argument("to_day", metavar="TO", type=str, help="The last day you want to searchd search. The format is \"MM/DD/YYYY\"")
    parser.add_argument("--verbose", help="output verbose message", action="store_true")
    parser.add_argument("--output", type=str, help="output json file name.", default="data.json")
    args = parser.parse_args()
    result = search(args.from_day, args.to_day, args.verbose)

    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)
