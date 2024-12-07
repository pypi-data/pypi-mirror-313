from flask import current_app

from osbot_utils.utils.Dev import pprint

DEFAULT_WEB_PREFIX = '/web'

def menu_links(prefix):

    url_map = current_app.url_map                           # Get the current Flask app's URL map
    matching_routes = {}                                    # Initialize an empty dictionary for matching routes

    rules = {str(rule):rule for rule in url_map.iter_rules()}

    for rule_str, rule in sorted(rules.items()):            # Loop through each rule in the  (sorted) URL map
        if '/api' in rule_str:                              # Skip any API routes
            continue
        if '<' in rule_str:                                 # Skip any routes with dynamic parts
            continue
        if 'POST' in rule.methods:                          # Skip any POST routes
            continue
        if rule_str.startswith(DEFAULT_WEB_PREFIX+prefix):                     # Check if the rule starts with the prefix
            last_part = rule_str.split('/')[-1]                             # Extract the last part of the route
            title = last_part.replace('-', ' ').title()         # Replace hyphens with spaces and title-case it

            if title == '':
                title = prefix[1:].title()                                  # If it's the root route, use the prefix itself (without slash)

            # todo: find a better way to handle the DEFAULT_WEB_PREFIX
            matching_routes[title] = rule_str          # Add to dictionary with title as key and rule as value

    return matching_routes                                                  # Return the dictionary of matching routes