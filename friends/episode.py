import requests
from bs4 import BeautifulSoup


class Episode:
    def __init__(self, episode_numbers: list[int], season: int, title: str, link: str):
        self.episode_numbers = episode_numbers
        self.season = season
        self.title = title
        self.link = link

    def __repr__(self):
        """Episode summary."""
        episode_str = "-".join(map(str, self.episode_numbers))
        return f"Episode {episode_str}: {self.title} (Season {self.season}, Link: {self.link})"


class EpisodeFactory:
    def __init__(self):
        self.url = "https://fangj.github.io/friends/"
        self.soup = self._get_soup()
        self.tags: list[BeautifulSoup] = self.soup.find_all("a")

    def _get_soup(self) -> BeautifulSoup:
        headers = {"Accept-Encoding": "identity"}
        r = requests.get(self.url, headers=headers, timeout=10)
        content = r.text
        soup = BeautifulSoup(content, "html.parser")
        return soup

    def create_episodes(self) -> list[Episode]:
        """Dispatch a list of Episode objects."""
        episodes = []
        for tag in self.tags:
            link = tag["href"]
            if isinstance(link, list):
                link = link[0]
            text = tag.get_text().strip()
            episode_numbers_text = text.split(" ")[0]
            episode_numbers = list(map(int, episode_numbers_text.split("-")))
            season = episode_numbers[0] // 100
            title = text[len(episode_numbers_text) + 2 :].strip()
            episode = Episode(episode_numbers, season, title, self.url + link)
            episodes.append(episode)
        return episodes
