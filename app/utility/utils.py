from datetime import datetime
from app.lib import BeautifulSoup as Bs


def date_from(timestamp):
    """Format the given timestamp""" 
    return datetime.fromtimestamp(timestamp)

def get_inner_node_value(node):
    if node.string is None:        
        return get_inner_node_value(node.next)    
    else:        
        return node.string

def suppify_body(body):
    """Return supped body with sups and links"""
    count = 1
    links_dict = {}
    soup = Bs.BeautifulSoup(body)
    for link_tag in soup.findAll('a'):
        inner_node_value = get_inner_node_value(link_tag)    
        if link_tag.has_key('href') and len(link_tag['href']) > 0 and inner_node_value.strip()!= '' and link_tag['href'].upper() != inner_node_value.upper():
                links_dict[count]  = link_tag['href']          
                link_tag.replaceWith( link_tag.prettify() + '<sup style="font-size:9px">[%d]</sup>' % count )          
                count += 1
    return (soup,links_dict)