from __future__ import annotations

from bs4 import BeautifulSoup, NavigableString, Tag, PageElement


class LinkSoup(BeautifulSoup):
    # noinspection PyUnresolvedReferences
    def _all_strings(self, strip=False, types=PageElement.default):
        _ = strip

        if types is self.default:
            types = self.interesting_string_types

        for descendant in self.descendants:
            if isinstance(descendant, Tag) and descendant.name == 'a':
                link_text = descendant.text.strip()
                link_text = link_text.replace('\n', ' ')
                yield str(f"<({link_text})[{descendant.get('href')}]> ")
            if isinstance(descendant, NavigableString) and descendant.parent.name == 'a':
                continue

            if types is None and not isinstance(descendant, NavigableString):
                continue
            descendant_type = type(descendant)
            if isinstance(types, type):
                if descendant_type is not types:
                    continue
            elif types is not None and descendant_type not in types:
                continue
            if strip:
                descendant = descendant.strip()
                if len(descendant) == 0:
                    continue
            yield descendant

