import requests
import re
from bs4 import BeautifulSoup


def get_single_scp(scp_id):
    """Returns soup for a given SCP item number."""

    try:
        r = requests.get(url='http://www.scp-wiki.net/scp-' + str(scp_id))
        if r.status_code == 200:
            return BeautifulSoup(r.content)
        else:
            print('Failed to access SCP Wiki page. HTTP Status Code ' + str(r.status_code))
            return
    except requests.RequestException as e:
        print('Failed to access SCP Wiki page. Request Error: ' + e)
        return


def get_scp_name(scp_id):
    # get the name (which unfortunately isn't listed on the single page)
    try:
        if int(scp_id) < 1000:
            # Series I
            url = 'http://www.scp-wiki.net/scp-series'
        elif int(scp_id) < 2000:
            # Series II
            url = 'http://www.scp-wiki.net/scp-series-2'
        elif int(scp_id) < 3000:
            # Series III
            url = 'http://www.scp-wiki.net/scp-series-3'
        else:
            # Series XXX
            print('Unavailable SCP Series')
            return

        r = requests.get(url=url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content)
            content = soup.find('div', id='page-content')
            list_elements = content.find_all('li')
            for li in list_elements:
                if re.findall('[0-9]+', li.next['href']):
                    if int(re.findall('[0-9]+', li.next['href'])[0]) == scp_id:
                        return re.split(' - ', li.get_text())[-1]
        else:
            print('Failed to access SCP Wiki page. HTTP Status Code ' + str(r.status_code))
            return
    except requests.RequestException as e:
        print('Failed to access SCP Wiki page. Request Error: ' + e)
        return


def parse_scp(soup, scp_id):

    if soup is None:
        return None

    # get the rating
    try:
        rating = soup.find('span', {'class': 'rate-points'}).contents[1].contents[0].replace('+', '')
    except AttributeError:
        # print('no rating found')
        rating = 0

    # get the content block
    content = soup.find('div', id='page-content')

    # get the main image
    try:
        main_image = content.find('div', {'class': 'scp-image-block'}).contents[0]['src']
    except AttributeError:
        # print('no main_image found')
        main_image = None

    # get the image caption
    try:
        image_caption = content.find('div', {'class': 'scp-image-block'}).contents[2].contents[1].contents[0]
    except AttributeError:
        # print('no image_caption found')
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
        # print('can\'t parse content')
        mapping = None

    # get page info
    page_info = soup.find('div', id='page-info')
    revision = re.findall('\d+', page_info.next)[0]
    last_updated = page_info.find('span')['class'][1].replace('time_', '')

    # get the tags
    tags_list = soup.find('div', {'class': 'page-tags'}).find('span')
    tags = [tag.string for tag in tags_list if tag.string != '\n']

    # get a link to the discussion page
    discussion_link = 'http://www.scp-wiki.net' + soup.find('a', id='discuss-button')['href']

    return {
        'id': scp_id,
        'rating': int(rating),
        'image': {
            'src': main_image,
            'caption': image_caption
        },
        'content': mapping,
        'revision': int(revision),
        'last_edited': int(last_updated),
        'tags': tags,
        'discussion': discussion_link
    }


def scp(scp_id):
    """
    Returns a dictionary with as much content as possible regarding the SCP ID.
    :param scp_id: Either a string with the established format (002) or an integer (2)
    """

    if len(str(int(scp_id))) == 1:
        scp_id = '00' + str(int(scp_id))
    elif len(str(int(scp_id))) == 2:
        scp_id = '0' + str(int(scp_id))

    scp_name = get_scp_name(int(scp_id))
    site_content = get_single_scp(str(scp_id))
    parsed_content = parse_scp(site_content, int(scp_id))

    parsed_content['name'] = scp_name

    return parsed_content


# list = []
# for i in range(2, 100):
#     try:
#         list.append(parse_scp(get_single_scp(i)))
#     except:
#         continue
# print(json.dumps(list))

print(scp('002'))

