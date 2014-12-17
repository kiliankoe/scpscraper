import requests
import re
from bs4 import BeautifulSoup


def get_single_scp(scp_id):
    """Returns soup for a given SCP item number."""

    if len(str(scp_id)) == 1:
        scp_id = '00' + str(scp_id)
    elif len(str(scp_id)) == 2:
        scp_id = '0' + str(scp_id)

    try:
        r = requests.get(url='http://www.scp-wiki.net/scp-' + str(scp_id))
        if r.status_code == 200:
            return BeautifulSoup(r.content)
        else:
            print('Failed to access SCP Wiki page. HTTP Status Code ' + str(r.status_code))
            return None
    except requests.RequestException as e:
        print('Failed to access SCP Wiki page. Request Error: ' + e)
        return None


def parse_scp(soup):

    if soup is None:
        return None

    # get the rating
    try:
        rating = soup.find('span', {'class': 'rate-points'}).contents[1].contents[0].replace('+', '')
    except AttributeError:
        print('no rating found')
        rating = 0

    # get the content block
    content = soup.find('div', id='page-content')

    # get the main image
    try:
        main_image = content.find('div', {'class': 'scp-image-block'}).contents[0]['src']
    except AttributeError:
        print('no main_image found')
        main_image = None

    # get the image caption
    try:
        image_caption = content.find('div', {'class': 'scp-image-block'}).contents[2].contents[1].contents[0]
    except AttributeError:
        print('no image_caption found')
        image_caption = None

    # get main content
    try:
        mapping = {}
        key = None
        for item in content.find_all('p'):
            if item.strong:
                key = item.strong.get_text(strip=True).rstrip(':')
                value = item.strong.next_sibling.strip()
            else:
                if key is not None:
                    value = mapping[key] + ' ' + item.get_text(strip=True)
                else:
                    value = None
            mapping[key] = value
        mapping.pop(None)
    except AttributeError:
        print('can\'t parse content')
        mapping = None

    # get page info
    page_info = soup.find('div', id='page-info')
    revision = re.findall('\d+', page_info.next)[0]
    last_updated = page_info.find('span')['class'][1].replace('time_', '')

    # TODO: get the tags, link to the discussion page, other stuff?

    return {
        'rating': int(rating),
        'image': {
            'src': main_image,
            'caption': image_caption
        },
        'content': mapping,
        'revision': int(revision),
        'last_edited': int(last_updated)
    }


print(parse_scp(get_single_scp(678)))
