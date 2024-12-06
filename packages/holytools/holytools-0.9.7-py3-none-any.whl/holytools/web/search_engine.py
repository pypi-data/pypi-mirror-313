from __future__ import annotations
import requests
import logging

from dataclasses import dataclass
# ---------------------------------------------------------

@dataclass
class SearchResult:
    name : str
    url : str
    desc : str

    def as_str(self) -> str:
        return f'[{self.name}]({self.url})\n{self.desc}\n'

    def __str__(self):
        return self.as_str()


class SearchEngine:
    def __init__(self,google_key : str, searchengine_id : str):
        self._GOOGLE_API_KEY : str = google_key
        self._SEARCHENGINE_ID : str = searchengine_id


    def get_urls(self, search_term: str, num_results : int = 5) -> list[str]:
        google_results = self.get_result_list(search_term=search_term, num_results=num_results)
        search_result_urls = [result['link'] for result in google_results]
        return search_result_urls


    def get_results(self, search_term : str, num_results : int = 5) -> list[SearchResult]:
        google_results = self.get_result_list(search_term=search_term, num_results=num_results)
        results = []
        for result in google_results:
            name = result['title']
            url = result['link']
            desc = result['snippet']
            search_result = SearchResult(name=name, url=url, desc=desc)
            results.append(search_result)
        return results


    def get_result_list(self, search_term : str, num_results : int = 5) -> list[dict]:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'q': f'{search_term}',
            'key': self._GOOGLE_API_KEY,
            'cx': self._SEARCHENGINE_ID,
            'num' : num_results
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            logging.warning(f'An error occured during search: {response.status_code} {response.reason}')
            return []

        response_json = response.json()
        reponse_content = response_json.get('items')
        if reponse_content is None:
            logging.warning(f'Unable to obtain search results')
            reponse_content = []

        return reponse_content