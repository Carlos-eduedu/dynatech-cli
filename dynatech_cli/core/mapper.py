import re
from time import sleep
from typing import List, Set
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from rich.console import Console

console = Console()


class Mapper:
    """
    Classe responsável por mapear páginas web a partir de um
    domínio inicial.
    Pode realizar mapeamento recursivo até uma profundidade
    máxima especificada.
    """

    DOMAIN_PATTERN = re.compile(
        r'https?://(?:www\.)?[-a-zA-Z0-9]{1,63}\.[a-zA-Z]{2,6}'
    )

    def __init__(
        self, domain: str, max_depth: int = 2, rate_limit: int = 0.5
    ) -> None:
        """
        Inicializa o Mapper com o domínio base e configurações.

        Args:
            domain (str): URL do domínio a ser mapeado.
            max_depth (int, optional): Profundidade máxima para mapeamento
            recursivo. Defaults to 2.
            rate_limit (float, optional): Intervalo em segundos entre
            requisições para controle de taxa. Defaults to 0.5.

        Raises:
            ValueError: Se a URL fornecida não for válida.
        """
        match = self.DOMAIN_PATTERN.findall(domain)
        if not match:
            raise ValueError('URL fornecida não é válida.')

        self.domain = match[0].rstrip('/')
        self.max_depth = max_depth
        self.rate_limit = rate_limit
        self.visited: Set[str] = set()
        self.all_links: Set[str] = set()

    @classmethod
    def _get_page(cls, url: str) -> BeautifulSoup:
        """
        Realiza uma requisição HTTP para a URL fornecida e retorna o conteúdo
        HTML.

        Args:
            url (str): URL a ser acessada.

        Returns:
            BeautifulSoup: Objeto BeautifulSoup com o conteúdo HTML da página.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except RequestException as e:
            console.log(f'[red]Erro ao acessar {url}:[/red] {e}')
            return BeautifulSoup('', 'html.parser')

    @classmethod
    def _find_links(cls, soup: BeautifulSoup) -> List[str]:
        """
        Extrai todos os links (`href`) presentes no HTML da página.

        Args:
            soup (BeautifulSoup): Objeto BeautifulSoup com o conteúdo HTML.

        Returns:
            List[str]: Lista de URLs extraídas.
        """
        return [link.get('href') for link in soup.find_all('a', href=True)]

    @classmethod
    def _clean_links(cls, links: List[str]) -> List[str]:
        """
        Filtra e limpa os links extraídos, removendo duplicatas e links
        inválidos.

        Args:
            links (List[str]): Lista de URLs extraídas.

        Returns:
            List[str]: Lista de URLs limpas e válidas.
        """
        link_pattern = re.compile(r'^/')
        cleaned = set()

        for link in links:
            if link and link_pattern.match(link):
                cleaned.add(link)

        return list(cleaned)

    def _is_valid_url(self, url: str) -> bool:
        """
        Verifica se a URL pertence ao mesmo domínio e não é de um tipo de
        arquivo indesejado.

        Args:
            url (str): URL a ser verificada.

        Returns:
            bool: True se a URL for válida, False caso contrário.
        """
        parsed_url = urlparse(url)
        domain_parsed = urlparse(self.domain)

        if parsed_url.netloc != domain_parsed.netloc:
            return False

        if any(
            parsed_url.path.endswith(ext)
            for ext in ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.svg']
        ):
            return False

        return True

    def _rate_limit_wait(self) -> None:
        """
        Aguarda o tempo especificado para controlar a taxa de requisições.
        """
        sleep(self.rate_limit)

    def crawl(self, url: str, depth: int) -> None:
        """
        Realiza o mapeamento recursivo de páginas web a partir de uma URL
        inicial.

        Args:
            url (str): URL inicial para mapeamento.
            depth (int): Profundidade atual de mapeamento.

        Raises:
            RecursionError: Se a profundidade máxima for atingida.
        """
        if depth > self.max_depth:
            return
        if url in self.visited:
            return

        self.visited.add(url)
        console.log(f"Visitando: [blue]{url}[/blue]")

        html = self._get_page(url)
        links = self._find_links(html)
        clean_links = self._clean_links(links)

        for link in clean_links:
            absolute_url = urljoin(self.domain, link)
            if (
                self._is_valid_url(absolute_url)
                and absolute_url not in self.visited
            ):
                self.all_links.add(absolute_url)
                self.crawl(absolute_url, depth + 1)
                self._rate_limit_wait()

    def map_web_site(self) -> List[str]:
        """
        Realiza o mapeamento do site de forma recursiva até a profundidade
        máxima.

        Returns:
            List[str]: Lista de todas as URLs mapeadas.
        """
        self.crawl(self.domain, 0)
        return sorted(self.all_links)
